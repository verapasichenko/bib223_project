import telebot
from pyowm import OWM
from telebot import types
import sqlite3

bot = telebot.TeleBot('5847682014:AAFhiFUbNhxt-St2tzMGUqiFuEukCKElOPg')


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
    owm = OWM('4b4ba7fd4d10e6a206a383cc2bba05dc') #API
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    location = get_location(observation.location.lat, observation.location.lon)
    temperature = weather.temperature("celsius")
    return temperature, location


@bot.message_handler(commands=['weather'])
def get_user_text(message):
    '''
    Функция откликается на команду и задает вопрос пользователю
    :param message: сообщение пользователя в боте
    :return: погоду
    '''
    if message.text == '/weather':
        bot.send_message(message.from_user.id, "Введи название города: ")
        bot.register_next_step_handler(message, get_weather) #ждет сообщение пользователя и вызывает указанную функцию с аргументом message


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
def get_user_text(message):
    '''

    :param message: получает сообщение от пользователя
    :return: сообщение приветствия
    '''
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.KeyboardButton('/help')
        btn2 = types.KeyboardButton('/weather')
        btn3 = types.KeyboardButton('/add')
        markup.row(btn1, btn2, btn3)
        bot.send_message(message.from_user.id,
                         "Привет, {0.first_name}! Я, Даша-путешественница, помогу тебе провести незабываемое время в Москве! По команде: \n/help можно станцию метро\n/weather можно узнать о погоде в Москве\n/add ты можешь добавить места, которых нет в списке, чтобы поделиться своими впечатлениями, а мы их добавим в список".format(
                             message.from_user), reply_markup=markup)


@bot.message_handler(commands=['help'])
def get_text_messages1(message):
    '''
    :param message: получает сообщение от пользователя
    :return: вопрос
    '''
    if message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Какую станцию метро ты хочешь посетить сегодня?\nВыбирать можно абсолютно любую станцию, но есть одно условие- она должна находиться внутри кольцевой линии")

        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            '''
            Функция, получая станцию метро, выдает варианты развлечений
            :param message: сообщение от пользователя
            :return: варианы развлечений
            '''
            if message.text == "Комсомольская" or message.text == "комсомольская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but1")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but2")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but3")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Курская" or message.text == "курская" or message.text == "чкаловская" or message.text == "Чкаловская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but4")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but5")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but6")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Таганская" or message.text == "таганская" or message.text == "Марксистская" or message.text == "марксистская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but7")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but8")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but9")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Красные ворота" or message.text == "красные ворота":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but10")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but11")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but12")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Чистые пруды" or message.text == "чистые пруды" or message.text == "Тургеневская" or message.text == "тургеневская" or message.text == "Сретенский бульвар" or message.text == "сретенский бульвар":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but13")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but14")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but15")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Лубянка" or message.text == "лубянка" or message.text == "Кузнецкий Мост" or message.text == "кузнецкий мост" or message.text == "Кузнецкий мост":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but16")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but17")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but18")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Охотный Ряд" or message.text == "охотный ряд" or message.text == "Охотный ряд" or message.text == "Театральная" or message.text == "театральная" or message.text == "Площадь Революции" or message.text == "Площадь революции" or message.text == "площадь революции":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but19")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but20")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but21")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Арбатская" or message.text == "арбатская" or message.text == "Боровицкая" or message.text == "боровицкая" or message.text == "Александровский Сад" or message.text == "александровский сад" or message.text == "Александровский сад" or message.text == "Библиотека имени Ленина" or message.text == "библиотека имени Ленина":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but22")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but23")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but24")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Кропоткинская" or message.text == "кропоткинская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but25")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but26")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but27")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Маяковская" or message.text == "маяковская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but28")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but29")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but30")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Новокузнецкая" or message.text == "новокузнецкая" or message.text == "Третьяковская" or message.text == "третьяковская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but31")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but32")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='клубы', callback_data="but33")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Новослободская" or message.text == "новослободская" or message.text == "Менделеевская" or message.text == "менделеевская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but34")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but35")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but36")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Проспект мира" or message.text == "проспект мира" or message.text == "Сухаревская" or message.text == "сухаревская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but37")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but38")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but39")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Цветной бульвар" or message.text == "цветной бульвар" or message.text == "Трубная" or message.text == "трубная":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but40")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but41")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but42")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Баррикадная" or message.text == "баррикадная" or message.text == "Краснопресненская" or message.text == "краснопресненская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but43")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but44")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but45")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Серпуховская" or message.text == "серпуховская" or message.text == "Добрынинская" or message.text == "добрынинская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but46")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but47")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but48")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Полянка" or message.text == "полянка":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but49")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but50")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but51")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Смоленская" or message.text == "смоленская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but52")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but53")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but54")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Киевская" or message.text == "киевская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but55")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but56")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but57")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Парк культуры" or message.text == "парк культуры":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but58")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but59")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but60")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Павелецкая" or message.text == "павелецкая":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but61")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but62")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but63")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Белорусская" or message.text == "белорусская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but64")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but65")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but66")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)
            elif message.text == "Октябрьская" or message.text == "октябрьская":
                keyboard = types.InlineKeyboardMarkup()
                but1 = types.InlineKeyboardButton(text='бары & рестораны', callback_data="but67")
                keyboard.add(but1)
                but2 = types.InlineKeyboardButton(text='достопримечательности', callback_data="but68")
                keyboard.add(but2)
                but3 = types.InlineKeyboardButton(text='развлечения', callback_data="but69")
                keyboard.add(but3)
                bot.send_message(message.from_user.id, text='Отлично, теперь давай выберем, как ты хочешь развлечься',
                                 reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    '''
    Функция принимает выбранное место и выдает вариант ссылок на развлечения
    :param call: выбранное место
    :return: ссылку на развлечение
    '''
    if call.data == "but1":
        msg1 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4575760-Komsomol_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg1)
    if call.data == "but2":
        msg2 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d15266271-Metro_Station_Komsomolskaya-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg2)
    if call.data == "but3":
        msg3 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4575760-Komsomol_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg3)
    if call.data == "but4":
        msg4 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d9575877-Kurskaya-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg4)
    if call.data == "but5":
        msg5 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4575960-Kursk_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg5)
    if call.data == "but6":
        msg6 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4575960-Kursk_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg6)
    if call.data == "but7":
        msg7 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4577349-Taganka_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg7)
    if call.data == "but8":
        msg8 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d15276786-Taganskaya_Metro_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg8)
    if call.data == "but9":
        msg9 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4577349-Taganka_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg9)
    if call.data == "but10":
        msg10 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4575855-Red_Gates_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg10)
    if call.data == "but11":
        msg11 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4575855-Red_Gates_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg11)
    if call.data == "but12":
        msg12 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4575855-Red_Gates_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg12)
    if call.data == "but13":
        msg13 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/Restaurants-g298484-zfn15621306-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg13)
    if call.data == "but14":
        msg14 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/Attractions-g298484-Activities-zfn15621306-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg14)
    if call.data == "but15":
        msg15 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/Attractions-g298484-Activities-c56-zfn15621306-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg15)
    if call.data == "but16":
        msg16 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4576080-Lubyanka_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg16)
    if call.data == "but17":
        msg17 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576080-Lubyanka_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg17)
    if call.data == "but18":
        msg18 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576080-Lubyanka_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg18)
    if call.data == "but19":
        msg19 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d301484-Okhotny_Ryad-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg19)
    if call.data == "but20":
        msg20 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d301484-Okhotny_Ryad-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg20)
    if call.data == "but21":
        msg21 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576586-Bird_Market_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg21)
    if call.data == "but22":
        msg22 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d9575849-Arbatskaya-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg22)
    if call.data == "but23":
        msg23 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/Attractions-g298484-Activities-zfn15621305-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg23)
    if call.data == "but24":
        msg24 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/Attractions-g298484-Activities-c56-zfn8707996-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg24)
    if call.data == "but25":
        msg25 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4575878-Kropotkinskaya_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg25)
    if call.data == "but26":
        msg26 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4575878-Kropotkinskaya_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg26)
    if call.data == "but27":
        msg27 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4575878-Kropotkinskaya_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg27)
    if call.data == "but28":
        msg28 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d14200972-Mayakovskaya_Metro_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg28)
    if call.data == "but29":
        msg29 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576179-Mayakovsky_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg29)
    if call.data == "but30":
        msg30 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576179-Mayakovsky_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg30)
    if call.data == "but31":
        msg31 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4576428-Novokuznetsk_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg31)
    if call.data == "but32":
        msg32 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576428-Novokuznetsk_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg32)
    if call.data == "but33":
        msg33 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576428-Novokuznetsk_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg33)
    if call.data == "but34":
        msg34 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4576442-Novoslobodskaya_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg34)
    if call.data == "but35":
        msg35 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576442-Novoslobodskaya_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg35)
    if call.data == "but36":
        msg36 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576442-Novoslobodskaya_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg36)
    if call.data == "but37":
        msg37 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d15276772-oa30-Prospekt_Mira_Metro_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg37)
    if call.data == "but38":
        msg38 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576854-Peace_Avenue_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg38)
    if call.data == "but39":
        msg39 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576854-Peace_Avenue_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg39)
    if call.data == "but40":
        msg40 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4577692-Flower_Boulevard_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg40)
    if call.data == "but41":
        msg41 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4577692-Flower_Boulevard_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg41)
    if call.data == "but42":
        msg42 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4577692-Flower_Boulevard_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg42)
    if call.data == "but43":
        msg43 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4574639-Barricade_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg43)
    if call.data == "but44":
        msg44 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4574639-Barricade_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg44)
    if call.data == "but45":
        msg45 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4574639-Barricade_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg45)
    if call.data == "but46":
        msg46 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4577133-Serpukhovskaya_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg46)
    if call.data == "but47":
        msg47 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4577133-Serpukhovskaya_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg47)
    if call.data == "but48":
        msg48 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4577133-Serpukhovskaya_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg48)
    if call.data == "but49":
        msg49 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4576769-Polyanka_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg49)
    if call.data == "but50":
        msg50 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576769-Polyanka_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg50)
    if call.data == "but51":
        msg51 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576769-Polyanka_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg51)
    if call.data == "but52":
        msg52 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d9575848-oa30-Smolenskaya-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg52)
    if call.data == "but53":
        msg53 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/Attraction_Review-g298484-d15276777-Reviews-Smolenskaya_Metro_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg53)
    if call.data == "but54":
        msg54 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/Attraction_Review-g298484-d15276777-Reviews-Smolenskaya_Metro_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg54)
    if call.data == "but55":
        msg55 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d15266252-Kiyevskaya_Metro_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg55)
    if call.data == "but56":
        msg56 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4575644-Kiev_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg56)
    if call.data == "but57":
        msg57 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4575644-Kiev_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg57)
    if call.data == "but58":
        msg58 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4576605-Culture_Park_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg58)
    if call.data == "but59":
        msg59 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576605-Culture_Park_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg59)
    if call.data == "but60":
        msg60 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4576605-Culture_Park_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg60)
    if call.data == "but61":
        msg61 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d7914834-Paveletskiy_Train_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg61)
    if call.data == "but62":
        msg62 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d7914834-Paveletskiy_Train_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg62)
    if call.data == "but63":
        msg63 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d7914834-Paveletskiy_Train_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg63)
    if call.data == "but64":
        msg64 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4574704-Belorussia_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg64)
    if call.data == "but65":
        msg65 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4574704-Belorussia_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg65)
    if call.data == "but66":
        msg66 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/AttractionsNear-g298484-d4574704-Belorussia_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg66)
    if call.data == "but67":
        msg67 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/RestaurantsNear-g298484-d4576528-October_Station-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg67)
    if call.data == "but68":
        msg68 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/Attraction_Review-g298484-d15324909-Reviews-Metro_Station_Oktyabrskaya-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg68)
    if call.data == "but69":
        msg69 = "перейди по ссылке, чтобы увидеть места\nhttps://www.tripadvisor.ru/Attraction_Review-g298484-d15324909-Reviews-Metro_Station_Oktyabrskaya-Moscow_Central_Russia.html"
        bot.send_message(call.message.chat.id, msg69)



conn = sqlite3.connect('/Users/ep/Desktop/project/database1.db', check_same_thread=False)
cursor = conn.cursor()#передаются заполнители



@bot.message_handler(commands=['add'])
def start_message(message):
    '''
    Функция откликается на команду и задает пользователю вопрос
    :param message: получает команду /add
    :return: вопрос пользователю
    '''
    bot.send_message(message.chat.id, 'Ты посетил классное место и хочешь им поделиться? Напиши в сообщении отзыв!\nПожалуйста, начни свой отзыв с \ add, чтобы нам было легче фильтровать сообщения:)')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''
    Функция принимает текст от пользователя и заносит отзыв в таблицу
    :param message: сообщение от пользователя
    :return: заносит сообщение в таблицу
    '''
    cursor.execute('INSERT INTO database (id_review, review) VALUES (?, ?)',
                   (message.from_user.id, message.text))

    conn.commit()

bot.polling(none_stop=True, interval=0)
