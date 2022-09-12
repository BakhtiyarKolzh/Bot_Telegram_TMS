#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os.path
import time
import os

from pathlib import WindowsPath
from aiogram import types, executor, Dispatcher, Bot, filters

import authentication  #### Library for authentication
import configure  #### Library for Token
import path_manager
import database

bot = Bot(token=(configure.config["token"]))
dp = Dispatcher(bot)
users_start = authentication.config["ID"]  # последнее - id группы если бот что-то должен делать в группе
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")

########################################################################################################################

actions = ['Выбор файлов', 'Выбрать все файлы', 'Отложить операцию']
formats = ['DWG', 'NWC', 'PDF', 'IFC']
decides = ['ОК', 'ОТМЕНА']

########################################################################################################################

temp = list()
start = False
step_01, step_02, step_03 = False, False, False


########################################################################################################################


async def create_keyboard_buttons(message, button_names, answer=str(), row=1, resize=True, one_time=True):
    if isinstance(button_names, list):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=resize, one_time_keyboard=one_time, row_width=row)
        for name in button_names:
            keyboard.insert(types.KeyboardButton(text=name))
        await message.answer(answer, reply_markup=keyboard)


async def create_inline_buttons(message, directory):
    global temp
    btn = []
    temp = list()
    next_action = ['ОК', 'ОТМЕНА']
    answer = 'И подтвердите операцию'
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    paths = path_manager.get_result_rvt_path_list(directory)
    if isinstance(paths, list):
        for idx, path in enumerate(paths):
            filename, ext = os.path.splitext(WindowsPath(path).name)
            btn.append(types.InlineKeyboardButton(f'{idx + 1}.\t{filename}', callback_data=filename))
            temp.append(filename)

        keyboard.add(*btn)
        keyboard.get_current()
        message = await message.answer("Выберите фаилы: ", reply_markup=keyboard)
        await create_keyboard_buttons(message, next_action, answer, 2)


########################################################################################################################
"""Output"""

directory = str()
controlId = str()
dictionary = dict()

########################################################################################################################
"""Start"""


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    global users_start
    if message.chat.id not in users_start:
        await message.answer('У Вас нет прав на выполнение данной команды, обратитесь к администратору')
    else:
        welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
        await bot.send_message(chat_id=message.from_user.id, text=welcome, parse_mode='html')
        await create_keyboard_buttons(message, ['Начать задание'], 'Выберите команду Начать задание')
        print('Начать задание')
        global start
        start = True


########################################################################################################################
"""Message handler"""


@dp.message_handler(lambda message: any(message.text))
async def callback_keyboard_buttons(message: types.Message):
    input = message.text

    global controlId
    global directory
    global actions
    print(input)

    global start
    global step_01
    global step_02
    global step_03

    if start and input == 'Начать задание':
        await create_keyboard_buttons(message, formats, 'Выберите формат для перевода данных:', 2)
        step_01 = True

    elif step_01 and input in formats:
        await message.answer("ВВЕДИТЕ ПУТЬ: ")
        step_02 = True

    elif step_02 and input.__contains__('PROJECT'):
        path = os.path.realpath(input)
        if os.path.exists(path):
            await create_keyboard_buttons(message, actions, 'Выберите нужную операцию', 3)
            directory = path
            step_03 = True
        else:
            await message.answer("MISTAKE")

    elif step_03 and input in actions:
        if input == 'Выбор файлов':
            await create_inline_buttons(message, directory)
        else:
            await create_keyboard_buttons(message, decides, 'Подтвердите операцию', 2)

    else:
        start = False
        await asyncio.sleep(1)
        types.ReplyKeyboardRemove()
        await message.answer("Выход из задания")
        step_01, step_02, step_03 = False, False, False


########################################################################################################################
"""Callback inline buttons handler"""


@dp.callback_query_handler(lambda c: c.data in temp)
async def callback_inline_buttons(call: types.callback_query):
    global dictionary
    filename = str(call.data)
    user_id = call.from_user.id
    await bot.send_message(call.from_user.id, f'✅ \tВыбран файл:\n{filename} ')
    vals = dictionary.get(user_id)
    if vals and isinstance(vals, list):
        vals.append(filename)


########################################################################################################################
"""Database run"""


async def database_run():
    while True:
        print('database run')
        await asyncio.sleep(1000)
        await database.run()


async def on_startup(x):
    asyncio.create_task(database_run())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, timeout=5, on_startup=on_startup)
