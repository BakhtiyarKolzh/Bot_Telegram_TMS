#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

flag = False
directory = None
controlId = None
commands = list()

reply_km = types.ReplyKeyboardMarkup
reply_kb = types.KeyboardButton
inline_km = types.InlineKeyboardMarkup
inline_kb = types.InlineKeyboardButton

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
    global commands
    global controlId
    global directory
    global controlId
    global reply_km
    global reply_kb
    chat_id = message.from_user.id
    commands, controlId, directory = list(), None, None

    welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
    await bot.send_message(chat_id=chat_id, text=welcome, parse_mode='html')
    markup = reply_km(resize_keyboard=True)
    markup.add(reply_kb(text='Начать задание'))
    await message.answer("Выберите команду Начать задание", reply_markup=markup)
    print('Начать задание')


########################################################################################################################
########################################################################################################################

''' НАЧАТЬ ЗАДАНИЕ '''


@dp.message_handler(lambda message: message.text == 'Начать задание')
async def call_back_start_to_format(message: types.Message):
    global flag
    global reply_km
    global reply_kb
    flag = True
    markup = reply_km(resize_keyboard=True)
    markup.add(reply_kb(text='DWG'), reply_kb(text='NWC'), reply_kb(text='PDF'))
    await message.answer("Выберите формат для перевода данных:", reply_markup=markup)
    print("Выберите формат для перевода данных:")


@dp.message_handler(lambda message: message.text in ['DWG', 'NWC', 'PDF'])
async def call_back_format(message: types.Message):
    global flag
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
    global flag
    global reply_km
    global reply_kb
    print(message.text)
    if flag:
        markup = reply_km(resize_keyboard=True)
        markup.add((reply_kb(text='Выбор файлов')), (reply_kb(text='Выбрать все файлы')),
                   (reply_kb(text='Отложить операцию')))
        await message.answer("Выберите нужную операцию", reply_markup=markup)
        print("Выберите нужную операцию")
        await call_back_menu(message)


@dp.message_handler(lambda message: len(message.text) > 15 and not os.path.exists(os.path.realpath(message.text)))
async def test_for_button(message: types.Message):
    # await menu_button_ok_and_cancel(message)
    await message.answer("MISTAKE")
    print(message.text)


@dp.message_handler(lambda message: message.text in ['Выбор файлов', 'Выбрать все файлы', 'Отложить операцию'])
async def call_back_menu(message: types.Message):
    msg = message.text
    global flag
    if flag:
        if msg == "Выбор файлов":
            print("Выбор файлов")
            await menu_button_ok_and_cancel(message)
            # await cmd_select_inline(message, directory)
            # await menu_button_ok_and_cancel(message)

        elif msg == "Выбрать все файлы":
            print("Выбрать все файлы")
            # await menu_button_ok_and_cancel(message)

        elif msg == "Отложить операцию":
            print("Отложить операцию")
            # await menu_button_ok_and_cancel(message)


########################################################################################################################
########################################################################################################################

'''SELECT A SECTION --- def'''

hide = types.InlineKeyboardButton

@dp.message_handler(lambda message: message.text in ['Выбор файлов', 'Выбрать все файлы', 'Отложить операцию'])
async def cmd_select_inline(message: types.Message, project_path):
    buttons = []
    time.sleep(0.5)
    keyboard = inline_km(row_width=1)
    paths = path_manager.get_result_rvt_path_list(project_path)
    for idx, path in enumerate(paths):
        name, ext = os.path.splitext(WindowsPath(path).name)
        buttons.append(inline_kb(name, callback_data=idx + 1 or 'btn'))


    keyboard.add(*buttons)
    await message.answer("Выбрать: ", reply_markup=keyboard)
    await menu_button_ok_and_cancel(message)


@dp.callback_query_handler(lambda c: c.data == 'btn')
async def call_for_cmd_line(callback_query: types.CallbackQuery):
    global commands
    if any(call.data):
        number = call.data
        number = int(number) if number.isdigit() else 0
        commands.append(number)
        print(number)






########################################################################################################################
########################################################################################################################

'''BUTTONS OK AND OTMENA'''


@dp.message_handler(lambda message: message.text in ['Выбор файлов', 'Выбрать все файлы', 'Отложить операцию'])
async def menu_button_ok_and_cancel(message):
    global commands
    global controlId
    global directory
    global reply_km
    global reply_kb
    global flag
    if flag:
        markup = reply_km(resize_keyboard=True)
        markup.add(reply_kb('ОК'), reply_kb('ОТМЕНА'))
        markup.one_time_keyboard = True

        await message.answer("Подтвердите выбранную операцию", reply_markup=markup)
        await call_back_ok_and_cancel(message)


@dp.message_handler(lambda message: message.text in ['ОК', 'ОТМЕНА'])
async def call_back_ok_and_cancel(message: types.Message):
    msg = message.text
    global flag
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
# #
# async def is_enabled():
#     print('запускаю цикл')
#     while True:
#         print('отправляю сообщения')
#         for user_id in range(100):
#             await asyncio.sleep(1)
#             print('отправил')
#             await asyncio.sleep(1)
#             print('1111')
#         print('жду')
#         await asyncio.sleep(10)
#
#
#
# async def on_startup(x):
#     asyncio.create_task(is_enabled())


# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True, timeout=1, on_startup=on_startup)

# --------------------------------------------------OUT ----------------------------------------------------------------

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, timeout=1)
