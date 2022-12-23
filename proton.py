import telebot
from pyowm import OWM
from telebot import types
from Token import BotToken
import random
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
    mgr = owm.weather_manager()#возвращаем объект для получения погоды
    observation = mgr.weather_at_place(city)#назначаем где нам нужно получить погоду
    weather = observation.weather#получаем саму погоду, используя свойство
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
    btn4 = types.KeyboardButton('/gor')

    markup.row(btn1, btn2, btn3, btn4)
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


@bot.callback_query_handler(func=lambda call: True)#принимает анонимную функциюи возвращает True
def callback_worker(call):
    '''
    Функция принимает выбранное место и выдает вариант ссылок на развлечения
    :param call: выбранное место
    :return: ссылку на развлечение
    '''
    station, type = call.data.split(',')#возвращаем список станций и ссылок через запятую
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

first = ["Сегодня — идеальный день для новых начинаний.","Оптимальный день для того, чтобы решиться на смелый поступок!","Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.","Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.","Плодотворный день для того, чтобы разобраться с накопившимися делами."]
second = ["Но помните, что даже в этом случае нужно не забывать про","Если поедете за город, заранее подумайте про","Те, кто сегодня нацелен выполнить множество дел, должны помнить про","Если у вас упадок сил, обратите внимание на","Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"]
second_add = ["отношения с друзьями и близкими.","работу и деловые вопросы, которые могут так некстати помешать планам.","себя и своё здоровье, иначе к вечеру возможен полный раздрай.","бытовые вопросы — особенно те, которые вы не доделали вчера.","отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."]
third = ["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.","Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.","Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.","Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.","Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты."]
# Метод, который получает сообщения и обрабатывает их
@bot.message_handler(commands=['gor'])
def get_gor_message(message):
    # Если написали «Привет»
    if message.text == "/gor":
        # Пишем приветствие
        bot.send_message(message.from_user.id, "Привет, сейчас я расскажу тебе гороскоп на сегодня.")
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого знака зодиака
        key_oven = types.InlineKeyboardButton(text='Овен', callback_data='zodiac')
        # И добавляем кнопку на экран
        keyboard.add(key_oven)
        key_telec = types.InlineKeyboardButton(text='Телец', callback_data='zodiac')
        keyboard.add(key_telec)
        key_bliznecy = types.InlineKeyboardButton(text='Близнецы', callback_data='zodiac')
        keyboard.add(key_bliznecy)
        key_rak = types.InlineKeyboardButton(text='Рак', callback_data='zodiac')
        keyboard.add(key_rak)
        key_lev = types.InlineKeyboardButton(text='Лев', callback_data='zodiac')
        keyboard.add(key_lev)
        key_deva = types.InlineKeyboardButton(text='Дева', callback_data='zodiac')
        keyboard.add(key_deva)
        key_vesy = types.InlineKeyboardButton(text='Весы', callback_data='zodiac')
        keyboard.add(key_vesy)
        key_scorpion = types.InlineKeyboardButton(text='Скорпион', callback_data='zodiac')
        keyboard.add(key_scorpion)
        key_strelec = types.InlineKeyboardButton(text='Стрелец', callback_data='zodiac')
        keyboard.add(key_strelec)
        key_kozerog = types.InlineKeyboardButton(text='Козерог', callback_data='zodiac')
        keyboard.add(key_kozerog)
        key_vodoley = types.InlineKeyboardButton(text='Водолей', callback_data='zodiac')
        keyboard.add(key_vodoley)
        key_ryby = types.InlineKeyboardButton(text='Рыбы', callback_data='zodiac')
        keyboard.add(key_ryby)
        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Выбери свой знак зодиака', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker1(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data1 == "zodiac":
        # Формируем гороскоп
        msg1 = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third)
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg1)

@bot.message_handler(content_types=['text'])
def handle_bad_message(message):
    ''' Ответ на непонятные сообщения '''
    if message.text not in ('/start', '/add', '/help', '/weather', '/gor'):
        bot.send_message(message.chat.id, text='Я тебя не понимаю. Напиши /start.')

bot.polling(none_stop=True, interval=0)
