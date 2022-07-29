#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import telebot
from telebot import types
import configure  #### Library for Token

#################################
# System Protection  by "ID"
bot = telebot.TeleBot(configure.config["token"])

users_start = [315207431]  # последнее - id группы если бот что-то должен делать в группе


# Органичение выполнение команды start
@bot.message_handler(func=lambda message: message.chat.id not in users_start, commands=['start', "print", "url"])
def some(message):
    bot.send_message(message.chat.id, 'У Вас нет прав на выполнение данной команды, обратитесь к администратору')


##############################################################################

@bot.message_handler(commands=['start'])
def start(message):
    welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
    bot.send_message(message.chat.id, welcome, parse_mode='html')

    menu_for_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/print", "/url"]
    for button in buttons:
        menu_for_button.add(types.KeyboardButton(button))
    bot.send_message(message.chat.id, "Выберите подходящую команду:", reply_markup=menu_for_button)


#######################################                 #######################################Button for process /print
@bot.message_handler(commands=['print'])
def export_par(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    button_DWG = types.InlineKeyboardButton('DWG', callback_data="DWG")
    button_NWC = types.InlineKeyboardButton('NWC', callback_data="NWC")
    button_PDF = types.InlineKeyboardButton('PDF', callback_data="PDF")
    markup.add(button_DWG, button_NWC, button_PDF)
    bot.send_message(message.chat.id, "Выберите формат для перевода данных:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'DWG':
            dir_for_DWG = bot.send_message(call.message.chat.id, 'Введите путь для DWG')
            bot.register_next_step_handler(dir_for_DWG, user_answer_for_DWG)

        elif call.data == 'NWC':
            dir_for_NWC = bot.send_message(call.message.chat.id, 'Введите путь для NWC')
            bot.register_next_step_handler(dir_for_NWC, user_answer_for_NWC)

        elif call.data == 'PDF':
            dir_for_PDF = bot.send_message(call.message.chat.id, 'Введите путь для PDF')
            bot.register_next_step_handler(dir_for_PDF, user_answer_for_PDF)
##################################################################################################################

def user_answer_for_DWG(message):
    open_dir = str(message.text)
    if os.path.exists(open_dir):
        filepath = os.path.join(open_dir + "\ExportToDWG.bat")
        PathLaunch(filepath, message, "DWG")
        print("DWG")
    else:
        bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")


def user_answer_for_NWC(message):
    open_dir = str(message.text)
    if os.path.exists(open_dir):
        filepath = os.path.join(open_dir + "\ExportToNavisworks.bat")
        PathLaunch(filepath, message, "NWC")
        print("NWC")
    else:
        bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")

def user_answer_for_PDF(message):
    open_dir = str(message.text)
    if os.path.exists(open_dir):
        filepath = os.path.join(open_dir + "\ExportToPDF.bat")
        PathLaunch(filepath, message, "PDF")
        print("PDF")
    else:
        bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")


##############################################################################################  Fuction for call
def PathLaunch(filepath,message,call):
    if (os.path.exists(filepath)):
        os.startfile(filepath)
        bot.send_message(message.chat.id, f"Процесс выгрузки в {call} запущен, ожидайте меню для выбора файлов")
    return
#################################################################################################################
##























###      URL for BOT

url_BIM360="https://insight.b360.eu.autodesk.com/accounts/bf8a62b2-d479-4c2e-8523-103a1de299ea/projects/7a15c326-d421-4efb-98cd-fa817eb95f96/home"
url_Google_Sheets="https://docs.google.com/spreadsheets/d/1tbvsFXLMzuKftQu9LV9jQ4FD6ik_l5yP-XRrhQsCrvw/edit?usp=sharing"
url_Yandex_Disk="https://disk.yandex.kz/client/disk?utm_source=main_stripe_big_more"
url_BI_Design="https://design.bi.group/"
url_Google_Docs="https://docs.google.com/spreadsheets/d/1WesHLNRMiR5OOTFm0-t-VFiDfdix1NWCtgoqZq52nFI/edit#gid=0"

##################################################################################################################################
@bot.message_handler(commands=['url'])
def website(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    button_for_bim360 = types.InlineKeyboardButton("BIM360", url=url_BIM360)
    button_for_Google_Sheets = types.InlineKeyboardButton("Google Sheets", url=url_Google_Sheets)
    button_for_Yandex_Disk = types.InlineKeyboardButton("Yandex Disk",url=url_Yandex_Disk)
    button_for_BI_Design = types.InlineKeyboardButton("BIDesign", url=url_BI_Design)
    button_for_Google_Docs = types.InlineKeyboardButton("Google Docs",url=url_Google_Docs)
    markup.add(button_for_bim360, button_for_Google_Sheets, button_for_BI_Design, button_for_Yandex_Disk,button_for_Google_Docs)
    bot.send_message(message.chat.id, "Пройдите по ссылке снизу:", reply_markup=markup)
####################################################################################################################################


bot.polling(none_stop=True)

# It needs for save, because maybe mistakes##################
###Fuck you

# open_dir = message.text
#     open_dir=str(open_dir)
#     for bat_name in os.listdir(open_dir):
#         filepath = os.path.join(open_dir + "\ExportToDWG.bat")
#         if (os.path.exists(filepath)):
#             os.startfile(filepath)
#             bot.send_message(message.chat.id, "Процесс выгрузки в DWG запущен")
#             return
#############################################################
# def user_answer_for_DWG(message):  ###   open bat file and show on the desktop
#     open_dir = str(message.text)
#     if os.path.exists(open_dir):
#         filepath = os.path.join(open_dir + "\ExportToDWG.bat")
#         if (os.path.exists(filepath)):
#             os.startfile(filepath)
#             bot.send_message(message.chat.id, "Процесс выгрузки в DWG запущен, ожидайте меню для выбора файлов")
#
#         return
#     else:
#         dir_for_DWG = bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
#         bot.register_next_step_handler(dir_for_DWG, user_answer_for_DWG)


#################################################                                        Experiment with NWC format


# def user_answer_for_NWC(message):
#     open_dir = str(message.text)
#     if os.path.exists(open_dir):
#         filepath = os.path.join(open_dir + "\ExportToNavisworks.bat")
#         if (os.path.exists(filepath)):
#             os.startfile(filepath)
#             bot.send_message(message.chat.id, "Процесс выгрузки в NWC запущен, ожидайте меню для выбора файлов")
#
#     else:
#         dir_for_NWC=bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
#         bot.register_next_step_handler(dir_for_NWC, user_answer_for_NWC)
#     return


