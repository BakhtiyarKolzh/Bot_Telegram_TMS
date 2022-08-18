#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path

import telebot
from telebot import types

import RevitSortFiles
import authentication  #### Library Protect ID
#    My libraries
import configure  #### Library for Token

# import database


#                                       INPUT DATES
########################################################################################################################
bot = telebot.TeleBot(configure.config["token"])
users_start = authentication.config["ID"]  # последнее - id группы если бот что-то должен делать в группе
database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")
########################################################################################################################


url_BIM360 = "https://insight.b360.eu.autodesk.com/accounts/bf8a62b2-d479-4c2e-8523-103a1de299ea/projects/7a15c326-d421-4efb-98cd-fa817eb95f96/home"
url_Google_Sheets = "https://docs.google.com/spreadsheets/d/1tbvsFXLMzuKftQu9LV9jQ4FD6ik_l5yP-XRrhQsCrvw/edit?usp=sharing"
url_Yandex_Disk = "https://disk.yandex.kz/client/disk?utm_source=main_stripe_big_more"
url_BI_Design = "https://design.bi.group/"
url_Google_Docs = "https://docs.google.com/spreadsheets/d/1WesHLNRMiR5OOTFm0-t-VFiDfdix1NWCtgoqZq52nFI/edit#gid=0"

########################################################################################################################

filepath = ''
controlId = ''
commands = list()


########################################################################################################################
#                                    --Bot Protection---

@bot.message_handler(func=lambda message: message.chat.id not in users_start, commands=['start', "url"])
def protection_id(message):
    bot.send_message(message.chat.id, 'У Вас нет прав на выполнение данной команды, обратитесь к администратору')
    return


########################################################################################################################

'''   START TELEGRAM    '''


########################################################################################################################
@bot.message_handler(commands=['start'])
def start(message):
    welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
    bot.send_message(message.chat.id, welcome, parse_mode='html')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_task = types.KeyboardButton('Начать задание')
    # button_url = types.KeyboardButton('URL')

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
    global controlId
    if message.text == "DWG":
        controlId = "DWG"
        dir_for_DWG = bot.send_message(message.chat.id, "Введите путь для DWG")
        bot.register_next_step_handler(dir_for_DWG, user_answer_for_DWG)

    elif message.text == "NWC":
        controlId = "NWC"
        dir_for_NWC = bot.send_message(message.chat.id, "Введите путь для NWC")
        bot.register_next_step_handler(dir_for_NWC, user_answer_for_NWC)

    elif message.text == "PDF":
        controlId = "PDF"
        dir_for_PDF = bot.send_message(message.chat.id, 'Введите путь для PDF')
        bot.register_next_step_handler(dir_for_PDF, user_answer_for_PDF)

    else:
        controlId = None
        result = bot.send_message(message.chat.id, "ОШИБКА ВВОДА!!! ВЫБЕРИТЕ ПРАВИЛЬНУЮ КНОПКУ!!!")
        bot.register_next_step_handler(result, callback)

    return


########################################################################################################################
########################################################################################################################

'''DWG CONVERTER'''

########################################################################################################################
# def user_answer_for_DWG(message):
#     open_dir = str(message.text)
#     if os.path.exists(open_dir):
#
#         #  SCAN DIR FOR REVIT
#         # listPaths = SortRevitNameFiles()
#
#         filepath = os.path.join(open_dir + "\ExportToDWG.bat")
#         path_launch(filepath, message, "DWG")
#         print("DWG")
#         result = bot.send_message(message.chat.id, "Выберите файлы:")
#         # bot.register_next_step_handler(result, func_for_keyboard)
#     else:
#         bot.send_message(message.chat.id, "ОШИБКА ПУТИ!!! ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
#     return
#

########################################################################################################################

'''Navisworks CONVERTER'''


########################################################################################################################
#
# def user_answer_for_NWC(message):
#     open_dir = str(message.text)
#
#     if os.path.exists(open_dir):
#
#         #  SCAN DIR FOR REVIT
#         # listPaths = SortRevitNameFiles()
#
#         filepath = os.path.join(open_dir + "\ExportToNavisworks.bat")
#         path_launch(filepath, message, "NWC")
#         print("NWC")
#         result = bot.send_message(message.chat.id, "Выберите файлы:")
#         # bot.register_next_step_handler(result, func_for_keyboard)
#     else:
#         bot.send_message(message.chat.id, "ОШИБКА ПУТИ!!! ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
#     return
#
#
# ########################################################################################################################
# '''PDF CONVERTER'''  # TEST Version ##########     Use only it

def user_answer_for_PDF(message):
    global filepath
    input_path = os.path.realpath(message.text)
    if os.path.exists(input_path):
        filepath = input_path
        listPaths = RevitSortFiles.get_result_rvt_path_list(input_path)
        filepath = os.path.join(input_path + "\ExportToPDF.bat")
        path_launch(filepath, message, "PDF")
        print("PDF")

        menu_for_button(message)


    else:
        filepath = None
        result = bot.send_message(message.chat.id, "ОШИБКА ПУТИ!!! ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
        bot.register_next_step_handler(result, user_answer_for_PDF)

    return


########################################################################################################################
########################################################################################################################

'''Start def'''


########################################################################################################################

def path_launch(filepath, message, call):
    if (os.path.exists(filepath)):
        # os.startfile(filepath)
        print("Старт")
        # bot.send_message(message.chat.id, f"Процесс выгрузки в {call} запущен")
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
    if message.text == "Выбор файлов":
        canceled = bool(call_button_ok_and_otmena(message))
        while (True):
            if canceled: return
            bot.register_next_step_handler(message, select_files)

    elif message.text == "Выбрать все файлы":
        print("Выбрать все файлы")
        select_all_files(message)

    elif message.text == "ОТМЕНА":
        print("ОТМЕНА")

    else:
        result = bot.send_message(message.chat.id, "ОШИБКА ВВОДА!!! ВЫБЕРИТЕ ПРАВИЛЬНУЮ КНОПКУ!!!")
        bot.register_next_step_handler(result, select_button)

    return


########################################################################################################################
########################################################################################################################

'''SELECT A SECTION --- def'''


def select_files(message):
    global commands
    commands = list()  # int types
    number = message.text

    if number != 0:
        print(number)
        commands.append(number)

    number = 0 if isinstance(number, str) and not number.isdigit() else number
    number = number if isinstance(number, int) else int(number)

    return number





########################################################################################################################
########################################################################################################################
'''SELECT All files--- def'''


def select_all_files(message):
    global commands
    result = None
    commands = list()  # int types
    number = 0
    ok = call_button_ok_and_otmena(message)
    if bool(ok): return
    number = 0 if isinstance(number, str) and not number.isdigit() else number
    number = int(number) if isinstance(number, str) else number

    print(number)

    bot.register_next_step_handler(message, start)

    return


########################################################################################################################
########################################################################################################################
@bot.message_handler(content_types=['text'])
def call_button_ok_and_otmena(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_name_ok = types.KeyboardButton('ОК')
    button_name_close = types.KeyboardButton('ОТМЕНА')

    markup.add(button_name_ok, button_name_close)

    msg = ""
    result = bot.send_message(message.chat.id, msg, reply_markup=markup)

    bot.register_next_step_handler(result, button_ok_and_otmena)

    return


def button_ok_and_otmena(message):
    if message.text == 'ОК':
        print('OK')


    elif message.text == 'ОТМЕНА':
        print('ОТМЕНА')

    return


# --------------------------------------------------OUT -----------------------------------------------------------------

bot.polling(none_stop=True)
########################################################################################################################

#                                                -SAVES-
