import telebot
import random
import sqlite3 as sql

bot = telebot.TeleBot('1830142505:AAF0QUSHxOS_QVjhLxVuwLeJkgaVj8Ln6So')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Я работаю.')

bot.polling(none_stop=True)