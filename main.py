import os
import telebot
from telebot import types

TOKEN = os.getenv('TELEGRAM_TOKEN') or "8215407859:AAGFlmK7VGW5eDZMKYbPoo-t8raLOXmNNAI"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🎁 Создать сделку", callback_data="deal")
    btn2 = types.InlineKeyboardButton("👥 Реферальная система", callback_data="ref")
    btn3 = types.InlineKeyboardButton("🌐 Язык", callback_data="lang")
    btn4 = types.InlineKeyboardButton("🆘 Поддержка", callback_data="help")
    
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    
    text = "💎 **Saphire Gift**\n\nДобро пожаловать! Ваш надежный P2P-гарант 😊"
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "deal":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("💎 TON", callback_data="ton")
        btn2 = types.InlineKeyboardButton("💳 Карта", callback_data="card")
        btn3 = types.InlineKeyboardButton("⭐ Звезды", callback_data="stars")
        btn4 = types.InlineKeyboardButton("🔙 Назад", callback_data="back")
        
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        markup.add(btn4)
        
        bot.edit_message_text("Выберите метод оплаты:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data == "back":
        start(call.message)

print("🤖 Бот запущен!")
bot.infinity_polling()

