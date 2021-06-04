import telebot
import random
import sqlite3 as sql

bot = telebot.TeleBot('1833045242:AAEZcG7f1HDnz-sU_AFYbPNDeRNO5GcrW1Q')
ev = random.randint(1, 2)

in_game_ids = []
mass_id_inroom = {1: [],
                  2: []}
locations = ['город', 'горы']


@bot.message_handler(commands=['start'])
def send_welcome(message):
    con = sql.connect('data.db')
    cur = con.cursor()
    cur.execute(f'select arc_1, title from events where id = {ev}')
    res = cur.fetchall()
    arc_1 = res[0][0]
    title = res[0][1]
    bot.send_message(message.chat.id,
                     f'Привет! Я бот для рп-игр. Сейчас идёт ивент "{title}". \n"{arc_1}". \nНапиши /new_character чтобы создать анкету.')
    cur.execute(f'select id from users')
    meh = cur.fetchall()
    sp = list(map(lambda x: str(x[0]), meh))
    if str(message.from_user.id) not in sp:
        cur.execute(f'INSERT INTO users (id) VALUES ({message.from_user.id});')
    cur.execute(f'update users set state = \'default\' where id = {message.from_user.id}')
    con.commit()


@bot.message_handler(commands=['help'])
def help_message(message):
    if in_game_ids.count(message.from_user.id) < 1:
        bot.send_message(message.chat.id,
                         'Чтобы войти в игру напиши /new_character, после чего ты создашь персонажа для евента, а затем войдешь в игру.\n'
                         'Чтобы узнать, что это за бот, напиши /start\n'
                         'Чтобы узнать подробнее про идущий евент, напиши /event_info')
    else:
        bot.send_message(message.chat.id, 'Чтобы узнать, что это за бот, напиши /start\n'
                                          'Чтобы узнать подробнее про идущий евент, напиши /event_info')


@bot.message_handler(commands=['new_character'])
def create_character(message):
    if in_game_ids.count(message.from_user.id) < 1:
        con = sql.connect('data.db')
        cur = con.cursor()
        cur.execute(f'select races, classes from events where id = {ev}')
        respon = cur.fetchall()
        bot.send_message(message.chat.id,
                         'Введите свой никнэйм, пол вашего персонажа, его класс, рассу, характер, и описание вашего персонажа (для примера историю, подробности, и т. д.)\n'
                         'Укажите это в виде:\n'
                         'никнэйм|пол|класс|расса|характер|описание\n'
                         '!!!НЕ ИСПОЛЬЗУЙТЕ СИМВОЛ "|" ВНУТРИ ТЕКСТА!!!\n'
                         f'Доступные рассы: {respon[0][0]}\n'
                         f'Доступные классы: {respon[0][1]}')
        cur.execute(f'update users set state = \'getting_info\' where id = {message.from_user.id}')
        con.commit()


@bot.message_handler(commands=['location'])
def location_select(message):
    global commands_state
    bot.send_message(message.from_user.id, 'Выберите локацию, к которой хотите присоединиться:\n'
                                           '1.Город\n'
                                           '2.Горы')
    commands_state = 'move_to_another_location'


@bot.message_handler(content_types=['text'])
def default_text(message):
    con = sql.connect('data.db')
    cur = con.cursor()
    cur.execute(f'select state from users where id = {message.from_user.id}')
    res = cur.fetchall()
    state = res[0][0]
    if state == 'default':
        bot.send_message(message.from_user.id, 'FUCK U')
    elif state == 'getting_info':
        sp = '\', \''.join(message.text.split('|'))
        print(f'update users set state = \'{sp}\' where id = {message.from_user.id}')
        cur.execute(f'update users set state = \'{sp}\' where id = {message.from_user.id}')
        cur.execute(f'update users set state = \'default\' where id = {message.from_user.id}')
    elif state == 'move_to_another_location':
        if message.text in [1, 2]:
            mass_id_inroom[message.text].append(message.from_user.id)
            bot.send_message(message.from_user.id,
                             f'Вы теперь находитесь в локации {locations[int(message.text) - 1]}.')
        else:
            bot.send_message(message.from_user.id, 'Это не так локация которую вы ищете (Такой локации нет)')


bot.polling(none_stop=True)
