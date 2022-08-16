#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import telebot
from telebot import types

#    My libraries
import configure  #### Library for Token
import authentication   #### Library Protect ID
import RevitSortFiles



#                                       INPUT DATES
########################################################################################################################
bot = telebot.TeleBot(configure.config["token"])
users_start = authentication.config["ID"]            # последнее - id группы если бот что-то должен делать в группе




url_BIM360 = "https://insight.b360.eu.autodesk.com/accounts/bf8a62b2-d479-4c2e-8523-103a1de299ea/projects/7a15c326-d421-4efb-98cd-fa817eb95f96/home"
url_Google_Sheets = "https://docs.google.com/spreadsheets/d/1tbvsFXLMzuKftQu9LV9jQ4FD6ik_l5yP-XRrhQsCrvw/edit?usp=sharing"
url_Yandex_Disk = "https://disk.yandex.kz/client/disk?utm_source=main_stripe_big_more"
url_BI_Design = "https://design.bi.group/"
url_Google_Docs = "https://docs.google.com/spreadsheets/d/1WesHLNRMiR5OOTFm0-t-VFiDfdix1NWCtgoqZq52nFI/edit#gid=0"

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
    button_url = types.KeyboardButton('URL')

    markup.add(button_task,button_url)
    bot.send_message(message.chat.id, "Выберите необходимую команду", reply_markup=markup)

    return


@bot.message_handler(content_types=['text'])
def start_task(message):
    if message.chat.type == "private":
        if message.text == "Начать задание":
            call_button_batch(message)

    return

# @bot.message_handler(content_types=['text'])
# def start_url(message):
#     if message.chat.type == "private":
#         if message.text == "URL":
#             Website(message)
#
#     return

########################################################################################################################

'''   CREATE BUTTON ---- DWG,NWC,PDF   '''
#######################################################################################################################

@bot.message_handler(content_types=['text'])
def call_button_batch(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_DWG = types.KeyboardButton('DWG')
    button_NWC =types.KeyboardButton('NWC')
    button_PDF = types.KeyboardButton('PDF')

    markup.add(button_DWG, button_NWC, button_PDF)

    result=bot.send_message(message.chat.id, "Выберите формат для перевода данных:", reply_markup=markup)
    bot.register_next_step_handler(result, callback)

    return

@bot.message_handler(content_types=['text'])
def callback(message):
    if message.text == "DWG":
        dir_for_DWG=bot.send_message(message.chat.id, "Введите путь для DWG")
        bot.register_next_step_handler(dir_for_DWG, user_answer_for_DWG)

    elif message.text == "NWC":
        dir_for_NWC = bot.send_message(message.chat.id, "Введите путь для NWC")
        bot.register_next_step_handler(dir_for_NWC, user_answer_for_NWC)

    elif message.text == "PDF":
        dir_for_PDF = bot.send_message(message.chat.id, 'Введите путь для PDF')
        bot.register_next_step_handler(dir_for_PDF, user_answer_for_PDF)

    return
########################################################################################################################
########################################################################################################################

#########
#########
#########

'''DWG CONVERTER'''

########################################################################################################################
def user_answer_for_DWG(message):
    open_dir = str(message.text)
    if os.path.exists(open_dir):

        #  SCAN DIR FOR REVIT
        # listPaths = SortRevitNameFiles()

        filepath = os.path.join(open_dir + "\ExportToDWG.bat")
        path_launch(filepath, message, "DWG")
        print("DWG")
        result = bot.send_message(message.chat.id, "Выберите файлы:")
        # bot.register_next_step_handler(result, func_for_keyboard)
    else:
        bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
    return
########################################################################################################################

'''Navisworks CONVERTER'''

########################################################################################################################

def user_answer_for_NWC(message):
    open_dir = str(message.text)

    if os.path.exists(open_dir):


        #  SCAN DIR FOR REVIT
        # listPaths = SortRevitNameFiles()

        filepath = os.path.join(open_dir + "\ExportToNavisworks.bat")
        path_launch(filepath, message, "NWC")
        print("NWC")
        result = bot.send_message(message.chat.id, "Выберите файлы:")
        # bot.register_next_step_handler(result, func_for_keyboard)
    else:
        bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
    return

########################################################################################################################
'''PDF CONVERTER'''


def user_answer_for_PDF(message):
    input_path = os.path.realpath(message.text)
    if os.path.exists(input_path):
        print(input_path)

        #  SCAN DIR FOR REVIT
        listPaths = RevitSortFiles.get_result_rvt_path_list(input_path)

        print(listPaths)

        filepath = os.path.join(input_path + "\ExportToPDF.bat")

        path_launch(filepath, message, "PDF")
        print("PDF")
        menu_for_button(message)

        # bot.register_next_step_handler(result, new_func)

    else:
        bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
    return


########################################################################################################################
########################################################################################################################

#########
#########
#########

'''Start def'''
########################################################################################################################

def path_launch(filepath, message, call):
    if (os.path.exists(filepath)):
        # os.startfile(filepath)
        print("Старт")
        bot.send_message(message.chat.id, f"Процесс выгрузки в {call} запущен")
    return

########################################################################################################################
########################################################################################################################

'''SELECT A SECTION --- def'''

def new_func(message):
    number_of_file = str(message.text)
    print(number_of_file)
    call_button_ok(message)
    # result = bot.send_message(message.chat.id, f"Выберана секция {number_of_file}")
    # bot.register_next_step_handler(result, Call_button_ok)
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

    result=bot.send_message(message.chat.id, "Выберите нужную операцию", reply_markup=markup)
    bot.register_next_step_handler(result, select_button)

    return

def select_button(message):
    if message.text == "Выбор файлов":
        bot.send_message(message.chat.id, "СПИСОК ФАЙЛОВ ПОДАН, ВЫБЕРИТЕ НЕОБХОДИМЫЕ")
        call_button_ok(message)    ###### переместить в функицю по выбору файлов


    elif message.text == "Выбрать все файлы":
        bot.send_message(message.chat.id, "ВСЕ ФАЙЛЫ ВЫБРАНЫ")
        start(message)     #####   нужна директория и функция для выбора всех файлов

    elif message.text == "ОТМЕНА":
        bot.send_message(message.chat.id, " ОПЕРАЦИЯ ОТМЕНЕНА")
        start(message)


    return
########################################################################################################################
########################################################################################################################

'''kEYBOARD OK'''

@bot.message_handler(content_types=['text'])
def call_button_ok(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_name_ok = types.KeyboardButton('ОК')
    button_name_close = types.KeyboardButton('ОТМЕНА')
    markup.add(button_name_ok,button_name_close)

    result=bot.send_message(message.chat.id, "Подтвердите операцию нажав ОК, если оперцию нужно отменить Отмена", reply_markup=markup)
    bot.register_next_step_handler(result, button_ok)

    return

def button_ok(message):
    if message.text == 'ОК':
        bot.send_message(message.chat.id, "Операция по выгрузке запущена")
        start(message)
    if message.text == 'ОТМЕНА':
        bot.send_message(message.chat.id, "Операция по выгрузке отменена")
        start(message)

    return

########################################################################################################################
########################################################################################################################

































'''BUTTON URL'''
########################################################################################################################
@bot.message_handler(commands=['url'])
def website(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_for_bim360 = types.InlineKeyboardButton("BIM360", url=url_BIM360)
    button_for_Google_Sheets = types.InlineKeyboardButton("Google Sheets", url=url_Google_Sheets)
    button_for_Yandex_Disk = types.InlineKeyboardButton("Yandex Disk", url=url_Yandex_Disk)
    button_for_BI_Design = types.InlineKeyboardButton("BIDesign", url=url_BI_Design)
    button_for_Google_Docs = types.InlineKeyboardButton("Google Docs", url=url_Google_Docs)
    markup.add(button_for_bim360, button_for_Google_Sheets, button_for_BI_Design, button_for_Yandex_Disk,
               button_for_Google_Docs)
    bot.send_message(message.chat.id, "Пройдите по ссылке снизу:", reply_markup=markup)

    return
########################################################################################################################
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # button_DWG = types.KeyboardButton('DWG')
    # button_NWC =types.KeyboardButton('NWC')
    # button_PDF = types.KeyboardButton('PDF')
    #
    # markup.add(button_DWG, button_NWC, button_PDF)
    #
    # result=bot.send_message(message.chat.id, "Выберите формат для перевода данных:", reply_markup=markup)
    # bot.register_next_step_handler(result, Callback)
    #
    # return




#--------------------------------------------------OUT -----------------------------------------------------------------

bot.polling(none_stop=True)
########################################################################################################################

#                                                -SAVES-
