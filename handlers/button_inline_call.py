#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path
import time
from datetime import time


import database
import path_manager
from pathlib import WindowsPath

from aiogram import types, executor, Dispatcher, Bot
from create_bot import dp, bot, users_start, reply_kb, reply_km, controlId, directory, dictionary, flag, inline_kb, \
    inline_km, temp, data_path


########################################################################################################################
#######################################################################################################################

async def create_inline_buttons(message):
    global temp
    global inline_km
    global inline_kb
    time.sleep(0.5)
    if directory:
        buttons = []
        temp = list()
        keyboard = inline_km(row_width=1)
        paths = path_manager.get_result_rvt_path_list(directory)
        if isinstance(paths, list):
            for idx, path in enumerate(paths):
                filename, ext = os.path.splitext(WindowsPath(path).name)
                buttons.append(inline_kb(f'{idx + 1}.\t{filename}', callback_data=filename))
                temp.append(filename)

            keyboard.add(*buttons)
            keyboard.get_current()
            await message.answer("Выбрать:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data in temp)
async def call_inline_buttons(call: types.callback_query):
    global dictionary
    if any(call.data):
        filename = str(call.data)
        user_id = call.from_user.id
        await bot.send_message(call.from_user.id, f'✅ \tВыбран файл:\n{filename} ')
        vals = dictionary.get(user_id)
        if vals and isinstance(vals, list):
            vals.append(filename)


        # значение = list cmd
        # ключ = userId

        print(filename)

########################################################################################################################
########################################################################################################################
def register_handler():
    dp.callback_query_handlers(call_inline_buttons)

def callback_query_handler(dp: Dispatcher):
    dp.callback_query_handlers(call_inline_buttons, lambda c: c.data in temp)
