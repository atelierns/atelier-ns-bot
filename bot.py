import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот ателье.\nВот наши актуальные прайсы 👇"
    )

    # Отправляем PDF-файлы с прайсами
    file_paths = [
        "Прайс ремонт и подгонка.pdf",
        "Прайс М.pdf",
        "Прайс М премиум.pdf",
        "Прайс М премиум (1).pdf",
        "Прайс Ж.pdf",
        "Прайс Ж премиум.pdf"
    ]

    for file_name in file_paths:
        with open(file_name, "rb") as pdf:
            bot.send_document(message.chat.id, pdf, caption=file_name)

print("Бот запущен.")
bot.polling()
