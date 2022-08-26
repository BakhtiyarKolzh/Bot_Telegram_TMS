#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path

from aiogram import types, executor, Dispatcher, Bot

import configure  #### Library for Token

#                                       INPUT DATES
########################################################################################################################

bot = Bot(token=(configure.config["token"]))
dp = Dispatcher(bot)

flag = False
directory = None
controlId = None
commands = list()

########################################################################################################################
########################################################################################################################
'''   START TELEGRAM    '''


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    global controlId
    chat_id = message.from_user.id
    welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
    await bot.send_message(chat_id=chat_id, text=welcome, parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Начать задание'))
    await message.answer("Выберите команду Начать задание", reply_markup=markup)
    print('Начать задание')


########################################################################################################################
########################################################################################################################

@dp.message_handler(lambda message: message.text == 'Начать задание')
async def call_back_start_to_format(message: types.Message):
    global flag
    flag = True
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='DWG'), types.KeyboardButton(text='NWC'), types.KeyboardButton(text='PDF'))
    await message.answer("Выберите формат для перевода данных:", reply_markup=markup)
    print("Выберите формат для перевода данных:")


########################################################################################################################
########################################################################################################################

@dp.message_handler(lambda message: message.text in ['DWG', 'NWC', 'PDF'])
async def call_back_format(message: types.Message):
    global flag
    print(flag)
    if flag:
        await message.answer("Введите путь:")
        global controlId
        controlId = message.text
        print(controlId)
        flag = False


########################################################################################################################
########################################################################################################################

# @dp.message_handler(lambda message: message.text in ['DWG', 'NWC', 'PDF'])
# async def check_directory(message: types.Message):
#     global directory
#     global flag
#
#     directory = os.path.realpath(message.text)
#     if os.path.exists(directory):
#         await menu_for_button(message)
#         print("exist")
#

########################################################################################################################
########################################################################################################################

'''Menu_for_button'''


@dp.message_handler(lambda message: os.path.exists(os.path.realpath(message.text)))
async def menu_for_button(message: types.Message):
    print(message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add((types.KeyboardButton(text='Выбор файлов')), (types.KeyboardButton(text='Выбрать все файлы')),
               (types.KeyboardButton(text='Отложить операцию')))
    await message.answer("Выберите нужную операцию", reply_markup=markup)
    print("Выберите нужную операцию")
    await call_back_menu(message)


@dp.message_handler(lambda message: len(message.text) > 15 and not os.path.exists(os.path.realpath(message.text)))
async def test_for_button(message: types.Message):
    await message.answer("okey")
    print(message.text)


########################################################################################################################
########################################################################################################################

@dp.message_handler(lambda message: message.text in ['Выбор файлов', 'Выбрать все файлы', 'Отложить операцию'])
async def call_back_menu(message: types.Message):
    if message.text == "Выбор файлов":
        print("Выбор файлов")
    elif message.text == "Выбрать все файлы":
        print("Выбрать все файлы")
    elif message.text == "Отложить операцию":
        print("ОТМЕНА")


########################################################################################################################
########################################################################################################################


# @dp.callback_query_handler(text='DWG')
# @dp.callback_query_handler(text='NWC')
# @dp.callback_query_handler(text='PDF')
# # @dp.message_handler(content_types=['text'], regexp=r"^(\w+)")
# async def call_button_batch(message: types.Message):
#     global controlId
#     chat_id = message.from_user.id
#     if message.text == "Начать задание":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(types.KeyboardButton('DWG'), types.KeyboardButton('NWC'), types.KeyboardButton('PDF'))
#         await bot.send_message(chat_id, "Выберите формат для перевода данных:", reply_markup=markup)
#         print("Выберите формат для перевода данных:")
#
#     if message.text in ['DWG', 'NWC', 'PDF']:
#         print('format')
#         print('it goes to the path ')
#         await bot.send_message(chat_id, "Введите путь")
#         if message.text == "DWG":
#             controlId = "DWG"
#             print(controlId)
#             await user_answer_format(message)
#         if message.text == "NWC":
#             controlId = "NWC"
#             print(controlId)
#             await user_answer_format(message)
#         if message.text == "PDF":
#             controlId = "PDF"
#             print(controlId)
#             await user_answer_format(message)
#     else:
#         await asyncio.
#         await call_button_batch(message)
#     return

########################################################################################################################
########################################################################################################################
#
# @dp.message_handler(content_types=['text'])
# async def user_answer_format(message: types.Message):
#     global directory
#     directory = os.path.realpath(message.text)
#     if os.path.exists(directory):
#         await menu_for_button(message)
#         print("exist")
#
#     return
#
#
# ########################################################################################################################
# ########################################################################################################################
#
# '''Menu_for_button'''
#
#
# @dp.message_handler(content_types=['text'])
# async def menu_for_button(message: types.Message):
#     global commands
#     chat_id = message.from_user.id
#     if message.text:
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add(types.KeyboardButton('Выбрать все файлы'), types.KeyboardButton('Выбрать все файлы'),
#                    types.KeyboardButton('ОТМЕНА'))
#         await bot.send_message(chat_id, "Выберите нужную операцию", reply_markup=markup)
#         print("Выберите нужную операцию")
#     if message.text == "Выбор файлов" or "Выбрать все файлы" or "ОТМЕНА":
#         print('f11111')
#         if message.text == "Выбор файлов":
#             print("Выбор файлов")
#
#         elif message.text == "Выбрать все файлы":
#             print("Выбрать все файлы")
#
#         elif message.text == "ОТМЕНА":
#             print("ОТМЕНА")
#
#         return
#     return
#
#
# '''SELECT A SECTION --- def'''


# hide = types.InlineKeyboardButton
#
# @dp.message_handler(content_types=['text'])
# async def cmd_select_inline(message: types.Message, project_path):
#     chat_id = message.from_user.id
#     buttons = []
#     time.sleep(0.5)
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     paths = path_manager.get_result_rvt_path_list(project_path)
#     for idx, path in enumerate(paths):
#         name, ext = os.path.splitext(WindowsPath(path).name)
#         buttons.append(types.InlineKeyboardButton(name, callback_data=idx + 1))
#
#     keyboard.add(*buttons)
#     await bot.send_message(chat_id, "Выбрать: ", reply_markup=keyboard)
#     await call_button_ok_and_cancel(message)
#
#     return

# @dp.callback_query_handler(func=lambda call: True)
# def call_for_cmd_line(call):
#     global commands
#     if any(call.data):
#         number = call.data
#         number = int(number) if number.isdigit() else 0
#         commands.append(number)
#         print(number)
#
#     return


########################################################################################################################
########################################################################################################################
# @dp.message_handler(content_types=['text'])
# async def call_button_ok_and_cancel(message):
#     global commands
#     global controlId
#     global directory
#     chat_id = message.from_user.id
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     markup.add(types.KeyboardButton('ОК'), types.KeyboardButton('ОТМЕНА'))
#     markup.one_time_keyboard = True
#     await bot.send_message(chat_id, "Введите данные", reply_markup=markup)
#     msg = message.text
#     print(msg)
#
#     if msg == 'ОК':
#         print('ОК')
#         return True
#
#     elif msg == 'ОТМЕНА':
#         print('ОТМЕНА')
#         return True
#
#
# ########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
#
# async def is_enabled():
#     print('запускаю цикл')
#     while True:
#         print('отправляю сообщения')
#         for user_id in range(100):
#             await asyncio.sleep(1)
#             print('отправил')
#         print('жду')
#         await asyncio.sleep(10)
#
#
# async def on_startup(x):
#     asyncio.create_task(is_enabled())
#
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True, timeout=1, on_startup=on_startup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, timeout=1)
