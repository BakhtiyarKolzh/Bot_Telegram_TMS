#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import os
import os.path
import time

from pathlib import WindowsPath
from aiogram import types, executor, Dispatcher, Bot


import database
import path_manager

import authentication  #### Library for authentication
import configure  #### Library for Token

########################################################################################################################
########################################################################################################################

bot = Bot(token=(configure.config["token"]))
dp = Dispatcher(bot)
users_start = authentication.config["ID"]  # последнее - id группы если бот что-то должен делать в группе
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")

start = False
directory = str()
controlId = str()
dictionary = dict()

reply_km = types.ReplyKeyboardMarkup
reply_kb = types.KeyboardButton
inline_km = types.InlineKeyboardMarkup
inline_kb = types.InlineKeyboardButton

flag= False
temp = list()

########################################################################################################################
########################################################################################################################

'''   BOT PROTECTION    '''


@dp.message_handler(lambda message: message.chat.id not in users_start, commands=['start'])
async def protection_id(message: types.Message):
    await message.answer('У Вас нет прав на выполнение данной команды, обратитесь к администратору')


########################################################################################################################
########################################################################################################################

'''   START TELEGRAM    '''


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    global dictionary
    global controlId
    global directory
    global controlId
    global reply_km
    global reply_kb
    chat_id = message.from_user.id

    welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
    await bot.send_message(chat_id=chat_id, text=welcome, parse_mode='html')
    markup = reply_km(resize_keyboard=True, one_time_keyboard=True)
    markup.add(reply_kb(text='Начать задание'))
    await message.answer("Выберите команду Начать задание", reply_markup=markup)
    print('Начать задание')
    user_id = message.from_user.id
    print(user_id)



########################################################################################################################
########################################################################################################################

''' НАЧАТЬ ЗАДАНИЕ '''


@dp.message_handler(lambda message: message.text == 'Начать задание')
async def call_back_start_to_format(message: types.Message):
    global start
    global reply_km
    global reply_kb
    global controlId
    flag = True
    markup = reply_km(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    markup.add(reply_kb(text='DWG'), reply_kb(text='NWC'), reply_kb(text='PDF'), reply_kb(text='IFC'))
    await message.answer("Выберите формат для перевода данных:", reply_markup=markup)
    print("Выберите формат для перевода данных:")



@dp.message_handler(lambda message: message.text in ['DWG', 'NWC', 'PDF', 'IFC'])
async def call_back_format(message: types.Message):
    global start
    print(flag)
    if flag:
        await message.answer("Введите путь:")
        global controlId
        controlId = message.text
        print(controlId)


########################################################################################################################
########################################################################################################################

'''ВЫБОР ФАЙЛОВ, ВЫБРАТЬ ВСЕ ФАЙЛЫ, ОТОЛОЖИТЬ ОПЕРАЦИЮ '''


@dp.message_handler(lambda message: os.path.exists(os.path.realpath(message.text)))
async def menu_for_button(message: types.Message):
    global start
    global reply_km
    global reply_kb
    global directory
    directory = message.text
    print(message.text)
    if flag:
        markup = reply_km(resize_keyboard=True, one_time_keyboard=True)
        markup.add((reply_kb(text='Выбор файлов')),
                   (reply_kb(text='Выбрать все файлы')),
                   (reply_kb(text='Отложить операцию')))
        await message.answer("Выберите нужную операцию", reply_markup=markup)
        print("Выберите нужную операцию")


# @dp.message_handler(lambda message: len(message.text) > 15 and not os.path.exists(os.path.realpath(message.text)))
# async def test_for_button(message: types.Message):
#     await message.answer("MISTAKE")
#     print(message.text)


@dp.message_handler(lambda message: message.text in ['Выбор файлов', 'Выбрать все файлы', 'Отложить операцию'])
async def call_back_menu(message: types.Message):
    msg = message.text
    global start
    global dictionary
    global directory
    await menu_button_ok_and_cancel(message)
    if flag:
        if msg == "Выбор файлов":
            print("Выбор файлов")
            await create_inline_buttons(message)

        elif msg == "Выбрать все файлы":
            # dictionary =
            database.save_command_data(data_path, directory, controlId, dictionary)
            print("Выбрать все файлы")


        elif msg == "Отложить операцию":
            print("Отложить операцию")


########################################################################################################################
########################################################################################################################

'''Inline buttons '''


async def create_inline_buttons(message):
    global temp
    global inline_km
    global inline_kb
    time.sleep(0.5)
    if directory:
        buttons = []
        temp = list()
        keyboard = inline_km(row_width=1)
        paths = path_manager.get_result_rvt_path_list(directory)
        if isinstance(paths, list):
            for idx, path in enumerate(paths):
                filename, ext = os.path.splitext(WindowsPath(path).name)
                buttons.append(inline_kb(f'{idx + 1}.\t{filename}', callback_data=filename))
                temp.append(filename)

            keyboard.add(*buttons)
            keyboard.get_current()
            await message.answer("Выбрать:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data in temp)
async def call_inline_buttons(call: types.callback_query):
    global dictionary
    if any(call.data):
        filename = str(call.data)
        user_id = call.from_user.id
        await bot.send_message(call.from_user.id, f'✅ \tВыбран файл:\n{filename} ')
        vals = dictionary.get(user_id)
        if vals and isinstance(vals, list):
            vals.append(filename)


        # значение = list cmd
        # ключ = userId

        print(filename)




########################################################################################################################
########################################################################################################################
'''BUTTONS OK AND OTMENA'''

@dp.message_handler(lambda message: message.text in ['Выбор файлов', 'Выбрать все файлы', 'Отложить операцию'])
async def menu_button_ok_and_cancel(message):
    global dictionary
    global controlId
    global directory
    global reply_km
    global reply_kb
    global start

    if flag:
        markup = reply_km(resize_keyboard=True, one_time_keyboard=True)
        markup.add(reply_kb('ОК'), reply_kb('ОТМЕНА'))
        markup.one_time_keyboard = True

        await message.answer("Подтвердите выбранную операцию", reply_markup=markup)
        await call_back_ok_and_cancel(message)


@dp.message_handler(lambda message: message.text in ['ОК', 'ОТМЕНА'])
async def call_back_ok_and_cancel(message: types.Message):
    msg = message.text
    global dictionary
    global controlId
    global directory
    global start
    if flag:
        if msg == 'ОК':
            print('ОК')
            await command_start(message)
            return True

        elif msg == 'ОТМЕНА':
            print('ОТМЕНА')
            await command_start(message)
            return True


########################################################################################################################
########################################################################################################################
#
async def database_run():
    while True:
        print('database run')
        await asyncio.sleep(1000)
        await database.run()

        # for user_id in range(100):
        #     print('отправил')
        #     await database.run()
        #     print('database')


async def on_startup(x):
    asyncio.create_task(database_run())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, timeout=5, on_startup=on_startup)

# --------------------------------------------------OUT ----------------------------------------------------------------
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=False, timeout=1)
