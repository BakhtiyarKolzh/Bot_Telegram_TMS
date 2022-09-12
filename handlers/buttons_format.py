#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path
import time

from aiogram import types, executor, Dispatcher, Bot
from create_bot import dp, bot, users_start, reply_kb, reply_km, controlId, directory, dictionary, flag, inline_kb, \
    inline_km, temp, data_path
from handlers.button_inline_call import create_inline_buttons
from handlers.buttons_ok_and_cancel import menu_button_ok_and_cancel

import database
import path_manager
from pathlib import WindowsPath
########################################################################################################################
########################################################################################################################

''' НАЧАТЬ ЗАДАНИЕ '''

########################################################################################################################

# @dp.message_handler(lambda message: message.text == 'Начать задание')
async def call_back_start_to_format(message: types.Message):
    global flag
    global reply_km
    global reply_kb
    global controlId
    flag = True
    markup = reply_km(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    markup.add(reply_kb(text='DWG'), reply_kb(text='NWC'), reply_kb(text='PDF'), reply_kb(text='IFC'))
    await message.answer("Выберите формат для перевода данных:", reply_markup=markup)
    print("Выберите формат для перевода данных:")


# @dp.message_handler(lambda message: message.text in ['DWG', 'NWC', 'PDF', 'IFC'])
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

########################################################################################################################

# @dp.message_handler(lambda message: os.path.exists(os.path.realpath(message.text)))
async def menu_for_button(message: types.Message):
    global flag
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


# @dp.message_handler(lambda message: message.text in ['Выбор файлов', 'Выбрать все файлы', 'Отложить операцию'])
async def call_back_menu(message: types.Message):
    msg = message.text
    global flag
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

def register_handlers_for_format(dp: Dispatcher):
    dp.register_message_handler(call_back_start_to_format,lambda message: message.text == 'Начать задание')

    dp.register_message_handler(call_back_format,lambda message: message.text in ['DWG', 'NWC', 'PDF', 'IFC'])

    dp.register_message_handler(menu_for_button, lambda message: os.path.exists(os.path.realpath(message.text)))

    dp.register_message_handler(call_back_menu, lambda message: message.text in ['Выбор файлов',
                                                                                 'Выбрать все файлы',
                                                                                 'Отложить операцию'])