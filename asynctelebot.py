#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import time
from pathlib import WindowsPath

import telebot
from telebot import types

import authentication  #### Library Protect ID
import configure  #### Library for Token
import database
import path_manager


import asyncio

import aiogram

from aiogram import types, executor, Dispatcher,Bot
#                                       INPUT DATES
########################################################################################################################


bot = telebot.TeleBot(configure.config["token"])
users_start = authentication.config["ID"]  # последнее - id группы если бот что-то должен делать в группе
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")

directory = None
controlId = None
commands = list()


########################################################################################################################

########################################################################################################################

'''   START TELEGRAM    '''


@bot.message_handler(commands=['start'])
async def start(message):
    global commands
    global controlId
    global directory
    commands, controlId, directory = list(), None, None
    welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
    await bot.send_message(message.chat.id, welcome, parse_mode='html')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_task = types.KeyboardButton('Начать задание')

    markup.add(button_task)
    await bot.send_message(message.chat.id, "Выберите команду Начать задание", reply_markup=markup)

    return


@bot.message_handler(content_types=['text'])
async def start_task(message):
    if message.chat.type == "private":
        if message.text == "Начать задание":
            call_button_batch(message)

    return

