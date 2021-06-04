import telebot
import random
import sqlite3 as sql

bot = telebot.TeleBot('1833045242:AAEZcG7f1HDnz-sU_AFYbPNDeRNO5GcrW1Q')

event = 'Надвигающаяся гроза'

in_game_ids = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Привет! Я бот для рп-игр. Сейчас идёт ивент "{event}". Сейчас происходит: "{event}". Напиши /new_character чтобы создать анкету.')

@bot.message_handler(commands=['help'])
def help_message(message):
    if in_game_ids.count(message.from_user.id) < 1:
        bot.send_message(message.chat.id, 'Чтобы войти в игру напиши /new_character, после чего ты создашь персонажа для евента, а затем войдешь в игру.\n'
                                          'Чтобы узнать, что это за бот, напиши /start\n'
                                          'Чтобы узнать подробнее про идущий евент, напиши /event_info')
    else:
        bot.send_message(message.chat.id, 'Чтобы узнать, что это за бот, напиши /start\n'
                         'Чтобы узнать подробнее про идущий евент, напиши /event_info')

@bot.message_handler(commands=['/new_character'])
def create_character(message):
    if in_game_ids.count(message.from_user.id) < 1:
        bot.send_message(message.chat.id, f'Привет! Я бот для рп-игр. Сейчас идёт ивент "{event}". Сейчас происходит: "{event}". Напиши /new_character чтобы создать анкету.')

bot.polling(none_stop=True)