import telebot
import random
import sqlite3 as sql

bot = telebot.TeleBot('1833045242:AAEZcG7f1HDnz-sU_AFYbPNDeRNO5GcrW1Q')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'hello and about')

bot.polling(none_stop=True)