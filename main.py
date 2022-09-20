#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import os.path
import sys
import time
from multiprocessing import Lock
from pathlib import WindowsPath

from aiogram import types, executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsSenderContact
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
from aiogram.types import ContentTypes

import authentication
import configure
import database
import path_manager

mutex = Lock()

bot = Bot(token=(configure.config["token"]))
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.CRITICAL)

markup = types.ReplyKeyboardRemove()

users_start = authentication.config["ID"]  # последнее - id группы если бот что-то должен делать в группе
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")

########################################################################################################################

delegates = ['Выбор файлов', 'Выбрать все файлы', 'ОТМЕНА']
formats = ['DWG', 'NWC', 'PDF', 'IFC']
decides = ['ОК', 'ОТМЕНА']

########################################################################################################################
"""Output"""


class Action(StatesGroup):
    action = State()


calldata = CallbackData('cmd', 'user', 'name', 'amount')

activate = False

"""
data = { time.time(): action }
"""


######################################################################################################################


async def create_keyboard_buttons(message, button_names, answer=str(), row=1, resize=True, one_time=True):
    if isinstance(button_names, list):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=resize, one_time_keyboard=one_time, row_width=row)
        for name in button_names:
            keyboard.insert(types.KeyboardButton(text=name))
        await bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=keyboard, protect_content=True)


async def create_inline_buttons(message, user, directory):
    if isinstance(directory, str) and directory.__contains__('PROJECT'):
        paths = path_manager.get_result_rvt_path_list(directory)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if isinstance(paths, list):
            buttons = []
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


def update_store(user: str, store: dict, input: dict):
    with mutex:
        output = store.get(user)
        if isinstance(output, dict):
            output.update(input)
        else:
            output = input
        store[user] = output
        return store


def close():
    global activate
    dp.wait_closed()
    activate = False
    print('close')
    bot.close()


########################################################################################################################
"""Start"""


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    global users_start
    with mutex:
        await asyncio.sleep(0.5)
        if message.chat.id not in users_start:
            await message.answer(text='У Вас нет прав на выполнение данной команды')
        else:
            try:
                await Action.action.set()
                await message.answer(f"Добро пожаловать👋, {message.from_user.first_name}")
                await create_keyboard_buttons(message, ['Начать задание'], 'Выберите команду Начать задание')
            except Exception as e:
                print(e.args)


########################################################################################################################
"""Message handler Ok / cancel"""


@dp.message_handler(commands=decides, state=Action.action, content_types=ContentTypes.TEXT)
async def callback_decides_buttons(msg: types.Message, state: FSMContext):
    if input == 'ОК':
        store = await state.get_data()
        user = msg.from_user.first_name
        data = store[user]
        if isinstance(data, dict):
            numbers = data.get('numbers')
            output = '№'.join(sorted(numbers))
            database.update_json_data(data_path, {f'{round(time.time())}-' + user: data})
            await msg.answer(f"Oтправлено на выполнения {output} 👌", reply_markup=markup)
            try:
                store.pop(user)
                print(store.items())
                await state.update_data(store)
            except Exception as e:
                print(e.args)
        else:
            await msg.answer("❌ Повторите ввод данных", reply_markup=markup)

    await create_keyboard_buttons(msg, ['Начать задание'], 'Выберите команду Начать задание')


########################################################################################################################
"""Message handler other commands """


@dp.message_handler(lambda msg: any(msg.text), state=Action.action, content_types=ContentTypes.TEXT)
async def callback_other_buttons(msg: types.Message, state: FSMContext):
    global activate
    activate = True
    input = msg.text
    print(input)

    if input == 'Начать задание':
        return await create_keyboard_buttons(msg, formats, 'Выберите формат для перевода данных:', 2)

    if input in formats and state:
        store, user = await state.get_data(), msg.from_user.first_name
        await state.set_data(update_store(user, store, {'control': input}))
        return await msg.answer("🗂 ВВЕДИТЕ ПУТЬ: ... ", reply_markup=markup)

    if input.__contains__('PROJECT') and state:
        if os.path.exists(os.path.realpath(input)):
            store, user = await state.get_data(), msg.from_user.first_name
            await state.set_data(update_store(user, store, {'directory': input}))
            return await create_keyboard_buttons(msg, delegates, 'Выберите нужную операцию', 3)
        else:
            await msg.answer("❌ Неправильный ввод данных")

    if input in delegates and state:
        store = await state.get_data()
        user = msg.from_user.first_name
        directory = store[user].get('directory')
        if input == 'Выбор файлов' and directory:
            await create_inline_buttons(msg, user, directory)
            return await state.set_data(update_store(user, store, {'numbers': list()}))
        elif input == 'Выбрать все файлы':
            await state.set_data(update_store(user, store, {'numbers': [0]}))
            return await create_keyboard_buttons(msg, decides, 'Подтвердите операцию', 3)


########################################################################################################################
"""Callback inline buttons handler"""


@dp.callback_query_handler(lambda query: query.data.startswith('cmd'), state=Action.action)
async def callback_inline_buttons(query: types.inline_query, state: FSMContext):
    cmd, user, filename, amount = query.data.split(":", maxsplit=3)
    if query.from_user.first_name == user:
        store = await state.get_data()
        numbers = list()
        data = store[user]
        numbers.append(int(amount))
        numbers.extend(data['numbers'])
        await state.set_data(update_store(user, store, {'numbers': numbers}))
        await bot.send_message(query.from_user.id, f'✅\tВыбран файл:\n{filename}')
        return print(numbers)


########################################################################################################################
"""Database run"""


def generator(data_path):
    while True:
        global activate
        sequence = database.stream_read_json(data_path)
        if not sequence and not activate: close()
        if sequence and len(sequence):
            session, command = sequence
            yield database.run_command(command)


async def database_run():
    global activate
    global data_path
    await asyncio.sleep(30)
    print(f'Activate => {activate}')
    if activate: generator(data_path)
    if not activate: await asyncio.sleep(60)


async def on_startup(x):
    asyncio.create_task(database_run())


if __name__ == '__main__':
    dp.bind_filter(IsSenderContact)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    executor.start_polling(dp, skip_updates=False, timeout=5, on_startup=on_startup)
