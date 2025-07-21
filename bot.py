import telebot
import os
from telebot import types
from flask import Flask
import threading

# Получаем токен из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Telegram ID для логов
ADMIN_CHAT_ID = 7564532772

# Канал для обязательной подписки
CHANNEL_USERNAME = "atelier_NS"  # без @

# Сопоставление кнопок с названиями PDF-файлов
price_files = {
    "man": ("👔 Пошив мужской одежды", "Прайс М.pdf"),
    "woman": ("👗 Пошив женской одежды", "Прайс Ж.pdf"),
    "man_premium": ("🧥 Премиум пошив мужской одежды", "Прайс М премиум.pdf"),
    "woman_premium": ("💃 Премиум пошив женской одежды", "Прайс Ж премиум.pdf"),
    "repair": ("🧵 Ремонт и подгонка", "Прайс ремонт и подгонка.pdf")
}

# --- Flask-хендлеры для проверки статуса приложения ---
@app.route('/')
def index():
    return "Бот работает."

@app.route('/ping')
def ping():
    return "pong"

# --- Проверка подписки на канал ---
def is_subscribed(chat_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", chat_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

# --- Логирование сообщений в личный Telegram ---
def log_event(text):
    try:
        bot.send_message(ADMIN_CHAT_ID, text)
    except Exception as e:
        print(f"Ошибка логирования: {e}")

# --- Главное меню с прайсами ---
def show_price_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for key, (label, _) in price_files.items():
        markup.add(types.InlineKeyboardButton(text=label, callback_data=key))
    markup.add(
        types.InlineKeyboardButton("📞 Связаться с мастером", url="https://t.me/atelierNS"),
        types.InlineKeyboardButton("🌐 Посетить сайт", url="https://atelierns.ru")
    )
    bot.send_message(chat_id, "💬 *Выберите интересующий вас прайс:*", reply_markup=markup, parse_mode="Markdown")

# --- Обработка команды /start ---
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    if not is_subscribed(chat_id):
        text = (
            "✨ *Рады приветствовать Вас в ателье Натальи Савиной.*\n\n"
            "Чтобы получить доступ к прайсам, пожалуйста, подпишитесь на наш канал:\n"
            "👉 [@atelier_NS](https://t.me/atelier_NS)\n\n"
            "После подписки нажмите /start ещё раз."
        )
        bot.send_message(chat_id, text, parse_mode="Markdown")
        return

    show_price_menu(chat_id)
    log_event(f"✅ @{message.from_user.username or 'без_юзернейма'} открыл бот")

# --- Обработка нажатий на кнопки ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "back":
        show_price_menu(call.message.chat.id)
        return

    if call.data in price_files:
        label, filename = price_files[call.data]
        try:
            with open(filename, "rb") as f:
                bot.send_document(call.message.chat.id, f, caption=filename)
            log_event(f"📥 @{call.from_user.username or 'без_юзернейма'} запросил прайс: {label}")
        except:
            bot.send_message(call.message.chat.id, "❗️Ошибка при отправке файла.")

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back"))
        bot.send_message(call.message.chat.id, "Вы можете вернуться назад и выбрать другой прайс:", reply_markup=markup)

# --- Обработка текстовых сообщений (вопросов) ---
@bot.message_handler(func=lambda m: True)
def handle_question(message):
    bot.send_message(message.chat.id, "Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.")
    log_event(f"❓ Вопрос от @{message.from_user.username or 'без_юзернейма'}: {message.text}")

# --- Flask-сервер для Fly.io ---
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- Запуск ---
print("Бот запущен.")
threading.Thread(target=run_flask).start()
bot.polling()
