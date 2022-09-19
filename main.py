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
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsSenderContact
from aiogram.utils.callback_data import CallbackData

import authentication  #### Library for authentication
import configure  #### Library for Token
import database
import path_manager

bot = Bot(token=(configure.config["token"]))
dp = Dispatcher(bot, storage=MemoryStorage())
ContentText = types.ContentTypes.TEXT
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


class Action(StatesGroup):
    action = State()


calldata = CallbackData('cmd', 'user', 'name', 'amount')

"""
data = { time.time(): action }
action[user] = commands 
commands[0] = control
commands[1] = directory
commands[1:] = index + 1
"""


######################################################################################################################


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
    print('RESET')
    if any([step_01, step_02, step_03]):
        # current_state = await state.get_state()
        # if current_state not is None: await state.finish()
        start, step_01, step_02, step_03 = False, False, False, False
        await message.answer(text='🤖', reply_markup=types.ReplyKeyboardRemove())
        await dp.wait_closed()
        await bot.close()
        commands = list()


async def timeout(message):
    try:
        await asyncio.sleep(300)
    finally:
        return await reset(message)


def update_store(user: str, store: dict, input: dict):
    with mutex:
        output = store.get(user)
        if isinstance(output, dict):
            output.update(input)
        else:
            output = input
        store[user] = output
        return store


########################################################################################################################
"""Start"""


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    global users_start
    types.ReplyKeyboardRemove()
    if message.chat.id not in users_start:
        await message.answer(text='У Вас нет прав на выполнение данной команды')
    else:
        global start
        start = True
        await Action.action.set()
        welcome = f"Добро пожаловать👋, {message.from_user.first_name}"
        await bot.send_message(chat_id=message.from_user.id, text=welcome)
        await create_keyboard_buttons(message, ['Начать задание'], 'Выберите команду Начать задание')


########################################################################################################################
"""Message handler"""


@dp.message_handler(IsSenderContact, lambda msg: any(msg.text), state=Action.action, content_types=ContentText)
async def callback_keyboard_buttons(msg: types.Message, state: FSMContext):
    user = msg.from_user.first_name.encode('cp1251', 'ignore').decode('cp1251')
    store = await state.get_data()
    input = msg.text
    print(input)

    if input == 'Начать задание':
        return await create_keyboard_buttons(msg, formats, 'Выберите формат для перевода данных:', 2)

    if input in formats:
        await state.set_data(update_store(user, store, {'control': input}))
        return await msg.answer("🗂 ВВЕДИТЕ ПУТЬ: ... ")

    if input.__contains__('PROJECT'):
        if os.path.exists(os.path.realpath(input)):
            await state.set_data(update_store(user, store, {'directory': input}))
            await create_keyboard_buttons(msg, delegates, 'Выберите нужную операцию', 3)
        else:
            await msg.answer("❌ ОШИБКА ВВОДА❗❗❗")

    if input in delegates:
        if input == 'Выбор файлов':
            await state.set_data(update_store(user, store, {'numbers': list()}))
            return await create_inline_buttons(msg, input)
        elif input == 'Выбрать все файлы':
            await state.set_data(update_store(user, store, {'numbers': [0]}))
            await create_keyboard_buttons(msg, decides, 'Подтвердите операцию', 3)

    if input in decides:
        print(store.items())
        if isinstance(store, dict) and input == 'ОК':
            await msg.answer("Задание отправлено на выполнения 👌", reply_markup=types.ReplyKeyboardRemove())
            database.update_json_data(data_path, store)
            await reset(msg)

    # if input == 'ОК':
    #     return await bot.send_message(msg.chat.id, '🌟', reply_markup=types.ReplyKeyboardRemove())
    #
    # if input == 'ОТМЕНА':
    #     return await create_keyboard_buttons(msg, ['Начать задание'], 'Выберите команду Начать задание')


########################################################################################################################
"""Callback inline buttons handler"""


@dp.callback_query_handler(lambda callback_query: True, state=Action.action)
async def callback_inline_buttons(query: types.inline_query, state: FSMContext):
    callback = query.data
    store = await state.get_data()
    if isinstance(callback, str) and callback.startswith('cmd'):
        cmd, user, filename, amount = callback.split(":", maxsplit=3)
        if query.from_user.first_name == user:
            numbers = list()
            data = store[user]
            numbers.append(int(amount))
            numbers.extend(data['numbers'])
            await state.set_data(update_store(user, store, {'numbers': numbers}))
            await bot.send_message(query.from_user.id, f'✅\tВыбран файл:\n{filename}')
            return print(numbers)


########################################################################################################################
"""Database run"""


async def database_run():
    while True:
        global data_path
        await asyncio.sleep(100)
        print('database activate')
        # cdata = database.stream_read_json(data_path)
        # if cdata and isinstance(cdata, tuple): database.run_command(cdata)


async def on_startup(x):
    asyncio.create_task(database_run())


if __name__ == '__main__':
    dp.bind_filter(IsSenderContact)
    executor.start_polling(dp, skip_updates=False, timeout=5, on_startup=on_startup)
