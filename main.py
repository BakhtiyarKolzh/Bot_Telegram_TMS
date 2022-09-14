#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os.path
import time
import os

from pathlib import WindowsPath
from aiogram import types, executor, Dispatcher, Bot

import authentication  #### Library for authentication
import configure  #### Library for Token
import path_manager
import database

bot = Bot(token=(configure.config["token"]))
dp = Dispatcher(bot)
users_start = authentication.config["ID"]  # последнее - id группы если бот что-то должен делать в группе
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")

########################################################################################################################

delegates = ['Выбор файлов', 'Выбрать все файлы', 'ОТМЕНА']
formats = ['DWG', 'NWC', 'PDF', 'IFC']
decides = ['ОК', 'ОТЛОЖИТЬ', 'ОТМЕНА']

########################################################################################################################

start, step_01, step_02, step_03 = False, False, False, False

########################################################################################################################
"""Output"""

count = 0
filenames = list()
indexes = list()
data = dict()
commands = list()
directory = None
control = None

"""
commands[0] = control
commands[1] = directory
commands[1:] = file index
action = action[user] = commands
data = data[count] = action
"""


########################################################################################################################
async def create_keyboard_buttons(message, button_names, answer=str(), row=1, resize=True, one_time=True):
    if isinstance(button_names, list):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=resize, one_time_keyboard=one_time, row_width=row)
        for name in button_names:
            keyboard.insert(types.KeyboardButton(text=name))
        await message.answer(answer, reply_markup=keyboard)


async def create_inline_buttons(message, directory):
    buttons = []
    global indexes
    indexes = list()
    global filenames
    filenames = list()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    paths = path_manager.get_result_rvt_path_list(directory)
    if isinstance(paths, list):
        for idx, path in enumerate(paths):
            filename, ext = os.path.splitext(WindowsPath(path).name)
            if len(filename) < 35:
                number = f'{idx + 1}'
                filename = filename.encode('cp1251', 'ignore').decode('cp1251')
                buttons.append(types.InlineKeyboardButton(f'{number}.\t{filename}', callback_data=number))
                filenames.append(filename)
                indexes.append(number)
                print(filename)

        keyboard.add(*buttons)
        keyboard.get_current()
        message = await message.answer("Выберите фаилы: ", reply_markup=keyboard)
        await create_keyboard_buttons(message, decides, 'Подтвердите операцию', 3)


async def reset(message):
    global indexes
    global start
    global step_01
    global step_02
    global step_03
    global commands
    commands = list()
    indexes, start, step_01, step_02, step_03 = list(), False, False, False, False
    await message.answer("Выход из задания")
    types.ReplyKeyboardRemove()
    await asyncio.sleep(1)
    print('RESET')
    return


########################################################################################################################
"""Start"""


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    global users_start
    types.ReplyKeyboardRemove()
    if message.chat.id not in users_start:
        await message.answer('У Вас нет прав на выполнение данной команды, обратитесь к администратору')
    else:
        welcome = f"Добро пожаловать👋, {message.from_user.first_name}"
        await bot.send_message(chat_id=message.from_user.id, text=welcome)
        await create_keyboard_buttons(message, ['Начать задание'], 'Выберите команду Начать задание')
        print('Начать задание')
        global start
        start = True


########################################################################################################################
"""Message handler"""


@dp.message_handler(lambda message: any(message.text))
async def callback_keyboard_buttons(message: types.Message):
    input = message.text
    global directory
    global delegates
    global count
    global start
    global step_01
    global step_02
    global step_03
    print(input)

    ### get formats
    if start and input == 'Начать задание':
        await create_keyboard_buttons(message, formats, 'Выберите формат для перевода данных:', 2)
        step_01 = True

    ### set control
    elif step_01 and input in formats:
        await message.answer("🗂 ВВЕДИТЕ ПУТЬ: ... ")
        commands.append(input)
        step_02 = True

    ### set directory path
    elif step_02 and input.__contains__('PROJECT'):
        directory = os.path.realpath(input)
        if os.path.exists(directory):
            await create_keyboard_buttons(message, delegates, 'Выберите нужную операцию', 3)
            commands.append(directory)
            step_03 = True
        else:
            await message.answer("❌ ОШИБКА ВВОДА❗❗❗")
            directory = None

    elif step_03 and input in delegates:
        if input == 'Выбор файлов':
            await create_inline_buttons(message, directory)
        elif input == 'Выбрать все файлы':
            await create_keyboard_buttons(message, decides, 'Подтвердите операцию', 3)
            commands.append(0)

    else:
        if all([step_01, step_02, step_03]) and input == 'ОК' and isinstance(data, dict):
            user_name = message.from_user.first_name.encode('cp1251', 'ignore').decode('cp1251')
            await message.answer("Задание отправлено в очередь выполнения 👌")
            data[count] = {user_name: commands}
            database.write_json_data(data_path, data)
            print(data.items())
            count += 1
        await reset(message)


########################################################################################################################
"""Callback inline buttons handler"""


@dp.callback_query_handler(lambda c: c.data in indexes)
async def callback_inline_buttons(call: types.callback_query):
    global filenames
    number = call.data
    for idx, filename in enumerate(filenames):
        if number == f'{idx + 1}':
            await bot.send_message(call.from_user.id, f'✅\tВыбран файл:\n{filename}')
            return commands.append(number)


########################################################################################################################
"""Database run"""


async def database_run():
    global data_path
    while True:
        print('database run')
        await asyncio.sleep(0.5)
        data_dict = database.deserialize_json_data(data_path)
        if not isinstance(data_dict, dict): await asyncio.sleep(1000)
        if isinstance(data_dict, dict):
            if len(data_dict):
                print("data is dict ")
                database.execute_commands(data_path)
                await asyncio.sleep(5)
            else:
                database.remove(data_path)


async def on_startup(x):
    asyncio.create_task(database_run())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, timeout=5, on_startup=on_startup)
