#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiogram import types, executor, Dispatcher, Bot
from create_bot import dp,bot,users_start,reply_kb,reply_km,controlId,directory,dictionary,flag,inline_kb,inline_km,temp
from handlers import admin
import create_bot


########################################################################################################################
########################################################################################################################

'''   BOT PROTECTION    '''


# @dp.message_handler(lambda message: message.chat.id not in users_start, commands=['start'])
async def protection_id(message: types.Message):
    await message.answer('У Вас нет прав на выполнение данной команды, обратитесь к администратору')


'''   START TELEGRAM    '''

# @dp.message_handler(commands=['start'])
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

def register_handlers_for_start(dp: Dispatcher):
    dp.register_message_handler(protection_id,lambda message: message.chat.id not in users_start, commands=['start'])
    dp.register_message_handler(command_start,commands=['start'])




