import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

price_text = """
💼 Прайс-лист:

🔹 Консультация — 1000₽  
🔹 Аудит сайта — 3000₽  
🔹 Настройка рекламы — от 5000₽  
🔹 Ведение соцсетей — от 7000₽

📩 Напишите, если хотите обсудить детали!
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот, отправляю прайс. Напиши /price")

@bot.message_handler(commands=['price'])
def send_price(message):
    bot.send_message(message.chat.id, price_text)

print("Бот запущен.")
bot.polling()
