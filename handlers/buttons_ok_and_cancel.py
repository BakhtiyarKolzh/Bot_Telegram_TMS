#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import time

from aiogram import types, executor, Dispatcher, Bot
from create_bot import dp, bot, users_start, reply_kb, reply_km, controlId, directory, dictionary, flag, inline_kb, \
    inline_km, temp, data_path

import database
import path_manager
from pathlib import WindowsPath

from handlers.start_button import command_start
########################################################################################################################
########################################################################################################################

'''BUTTONS OK AND OTMENA'''

# @dp.message_handler(lambda message: message.text in ['Выбор файлов', 'Выбрать все файлы', 'Отложить операцию'])
async def menu_button_ok_and_cancel(message):
    global dictionary
    global controlId
    global directory
    global reply_km
    global reply_kb
    global flag

    if flag:
        markup = reply_km(resize_keyboard=True, one_time_keyboard=True)
        markup.add(reply_kb('ОК'), reply_kb('ОТМЕНА'))
        markup.one_time_keyboard = True

        await message.answer("Подтвердите выбранную операцию", reply_markup=markup)
        await call_back_ok_and_cancel(message)


# @dp.message_handler(lambda message: message.text in ['ОК', 'ОТМЕНА'])
async def call_back_ok_and_cancel(message: types.Message):
    msg = message.text
    global dictionary
    global controlId
    global directory
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

def register_handlers_for_ok_cancel(dp: Dispatcher):
    dp.register_message_handler(menu_button_ok_and_cancel,lambda message: message.text in
                                                                          ['Выбор файлов',
                                                                           'Выбрать все файлы',
                                                                           'Отложить операцию'])
    dp.register_message_handler(call_back_ok_and_cancel,lambda message: message.text in ['ОК', 'ОТМЕНА'])


