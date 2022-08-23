#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
import os.path

from aiogram import types, executor, Dispatcher, Bot

import configure  #### Library for Token
#                                       INPUT DATES
########################################################################################################################
import database

bot = Bot(token=(configure.config["token"]))
dp = Dispatcher(bot)

########################################################################################################################
########################################################################################################################
'''   START TELEGRAM    '''


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):

    chat_id = message.chat.id
    welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
    await bot.send_message(chat_id=chat_id, text=welcome, parse_mode='html')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_task = types.KeyboardButton('Начать задание')

    markup.add(button_task)
    await bot.send_message(chat_id, "Выберите команду Начать задание", reply_markup=markup)

    return


@dp.message_handler(content_types=['text'])
async def start_task(message: types.Message):
    if message.chat.type == "private":
        if message.text == "Начать задание":
            await call_button_batch(message)


########################################################################################################################
########################################################################################################################
@dp.message_handler(content_types=['text'])
async def call_button_batch(message: types.Message):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_DWG = types.KeyboardButton('DWG')
    button_NWC = types.KeyboardButton('NWC')
    button_PDF = types.KeyboardButton('PDF')

    markup.add(button_DWG, button_NWC, button_PDF)

    await bot.send_message(chat_id, text="Выберите формат для перевода данных:", reply_markup=markup)

    return


@dp.message_handler(content_types=['text'])
async def callback(message: types.Message):
    global controlId
    if message.text == "DWG":
        controlId = "DWG"
        dir_for_DWG = bot.send_message(message.chat.id, "Введите путь для DWG")
        # bot.register_next_step_handler(dir_for_DWG, user_answer_Format)
        print(controlId)

    elif message.text == "NWC":
        controlId = "NWC"
        dir_for_NWC = bot.send_message(message.chat.id, "Введите путь для NWC")
        # bot.register_next_step_handler(dir_for_NWC, user_answer_Format)
        print(controlId)

    elif message.text == "PDF":
        controlId = "PDF"
        dir_for_PDF = bot.send_message(message.chat.id, 'Введите путь для PDF')
        await user_answer_Format(message)
        print(controlId)

    else:
        controlId = None
        result = bot.send_message(message.chat.id, "ОШИБКА ВВОДА!!! ВЫБЕРИТЕ ПРАВИЛЬНУЮ КНОПКУ!!!")
        # bot.register_next_step_handler(result, callback)

    return


########################################################################################################################
########################################################################################################################


async def user_answer_Format(message: types.Message):
    global directory
    directory = os.path.realpath(message.text)
    if os.path.exists(directory):
        # menu_for_button(message)
        print("exist")

    else:
        directory = None
        await bot.send_message(message.chat.id, "ОШИБКА ПУТИ!!! ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
        await user_answer_Format(message)
        # bot.register_next_step_handler(result, user_answer_Format)

    return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
