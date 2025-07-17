import telebot
import os
from telebot import types
from flask import Flask
import threading

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Flask-сервер для Render
app = Flask(__name__)

# Канал, на который должна быть подписка (без @)
CHANNEL_USERNAME = "atelier_NS"

# Сопоставление кнопок и PDF-файлов
price_files = {
    "man": ("👔 Пошив мужской одежды", "Прайс М.pdf"),
    "woman": ("👗 Пошив женской одежды", "Прайс Ж.pdf"),
    "man_premium": ("🧥 Премиум пошив мужской одежды", "Прайс М премиум.pdf"),
    "woman_premium": ("💃 Премиум пошив женской одежды", "Прайс Ж премиум.pdf"),
    "repair": ("🧵 Ремонт и подгонка", "Прайс ремонт и подгонка.pdf")
}

# Проверка подписки
def is_subscribed(chat_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", chat_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# Обработка команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    if not is_subscribed(chat_id):
        text = (
            "✨ *Рады приветствовать Вас в ателье Натальи Савиной.*\n\n"
            "Чтобы получить доступ к прайсам, пожалуйста, подпишитесь на наш Telegram-канал:\n"
            "👉 [@atelier_NS](https://t.me/atelier_NS)\n\n"
            "После подписки нажмите /start ещё раз."
        )
        bot.send_message(chat_id, text, parse_mode="Markdown")
        return

    # Показываем кнопки с прайсами
    markup = types.InlineKeyboardMarkup()
    for key, (label, _) in price_files.items():
        markup.add(types.InlineKeyboardButton(text=label, callback_data=key))

    bot.send_message(chat_id, "💬 *Выберите интересующий вас прайс:*", reply_markup=markup, parse_mode="Markdown")

# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: call.data in price_files)
def send_pdf(call):
    _, filename = price_files[call.data]
    try:
        with open(filename, "rb") as f:
            bot.send_document(call.message.chat.id, f, caption=filename)
    except:
        bot.send_message(call.message.chat.id, "❗️Ошибка при отправке файла.")

# Flask для Render (не даёт боту уснуть)
@app.route('/')
def index():
    return "Бот работает."

@app.route('/ping')
def ping():
    return "pong"

# Запуск Flask-сервера в отдельном потоке
def run_flask():
    app.run(host="0.0.0.0", port=10000)

print("Бот запущен.")
threading.Thread(target=run_flask).start()
bot.polling()
@bot.message_handler(commands=['id'])
def send_user_id(message):
    bot.send_message(message.chat.id, f"Ваш user_id: `{message.chat.id}`", parse_mode="Markdown")
