import telebot
import os
from flask import Flask

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Бот работает."

@app.route('/ping')
def ping():
    return "pong"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот ателье.\nВот наши актуальные прайсы 👇"
    )

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

# запускаем Flask в отдельном потоке
import threading
def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()
bot.polling()
