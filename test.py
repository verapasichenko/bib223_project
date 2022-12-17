import unittest
from unittest.mock import AsyncMock

import main

class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_something(self):
        message = AsyncMock()
        await main.hello(message)
        message.answer.assrt_called_with('Привет, {0.first_name}! Я, Даша-путешественница, помогу тебе провести незабываемое время в Москве! По команде: \n/help можно станцию метро\n/weather можно узнать о погоде в Москве\n/add ты можешь добавить места, которых нет в списке, чтобы поделиться своими впечатлениями, а мы их добавим в список'.format(
                             message.from_user), reply_markup=markup)

class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_something(self):
        message = AsyncMock()
        await main.weather(message)
        message.answer.assrt_called_with('Введи название города: ')

if __name__ == '__main__':
    unittest.main()
    
