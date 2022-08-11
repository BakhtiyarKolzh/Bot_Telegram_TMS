
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import keyboard
from keyboard import press
import telebot
from telebot import types

#    My libraries
import configure  #### Library for Token
import authentication   #### Library Protect ID



#                                       INPUT DATES
##############################################################################
bot = telebot.TeleBot(configure.config["token"])
users_start = authentication.config["ID"]            # последнее - id группы если бот что-то должен делать в группе


url_BIM360 = "https://insight.b360.eu.autodesk.com/accounts/bf8a62b2-d479-4c2e-8523-103a1de299ea/projects/7a15c326-d421-4efb-98cd-fa817eb95f96/home"
url_Google_Sheets = "https://docs.google.com/spreadsheets/d/1tbvsFXLMzuKftQu9LV9jQ4FD6ik_l5yP-XRrhQsCrvw/edit?usp=sharing"
url_Yandex_Disk = "https://disk.yandex.kz/client/disk?utm_source=main_stripe_big_more"
url_BI_Design = "https://design.bi.group/"
url_Google_Docs = "https://docs.google.com/spreadsheets/d/1WesHLNRMiR5OOTFm0-t-VFiDfdix1NWCtgoqZq52nFI/edit#gid=0"

##############################################################################



#                                    --Bot Protection---

@bot.message_handler(func=lambda message: message.chat.id not in users_start, commands=['start', "print", "url"])
def some(message):
    bot.send_message(message.chat.id, 'У Вас нет прав на выполнение данной команды, обратитесь к администратору')
    return

##############################################################################

#                                   ----start Telegram bot----
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

    return

##############################################################################   Button for process /print


#                                 def for -print-   Creating buttons
##############################################################################
@bot.message_handler(commands=['print'])
def export_par(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    button_DWG = types.InlineKeyboardButton('DWG', callback_data="DWG")
    button_NWC = types.InlineKeyboardButton('NWC', callback_data="NWC")
    button_PDF = types.InlineKeyboardButton('PDF', callback_data="PDF")
    markup.add(button_DWG, button_NWC, button_PDF)
    bot.send_message(message.chat.id, "Выберите формат для перевода данных:", reply_markup=markup)
    return

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
    return

##################################################################################################################


#                                DWG CONVERTER
###############################################################################
def user_answer_for_DWG(message):
    open_dir = str(message.text)
    if os.path.exists(open_dir):

        #  SCAN DIR FOR REVIT
        # listPaths = SortRevitNameFiles()

        filepath = os.path.join(open_dir + "\ExportToDWG.bat")
        PathLaunch(filepath, message, "DWG")
        print("DWG")
        result = bot.send_message(message.chat.id, "Выберите файлы:")
        bot.register_next_step_handler(result, func_for_keyboard)
    else:
        bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
    return
###############################################################################
#                                NWC CONVERTER
###############################################################################

def user_answer_for_NWC(message):
    open_dir = str(message.text)
    if os.path.exists(open_dir):

        #  SCAN DIR FOR REVIT
        # listPaths = SortRevitNameFiles()

        filepath = os.path.join(open_dir + "\ExportToNavisworks.bat")
        PathLaunch(filepath, message, "NWC")
        print("NWC")
        result = bot.send_message(message.chat.id, "Выберите файлы:")
        bot.register_next_step_handler(result, func_for_keyboard)
    else:
        bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
    return

##################################################################################################################
#                                PDF CONVERTER
#####################################################################################################
def user_answer_for_PDF(message):
    open_dir = str(message.text)
    if os.path.exists(open_dir):

        #  SCAN DIR FOR REVIT
        # listPaths = SortRevitNameFiles()

        filepath = os.path.join(open_dir + "\ExportToPDF.bat")
        PathLaunch(filepath, message, "PDF")
        print("PDF")
        result = bot.send_message(message.chat.id, "Выберите файлы:")
        bot.register_next_step_handler(result, func_for_keyboard)

    else:
        bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
    return

###############################################################################################################

#                                -DEF- FOR start file
##############################################################################################
def PathLaunch(filepath, message, call):
    if (os.path.exists(filepath)):
        os.startfile(filepath)
        print("Старт")
        bot.send_message(message.chat.id, f"Процесс выгрузки в {call} запущен")
    return
#################################################################################################################

#                                -DEF- TO Sort files
################################################################
# def SortRevitNameFiles():
#     return
#################################################################






#                                -DEF- FOR Keyboard control
###########################################################################################################
def func_for_keyboard(message):
    number_of_file = str(message.text)
    if number_of_file > "0":
        keyboard.write(number_of_file)
        press('enter')
        console_a = bot.send_message(message.chat.id, f"Выбана секция {number_of_file}")
        bot.register_next_step_handler(console_a, func_for_keyboard)
    elif number_of_file == "0":
        keyboard.write("0")
        press('enter')
        bot.send_message(message.chat.id, f"Операция по выгрузке запущена")
    elif number_of_file == "-":
        keyboard.write("-")
        press('enter')
        bot.send_message(message.chat.id, f"Выполнена отмена операции по запуску")
    else:
        console_b = bot.send_message(message.chat.id, "ОШИБКА ВВОДА!!!")
        bot.register_next_step_handler(console_b, func_for_keyboard)
    return

#############################################################################################################

#                                BUTTON FOR -url-
####################################################################################################################
@bot.message_handler(commands=['url'])
def website(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    button_for_bim360 = types.InlineKeyboardButton("BIM360", url=url_BIM360)
    button_for_Google_Sheets = types.InlineKeyboardButton("Google Sheets", url=url_Google_Sheets)
    button_for_Yandex_Disk = types.InlineKeyboardButton("Yandex Disk", url=url_Yandex_Disk)
    button_for_BI_Design = types.InlineKeyboardButton("BIDesign", url=url_BI_Design)
    button_for_Google_Docs = types.InlineKeyboardButton("Google Docs", url=url_Google_Docs)
    markup.add(button_for_bim360, button_for_Google_Sheets, button_for_BI_Design, button_for_Yandex_Disk,
               button_for_Google_Docs)
    bot.send_message(message.chat.id, "Пройдите по ссылке снизу:", reply_markup=markup)
    return
#####################################################################################################################





#-------------------------------------------OUT --------------------

bot.polling(none_stop=True)
#######################################################################################################

#                                          -SAVES-