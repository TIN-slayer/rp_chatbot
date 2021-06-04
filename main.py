import telebot
import random
import sqlite3 as sql

bot = telebot.TeleBot('1833045242:AAEZcG7f1HDnz-sU_AFYbPNDeRNO5GcrW1Q')

event = 'Надвигающаяся гроза'

commands_state = 'default'
in_game_ids = []
mass_id_inroom = {1:[],
                  2:[]}
locations = ['город', 'горы']

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

@bot.message_handler(commands=['new_character'])
def create_character(message):
    if in_game_ids.count(message.from_user.id) < 1:
        bot.send_message(message.chat.id, 'Введите свой никнэйм, пол вашего персонажа, его класс, рассу, характер, и описание вашего персонажа (для примера историю, подробности, и т. д.)\n'
                                          'Укажите это в виде:\n'
                                          'никнэйм|пол|класс|расса|характер|описание\n'
                                          '!!!НЕ ИСПОЛЬЗУЙТЕ СИМВОЛ "|" ВНУТРИ ТЕКСТА!!!')
@bot.message_handler(commands=['location'])
def location_select(message):
    global commands_state
    bot.send_message(message.from_user.id, 'Выберите локацию, к которой хотите присоединиться:\n'
                                           '1.Город\n'
                                           '2.Горы')
    commands_state = 'move_to_another_location'

@bot.message_handler(content_types=['text'])
def default_text(message):
    if commands_state == 'move_to_another_location':
        if message.text in [1, 2]:
            mass_id_inroom[message.text].append(message.from_user.id)
            bot.send_message(message.from_user.id, f'Вы теперь находитесь в локации {locations[int(message.text)-1]}.')
        else:
            bot.send_message(message.from_user.id, 'Это не так локация которую вы ищете (Такой локации нет)')

bot.polling(none_stop=True)
