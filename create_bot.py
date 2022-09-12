
import os.path

from aiogram import types, executor, Dispatcher, Bot

import authentication  #### Library for authentication
import configure  #### Library for Token

########################################################################################################################
########################################################################################################################

bot = Bot(token=(configure.config["token"]))
dp = Dispatcher(bot)
users_start = authentication.config["ID"]  # последнее - id группы если бот что-то должен делать в группе
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")

start = False
directory = str()
controlId = str()
dictionary = dict()

reply_km = types.ReplyKeyboardMarkup
reply_kb = types.KeyboardButton
inline_km = types.InlineKeyboardMarkup
inline_kb = types.InlineKeyboardButton

temp = list()
