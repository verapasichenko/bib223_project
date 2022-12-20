import telebot
from pyowm import OWM
from telebot import types
from Token import BotToken

from lib.database import Database
from lib.stations import stations_data


db = Database()
bot = telebot.TeleBot(BotToken)


def get_location(lat, lon):
    '''
    :param lat: широта
    :param lon:долгота
    :return:ссылку нужную
    '''
    url = f"https://yandex.ru/pogoda/maps/nowcast?lat={lat}&lon={lon}&via=hnav&le_lightning=1"
    return url


def weather(city: str):
    '''
    Функция в ответ на город выводит ее температуру
    :param city: вводим город
    :return: выводим температуру и локацию
    '''
    owm = OWM('4b4ba7fd4d10e6a206a383cc2bba05dc')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    location = get_location(observation.location.lat, observation.location.lon)
    temperature = weather.temperature("celsius")
    return temperature, location


@bot.message_handler(commands=['weather'])
def get_weather_message(message):
    '''
    Функция откликается на команду и задает вопрос пользователю
    :param message: сообщение пользователя в боте
    :return: погоду
    '''
    bot.send_message(message.from_user.id, "Введи название города: ")
    bot.register_next_step_handler(message, get_weather)


def get_weather(message):
    '''
    Функция принимает сообщение(город) и показывает погоду в этом городе
    :param message: получает город от пользователя
    :return: возвращает ему погоду в этом городе
    '''
    city = message.text
    try:
        w = weather(city)
        bot.send_message(message.from_user.id, f'В городе {city} сейчас {round(w[0]["temp"])} градусов,'
                                               f'чувствуется как {round(w[0]["feels_like"])} градусов')
        bot.send_message(message.from_user.id, w[1])
        bot.send_message(message.from_user.id,
                         "Отлично! Ты узнал погоду на сегодня! Теперь нажми /help, чтобы мы могли выбрать подходящее место твоего времяпрепровождения")

    except Exception:  # что нужно сделать чтобы не было ошибки
        bot.send_message(message.from_user.id, "Такого города я не припомню...")
        bot.send_message(message.from_user.id, "Введи еще раз название города: ")
        bot.register_next_step_handler(message, get_weather)


@bot.message_handler(commands=['start'])
def get_start_message(message):
    '''

    :param message: получает сообщение от пользователя
    :return: сообщение приветствия
    '''
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('/help')
    btn2 = types.KeyboardButton('/weather')
    btn3 = types.KeyboardButton('/add')
    markup.row(btn1, btn2, btn3)
    bot.send_message(message.from_user.id,
                        "Привет, {0.first_name}! Я, Даша-путешественница, помогу тебе провести незабываемое время в Москве! По команде: \n/help можно станцию метро\n/weather можно узнать о погоде в Москве\n/add ты можешь добавить места, которых нет в списке, чтобы поделиться своими впечатлениями, а мы их добавим в список".format(
                            message.from_user), reply_markup=markup)


@bot.message_handler(commands=['help'])
def get_help_message(message):
    '''
    :param message: получает сообщение от пользователя
    :return: вопрос
    '''
    bot.send_message(message.from_user.id,
                        "Какую станцию метро ты хочешь посетить сегодня?\nВыбирать можно абсолютно любую станцию, но есть одно условие- она должна находиться внутри кольцевой линии")
    bot.register_next_step_handler(message, get_station)


def get_station(message):
    '''
    Функция, получая станцию метро, выдает варианты развлечений
    :param message: сообщение от пользователя
    :return: варианы развлечений
    '''
    if message.text.lower() not in stations_data.keys():
        bot.send_message(message.from_user.id, text="Такой станции нет в списке, попробуй еще раз")
        bot.register_next_step_handler(message, get_station)
    else:
        keyboard = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data=f"{message.text.lower()},0")
        keyboard.add(but1)
        but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data=f"{message.text.lower()},1")
        keyboard.add(but2)
        but3 = types.InlineKeyboardButton(text='развлечения', callback_data=f"{message.text.lower()},2")
        keyboard.add(but3)
        bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                            reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call, bot=bot):
    '''
    Функция принимает выбранное место и выдает вариант ссылок на развлечения
    :param call: выбранное место
    :return: ссылку на развлечение
    '''
    station, type = call.data.split(',')
    bot.send_message(call.message.chat.id, text="Отличный выбор!")
    bot.send_message(call.message.chat.id, text=stations_data[station][int(type)])


@bot.message_handler(commands=['add'])
def get_add_message(message):
    '''
    Функция откликается на команду и задает пользователю вопрос
    :param message: получает команду /add
    :return: вопрос пользователю
    '''
    bot.send_message(message.chat.id, 'Ты посетил классное место и хочешь им поделиться? Напиши в сообщении отзыв:')
    bot.register_next_step_handler(message, add_review)


def add_review(message):
    '''
    Функция принимает текст от пользователя и заносит отзыв в таблицу
    :param message: сообщение от пользователя
    :return: заносит сообщение в таблицу
    '''
    db.add_review(message)


@bot.message_handler(content_types=['text'])
def handle_bad_message(message):
    ''' Ответ на непонятные сообщения '''
    if message.text not in ('/start', '/add', '/help', '/weather'):
        bot.send_message(message.chat.id, text='Я тебя не понимаю. Напиши /start.')

bot.polling(none_stop=True, interval=0)
