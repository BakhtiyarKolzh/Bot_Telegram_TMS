#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
import os.path
import time
from multiprocessing import Lock
from pathlib import WindowsPath

from aiogram import types, executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import IsSenderContact
from aiogram.utils.callback_data import CallbackData

import authentication  #### Library for authentication
import configure  #### Library for Token
import database
import path_manager

bot = Bot(token=(configure.config["token"]))
dp = Dispatcher(bot, storage=MemoryStorage())
mutex = Lock()

users_start = authentication.config["ID"]  # последнее - id группы если бот что-то должен делать в группе
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")

########################################################################################################################

delegates = ['Выбор файлов', 'Выбрать все файлы', 'ОТМЕНА']
formats = ['DWG', 'NWC', 'PDF', 'IFC']
decides = ['ОК', 'ОТМЕНА']

########################################################################################################################

start, step_01, step_02, step_03 = False, False, False, False

########################################################################################################################
"""Output"""

commands = list()

"""
commands[0] = control
commands[1] = directory
commands[1:] = file index
action = action[user] = commands
data = data[count] = action
"""

########################################################################################################################


calldata = CallbackData('cmd', 'user', 'name', 'amount')


########################################################################################################################


async def create_keyboard_buttons(message, button_names, answer=str(), row=1, resize=True, one_time=True):
    if isinstance(button_names, list):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=resize, one_time_keyboard=one_time, row_width=row)
        for name in button_names:
            keyboard.insert(types.KeyboardButton(text=name))
        await bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=keyboard, protect_content=True)


async def create_inline_buttons(message, directory):
    buttons = []
    user = message.from_user.first_name
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    paths = path_manager.get_result_rvt_path_list(directory)
    if isinstance(paths, list):
        for idx, path in enumerate(paths):
            filename, ext = os.path.splitext(WindowsPath(path).name)
            filename = filename.encode('cp1251', 'ignore').decode('cp1251')
            if len(filename) < 35:
                number = f'{idx + 1}'
                sequence = f'{number}.\t{filename}'
                buttons.append(types.InlineKeyboardButton(sequence, callback_data=calldata.new(user=user,
                                                                                               name=filename,
                                                                                               amount=number)))
        keyboard.add(*buttons)
        keyboard.get_current()
        await message.answer(text="Проекты: ", reply_markup=keyboard, protect_content=True)
        await create_keyboard_buttons(message, decides, 'Подтвердите операцию', 3)


async def reset(message):
    global start
    global step_01
    global step_02
    global step_03
    global commands
    commands = list()
    start, step_01, step_02, step_03 = False, False, False, False
    await message.answer(text='🤖', reply_markup=types.ReplyKeyboardRemove())
    await dp.wait_closed()
    await bot.close()
    print('RESET')
    return


########################################################################################################################
"""Start"""


@dp.message_handler(commands=['start'], state=None)
async def command_start(message: types.Message):
    global users_start
    types.ReplyKeyboardRemove()
    if message.chat.id not in users_start:
        await message.answer(text='У Вас нет прав на выполнение данной команды')
    else:
        welcome = f"Добро пожаловать👋, {message.from_user.first_name}"
        await bot.send_message(chat_id=message.from_user.id, text=welcome)
        await create_keyboard_buttons(message, ['Начать задание'], 'Выберите команду Начать задание')
        print('Начать задание')
        global start
        start = True


########################################################################################################################
"""Message handler"""


@dp.message_handler(IsSenderContact, lambda msg: any(msg.text) and len(msg.text), content_types=types.ContentTypes.TEXT)
async def callback_keyboard_buttons(msg: types.Message):
    input = msg.text
    global directory
    global delegates
    global start
    global step_01
    global step_02
    global step_03
    print(input)

    ### get formats
    if start and input == 'Начать задание':
        await create_keyboard_buttons(msg, formats, 'Выберите формат для перевода данных:', 2)
        step_01 = True

    ### set control
    elif step_01 and input in formats:
        # 1 append control
        step_02 = True
        control = input
        commands.append(control)
        await msg.answer("🗂 ВВЕДИТЕ ПУТЬ: ... ")

    ### set directory path
    elif step_02 and input.__contains__('PROJECT'):
        directory = os.path.realpath(input)
        if os.path.exists(directory):
            # 2 append directory
            step_03 = True
            commands.append(directory)
            await create_keyboard_buttons(msg, delegates, 'Выберите нужную операцию', 3)
        else:
            await msg.answer("❌ ОШИБКА ВВОДА❗❗❗")
            directory = None

    elif step_03 and input in delegates:
        if input == 'Выбор файлов':
            await create_inline_buttons(msg, directory)
        elif input == 'Выбрать все файлы':
            await create_keyboard_buttons(msg, decides, 'Подтвердите операцию', 3)
            commands.append(0)

    if all([step_01, step_02, step_03]) and input == 'ОК' and len(commands):
        user_name = msg.from_user.first_name.encode('cp1251', 'ignore').decode('cp1251')
        await msg.answer("Задание отправлено в очередь выполнения 👌", reply_markup=types.ReplyKeyboardRemove())
        data = {round(time.time()): {user_name: commands}}
        database.write_json_data(data_path, data)
        return await reset(msg)

    if not all([step_01, step_02, step_03]) and input == 'ОК':
        return await bot.send_message(msg.chat.id, '🌟', reply_markup=types.ReplyKeyboardRemove())

    if input == 'ОТМЕНА':
        print('123')
        return await create_keyboard_buttons(msg, ['Начать задание'], 'Выберите команду Начать задание')

    if any([step_01, step_02, step_03]):
        try:
            await asyncio.sleep(300)
        finally:
            return await reset(msg)


########################################################################################################################
"""Callback inline buttons handler"""


@dp.callback_query_handler(lambda callback_query: True)
async def callback_inline_buttons(query: types.inline_query):
    callback = query.data
    if isinstance(callback, str) and callback.startswith('cmd'):
        cmd, user, filename, amount = callback.split(":", maxsplit=3)
        await bot.send_message(query.from_user.id, f'✅\tВыбран файл:\n{filename}')
        commands.append(int(amount))
        return print(amount)


########################################################################################################################
"""Database run"""


async def database_run():
    while True:
        global data_path
        print('run database')
        await asyncio.sleep(300)
        action = database.stream_read_json(data_path)
        if action and isinstance(action, dict):
            await database.run_command(action)


async def on_startup(x):
    asyncio.create_task(database_run())


if __name__ == '__main__':
    dp.bind_filter(IsSenderContact)
    executor.start_polling(dp, skip_updates=False, timeout=5, on_startup=on_startup)
