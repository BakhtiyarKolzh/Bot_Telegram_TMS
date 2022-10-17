#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import os.path
import sys
from multiprocessing import Lock
from pathlib import WindowsPath

from aiogram import types, executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsSenderContact
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentTypes
from aiogram.utils.callback_data import CallbackData

import authentication
import configure
import database
import path_manager

lock = asyncio.Lock()
mutex = Lock()

bot = Bot(token=(configure.config["token"]))
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.CRITICAL)

remove = types.ReplyKeyboardRemove()

users_start = authentication.config["ID"]  # последнее - id группы если бот что-то должен делать в группе
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")

########################################################################################################################

delegates = ['Выбор файлов', 'Выбрать все файлы', 'ОТМЕНА']
formats = ['DWG', 'NWC', 'PDF', 'IFC']
options = ['Стандартно', 'Без связей']
decides = ['ОК', 'ОТМЕНА']

########################################################################################################################
"""Output"""


class Action(StatesGroup):
    action = State()


calldata = CallbackData('cmd', 'user', 'name', 'amount')

activate = False


######################################################################################################################


async def create_keyboard_buttons(msg, button_names, answer: str, row=1, resize=True, one_time=True):
    if isinstance(button_names, list):
        await asyncio.sleep(0.125)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=resize, one_time_keyboard=one_time, row_width=row)
        for name in button_names:
            await asyncio.sleep(0.05)
            keyboard.insert(types.KeyboardButton(text=name))
        await msg.answer(text=answer, reply_markup=keyboard, protect_content=True)


async def create_inline_buttons(msg, user, directory):
    if isinstance(directory, str):
        paths = path_manager.get_result_rvt_path_list(directory)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if isinstance(paths, list):
            buttons = []
            for idx, path in enumerate(paths):
                filename, ext = os.path.splitext(WindowsPath(path).name)
                filename = filename.encode('cp1251', 'ignore').decode('cp1251')
                print(filename)
                if len(filename) < 35:
                    try:
                        number = f'{idx + 1}'
                        sequence = f'{number}.\t{filename}'
                        data = calldata.new(user=user, name=filename, amount=number)
                        buttons.append(types.InlineKeyboardButton(sequence, callback_data=data))
                    except Exception as e:
                        print(e.args)

            keyboard.add(*buttons)
            keyboard.get_current()
            await msg.answer(text="Проекты: ", reply_markup=keyboard, protect_content=True)

    return await create_keyboard_buttons(msg, options, 'Выберите опцию', 2)


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
async def command_start(msg: types.Message):
    global users_start
    async with lock:
        if msg.chat.id not in users_start:
            await msg.answer(text='У Вас нет прав на выполнение данной команды')
            await asyncio.sleep(15)
        else:
            try:
                await Action.action.set()
                await msg.answer(f"Добро пожаловать👋, {msg.from_user.first_name}")
                await create_keyboard_buttons(msg, ['Начать задание'], 'Выберите команду Начать задание')
            except Exception as e:
                print(e.args)


########################################################################################################################
"""Message handler Ok / cancel"""


@dp.message_handler(lambda msg: msg.text in decides, state=Action.action, content_types=ContentTypes.TEXT)
async def callback_decides_buttons(msg: types.Message, state: FSMContext):
    user = msg.from_user.first_name
    store = await state.get_data()
    async with lock:
        if msg.text == 'ОК':
            command = store[user]
            if isinstance(command, dict):
                if database.run_command(command):
                    numbers = sorted(command.get('numbers'))
                    output = ', '.join(str(num) for num in numbers)
                    await msg.answer(f"👌 Oтправлено на выполнения => " + output, reply_markup=remove)
            else:
                await msg.answer("❌ Повторите ввод данных", reply_markup=remove)
        try:
            store.pop(user)
            await asyncio.sleep(1.5)
            await state.update_data(store)
        except Exception as e:
            print(e.args)
    return await create_keyboard_buttons(msg, ['Начать задание'], 'Выберите команду Начать задание')


########################################################################################################################
"""Message handler other commands """


@dp.message_handler(lambda msg: len(msg.text), state=Action.action, content_types=ContentTypes.TEXT)
async def callback_other_buttons(msg: types.Message, state: FSMContext):
    user = msg.from_user.first_name
    store = await state.get_data()
    global activate
    activate = True
    input = msg.text
    print('Input\t' + input)

    if input == 'Начать задание':
        return await create_keyboard_buttons(msg, formats, 'Выберите формат для перевода данных:', 2)

    if input in formats and state:
        await state.set_data(update_store(user, store, {'control': input}))
        return await msg.answer("🗂 ВВЕДИТЕ ПУТЬ: ... ", reply_markup=remove)

    if input.__contains__('PROJECT') and state:
        if os.path.exists(os.path.realpath(input)):
            await state.set_data(update_store(user, store, {'directory': input}))
            return await create_keyboard_buttons(msg, delegates, 'Выберите нужную операцию', 3)
        else:
            await msg.answer("❌ Неправильный ввод данных")

    if input in delegates and state:
        directory = store[user].get('directory')
        if input == 'Выбор файлов' and directory:
            await state.set_data(update_store(user, store, {'numbers': []}))
            return await create_inline_buttons(msg, user, directory)
        elif input == 'Выбрать все файлы':
            await state.set_data(update_store(user, store, {'numbers': [0]}))
            return await create_keyboard_buttons(msg, options, 'Выберите опцию', 2)

    if input in options and state:
        await state.set_data(update_store(user, store, {'option': input}))
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

########################################################################################################################
########################################################################################################################
"""Database run"""

# @dp.message_handler()
# async def send_notice(data: dict):
#     for user in users_start:
#         control = data.get('control')
#         numbers = data.get('numbers')
#         parts = Path(os.path.realpath(data.get('directory'))).parts
#         msg = f'Запущен => {parts[1]}\t\t\t[{control}]\t{numbers}'
#         await bot.send_message(chat_id=user, text='🤖')
#         await bot.send_message(chat_id=user, text=msg)
#
##ASAA#ASAA
# async def database_run(dp):
#     while True:
#         global activate
#         global data_path
#         print(f'Activate => {activate}')
#         if not activate: await asyncio.sleep(300)
#         sequence = database.stream_read_json(data_path)
#         if not sequence: await close_bot(dp)
#         print(f'sequence => {sequence}')
#         if sequence and len(sequence):
#             session, command = sequence
#             if isinstance(command, dict):
#                 if database.run_command(command):
#                     await send_notice(command)
#
#
# async def on_startup(dp):
#     asyncio.create_task(database_run(dp))


if __name__ == '__main__':
    dp.bind_filter(IsSenderContact)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    executor.start_polling(dp, skip_updates=False, timeout=5)
