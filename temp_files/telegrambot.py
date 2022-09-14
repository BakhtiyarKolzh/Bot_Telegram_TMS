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

#                                       INPUT DATES
########################################################################################################################


bot = telebot.TeleBot(configure.config["token"])
users_start = authentication.config["ID"]  # последнее - id группы если бот что-то должен делать в группе
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../data_file.json")

directory = None
control = None
dictionary = list()


########################################################################################################################
#                                    --Bot Protection---

@bot.message_handler(func=lambda message: message.chat.id not in users_start, commands=['start'])
def protection_id(message):
    bot.send_message(message.chat.id, 'У Вас нет прав на выполнение данной команды, обратитесь к администратору')
    return


########################################################################################################################

'''   START TELEGRAM    '''


@bot.message_handler(commands=['start'])
def start(message):
    global dictionary
    global control
    global directory
    commands, controlId, directory = list(), None, None
    welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
    bot.send_message(message.chat.id, welcome, parse_mode='html')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_task = types.KeyboardButton('Начать задание')

    markup.add(button_task)
    bot.send_message(message.chat.id, "Выберите команду Начать задание", reply_markup=markup)

    return


@bot.message_handler(content_types=['text'])
def start_task(message):
    if message.chat.type == "private":
        if message.text == "Начать задание":
            call_button_batch(message)

    return


########################################################################################################################

'''   CREATE BUTTON ---- DWG,NWC,PDF   '''


#######################################################################################################################

@bot.message_handler(content_types=['text'])
def call_button_batch(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_DWG = types.KeyboardButton('DWG')
    button_NWC = types.KeyboardButton('NWC')
    button_PDF = types.KeyboardButton('PDF')

    markup.add(button_DWG, button_NWC, button_PDF)

    result = bot.send_message(message.chat.id, "Выберите формат для перевода данных:", reply_markup=markup)
    bot.register_next_step_handler(result, callback)

    return


@bot.message_handler(content_types=['text'])
def callback(message):
    global control
    if message.text == "DWG":
        controlId = "DWG"
        dir_for_DWG = bot.send_message(message.chat.id, "Введите путь для DWG")
        bot.register_next_step_handler(dir_for_DWG, user_answer_Format)
        print(controlId)

    elif message.text == "NWC":
        controlId = "NWC"
        dir_for_NWC = bot.send_message(message.chat.id, "Введите путь для NWC")
        bot.register_next_step_handler(dir_for_NWC, user_answer_Format)
        print(controlId)

    elif message.text == "PDF":
        controlId = "PDF"
        dir_for_PDF = bot.send_message(message.chat.id, 'Введите путь для PDF')
        bot.register_next_step_handler(dir_for_PDF, user_answer_Format)
        print(controlId)

    else:
        controlId = None
        result = bot.send_message(message.chat.id, "ОШИБКА ВВОДА!!! ВЫБЕРИТЕ ПРАВИЛЬНУЮ КНОПКУ!!!")
        bot.register_next_step_handler(result, callback)

    return


########################################################################################################################
########################################################################################################################


def user_answer_Format(message):
    global directory
    directory = os.path.realpath(message.text)
    if os.path.exists(directory):
        menu_for_button(message)
        print("exist")

    else:
        directory = None
        result = bot.send_message(message.chat.id, "ОШИБКА ПУТИ!!! ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
        bot.register_next_step_handler(result, user_answer_Format)

    return


########################################################################################################################
########################################################################################################################

'''Menu_for_button'''


@bot.message_handler(content_types=['text'])
def menu_for_button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_select_files = types.KeyboardButton('Выбор файлов')
    button_all_files = types.KeyboardButton('Выбрать все файлы')
    button_close = types.KeyboardButton('ОТМЕНА')

    markup.add(button_select_files, button_all_files, button_close)

    result = bot.send_message(message.chat.id, "Выберите нужную операцию", reply_markup=markup)
    bot.register_next_step_handler(result, select_button)

    return


def select_button(message):
    global dictionary
    if message.text == "Выбор файлов":
        cmd_select_inline(message, directory)
        print("Выбор файлов")

    elif message.text == "Выбрать все файлы":
        commands.append(0)
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        database.save_command_data(data_path, directory, control, commands)
        bot.send_message(message.chat.id, " 00000 ")
        print("Выбрать все файлы")
        print(commands)
        start(message)

    elif message.text == "ОТМЕНА":
        print("ОТМЕНА")
        start(message)

    else:
        result = bot.send_message(message.chat.id, "ОШИБКА ВВОДА!!! ВЫБЕРИТЕ ПРАВИЛЬНУЮ КНОПКУ!!!")
        bot.register_next_step_handler(result, select_button)

    return


########################################################################################################################
########################################################################################################################

'''SELECT A SECTION --- def'''

hide = types.InlineKeyboardButton


def cmd_select_inline(message, project_path):
    buttons = []
    time.sleep(0.5)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    paths = path_manager.get_result_rvt_path_list(project_path)
    for idx, path in enumerate(paths):
        name, ext = os.path.splitext(WindowsPath(path).name)
        buttons.append(types.InlineKeyboardButton(name, callback_data=idx + 1))

    keyboard.add(*buttons)
    bot.clear_step_handler(message)
    bot.send_message(message.chat.id, "Выбрать: ", reply_markup=keyboard)
    call_button_ok_and_cancel(message)

    return


@bot.callback_query_handler(func=lambda call: True)
def call_for_cmd_line(call):
    global dictionary
    if any(call.data):
        number = call.data
        number = int(number) if number.isdigit() else 0
        commands.append(number)
        print(number)

    return


########################################################################################################################
########################################################################################################################
@bot.message_handler(content_types=['text'])
def call_button_ok_and_cancel(message):
    global dictionary
    global control
    global directory
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('ОК'), types.KeyboardButton('ОТМЕНА'))
    markup.one_time_keyboard = True
    bot.send_message(message.chat.id, "Введите данные", reply_markup=markup)
    msg = message.text
    print(msg)

    if msg == 'ОК':
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        database.save_command_data(data_path, directory, controlId, commands)
        bot.send_message(message.chat.id, "Файлы были запущены, возвращаю обратно в меню")
        print(commands)
        start(message)
        return True

    elif msg == 'ОТМЕНА':
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.send_message(message.chat.id, "Отменено")
        start(message)
        return True

    else:
        bot.register_next_step_handler(message, call_button_ok_and_cancel)


# --------------------------------------------------OUT -----------------------------------------------------------------
def run_polling():
    bot.infinity_polling(none_stop=True, interval=0.5, timeout=1)
    return
########################################################################################################################

#                                                -SAVES-
