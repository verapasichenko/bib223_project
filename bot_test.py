import pytest

from pytest_mock import mocker
from unittest.mock import Mock
import telebot
from telebot import types

import bot

def test_bot_start(mocker):
    '''Test bot start message'''
    # replace tested method with mock
    telebot.TeleBot.send_message = Mock()
    # create mock message
    message = Mock()
    message.from_user.id = 0
    message.from_user.first_name = 'Test'
    message.text = '/start'
    # replace markup with mock
    types.ReplyKeyboardMarkup = Mock()
    types.ReplyKeyboardMarkup.row = Mock()
    types.KeyboardButton = Mock()
    # create mock markup
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('/help')
    btn2 = types.KeyboardButton('/weather')
    btn3 = types.KeyboardButton('/add')
    markup.row(btn1, btn2, btn3)
    # call tested method
    bot.get_start_message(message)
    bot.bot.send_message.assert_called_once_with(message.from_user.id,
                         "Привет, {0.first_name}! Я, Даша-путешественница, помогу тебе провести незабываемое время в Москве! По команде: \n/help можно станцию метро\n/weather можно узнать о погоде в Москве\n/add ты можешь добавить места, которых нет в списке, чтобы поделиться своими впечатлениями, а мы их добавим в список".format(
                             message.from_user), reply_markup=markup)


def test_bot_help(mocker):
    '''Test bot help message'''
    # replace tested method with mock
    telebot.TeleBot.send_message = Mock()
    telebot.TeleBot.register_next_step_handler = Mock()
    # create mock message
    message = Mock()
    message.from_user.id = 0
    message.from_user.first_name = 'Test'
    message.text = '/help'
    # call tested method
    bot.get_help_message(message)
    bot.bot.send_message.assert_called_once_with(message.from_user.id,
                        "Какую станцию метро ты хочешь посетить сегодня?\nВыбирать можно абсолютно любую станцию, но есть одно условие- она должна находиться внутри кольцевой линии")
    bot.bot.register_next_step_handler.assert_called_once_with(message, bot.get_station)


def test_bot_weather(mocker):
    '''Test bot weather message'''
    # replace tested method with mock
    telebot.TeleBot.send_message = Mock()
    telebot.TeleBot.register_next_step_handler = Mock()
    # create mock message
    message = Mock()
    message.from_user.id = 0
    message.from_user.first_name = 'Test'
    message.text = '/weather'
    # call tested method
    bot.get_weather_message(message)
    bot.bot.send_message.assert_called_once_with(message.from_user.id, "Введи название города: ")
    bot.bot.register_next_step_handler.assert_called_once_with(message, bot.get_weather)


def test_bot_add(mocker):
    '''Test bot add message'''
    # replace tested method with mock
    telebot.TeleBot.send_message = Mock()
    telebot.TeleBot.register_next_step_handler = Mock()
    # create mock message
    message = Mock()
    message.from_user.id = 0
    message.from_user.first_name = 'Test'
    message.text = '/add'
    # call tested method
    bot.get_add_message(message)
    bot.bot.send_message.assert_called_once_with(message.chat.id, 'Ты посетил классное место и хочешь им поделиться? Напиши в сообщении отзыв:')
    bot.bot.register_next_step_handler.assert_called_once_with(message, bot.add_review)