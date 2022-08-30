




########################################################################

##         FLAG
# @bot.message_handler(commands=['start'])
# def start(message, IsBissy=flag):
#     if False == IsBissy:
#         IsBissy = True
#         welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
#         bot.send_message(message.chat.id, welcome, parse_mode='html')
#
    #     menu_for_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     buttons = ["/print", "/url"]
    #     for button in buttons:
    #         menu_for_button.add(types.KeyboardButton(button))
    #     bot.send_message(message.chat.id, "Выберите подходящую команду:", reply_markup=menu_for_button)
    # else:
    #     bot.send_message(message.chat.id, " ", reply_markup= menu_for_button)
    #     return
# ###########################################################################
#
#












##
#                SHABLON 1         scan dir
# def user_answer_for_PDF(message):
#     open_dir = str(message.text)
#     if os.path.exists(open_dir):
#         for file_name in os.listdir(open_dir):
#             if fnmatch.fnmatch(file_name, '*.rvt'):
#                 print(file_name)
#                 bot.send_message(message.chat.id, file_name)
#
#
#
# ##  end PROCESS
#         filepath = os.path.join(open_dir + "\ExportToPDF.bat")
#         PathLaunch(filepath, message, "PDF")
#         print("PDF")
#     else:
#         bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")
###########################################################################################
#            SHABLON 2
# def user_answer_for_PDF(message):
#     open_dir = str(message.text)
#     if os.path.exists(open_dir):


##  end PROCESS
#     filepath = os.path.join(open_dir + "\ExportToPDF.bat")
#     PathLaunch(filepath, message, "PDF")
#     print("PDF")
#
#         for direction in filepath:
#             direction = sys.stdin.readlines()
#             print(direction)
#
#
#
#     result=bot.send_message(message.chat.id, "Выберите файлы:")
#     bot.register_next_step_handler(result, func_for_keyboard)
#
#
#
# else:
#     bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗА

#НОВО!!!")

###########################################################################################
# def user_answer_for_PDF(message):
#     open_dir = str(message.text)
#     if os.path.exists(open_dir):
#         # filepath = os.path.join(open_dir, "ExportToPDF.bat")
#         # PathLaunch(filepath, message, "PDF")
#         # # print("PDF")
#
#         # with subprocess.Popen(filepath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
#         #
#         #
#         #
#         #     outs, errs = proc.communicate(timeout=5)
#         #     print("PDF")
#         #     with open(newfile, 'wb') as file:
#         #         file.write(outs)
#         #         print("Yes")
#         #
#
#
#
#         # result=bot.send_message(message.chat.id, "Выберите файлы:")
#         # bot.register_next_step_handler(result, func_for_keyboard)
#
#         ##  end PROCESS
#         filepath = os.path.join(open_dir + "\ExportToPDF.bat")
#         PathLaunch(filepath, message, "PDF")
#         print("PDF")
#         result = bot.send_message(message.chat.id, "Выберите файлы:")
#         bot.register_next_step_handler(result, func_for_keyboard)
#
#
#
#     else:
#         bot.send_message(message.chat.id, "ОШИБКА ПУТИ, ВВЕДИТЕ ПУТЬ ЗАНОВО!!!")

#####################   SCAN DIR                        ###########################################
        # for file_name in os.listdir(open_dir):
        #     if fnmatch.fnmatch(file_name, '*.rvt'):
        #         # print(file_name)
        # bot.send_message(message.chat.id, file_name)
        ##  end PROCESS
 ###########################################################################################################



#2022-08-12

#                                -DEF- FOR Keyboard control
########################################################################################################################
# def func_for_keyboard(message):
#     number_of_file = str(message.text)
#     if number_of_file > "0":
#         keyboard.write(number_of_file)
#         press('enter')
#         console_a = bot.send_message(message.chat.id, f"Выбана секция {number_of_file}")
#         bot.register_next_step_handler(console_a, func_for_keyboard)
#     elif number_of_file == "0":
#         keyboard.write("0")
#         press('enter')
#         bot.send_message(message.chat.id, f"Операция по выгрузке запущена")
#     elif number_of_file == "-":
#         keyboard.write("-")
#         press('enter')
#         bot.send_message(message.chat.id, f"Выполнена отмена операции по запуску")
#     else:
#         console_b = bot.send_message(message.chat.id, "ОШИБКА ВВОДА!!!")
#         bot.register_next_step_handler(console_b, func_for_keyboard)
#     return

########################################################################################################################

# i = bot.send_message(call.message.chat.id, 'текст')
# print(i)

########################################################################################################################
########################################################################################################################
########################################################################################################################



# @bot.message_handler(commands=['print'])
# def export_par(message):
#     markup = types.InlineKeyboardMarkup(row_width=3)
#     button_DWG = types.InlineKeyboardButton('DWG', callback_data="DWG", id=12)
#     button_NWC = types.InlineKeyboardButton('NWC', callback_data="NWC", id=12)
#     button_PDF = types.InlineKeyboardButton('PDF', callback_data="PDF", id=12)
#     markup.add(button_DWG, button_NWC, button_PDF)
#
#     bot.send_message(message.chat.id, "Выберите формат для перевода данных:", reply_markup=markup)
#     return
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     if call.message.chat.id:
#         if call.data == 'DWG':
#             dir_for_DWG = bot.send_message(call.message.chat.id, 'Введите путь для DWG')
#             bot.register_next_step_handler(dir_for_DWG, user_answer_for_DWG)
#
#         elif call.data == 'NWC':
#             dir_for_NWC = bot.send_message(call.message.chat.id, 'Введите путь для NWC')
#             bot.register_next_step_handler(dir_for_NWC, user_answer_for_NWC)
#
#         elif call.data == 'PDF':
#             dir_for_PDF = bot.send_message(call.message.chat.id, 'Введите путь для PDF')
#             bot.register_next_step_handler(dir_for_PDF, user_answer_for_PDF)
#     return
########################################################################################################################
########################################################################################################################
# '''SELECT BUTTON OK --- ZERO'''
#
# def func_zero(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button_name_ok = types.KeyboardButton('ОК')
#     markup.add(button_name_ok)
#     result = bot.send_message(message.chat.id, "Подтвердите операцию нажав ОК",
#                               reply_markup=markup)
#     bot.register_next_step_handler(result, func_zero_button_ok)
#     return
#
# def func_zero_button_ok(message):
#     if message.text == 'ОК':
#         global filepath
#         global commands
#         global controlId
#         result=bot.send_message(message.chat.id, "Операция по выгрузке запущена")
#         # database.save_command_data(database_path, filepath, controlId, commands)
#         bot.register_next_step_handler(result, start)
#
#     return
# ########################################################################################################################
########################################################################################################################





'''BUTTON URL'''


########################################################################################################################
# def website(message):
#     markup = types.InlineKeyboardMarkup(row_width=3)
#
#     button_for_bim360 = types.InlineKeyboardButton("BIM360", url=url_BIM360)
#     button_for_Google_Sheets = types.InlineKeyboardButton("Google Sheets", url=url_Google_Sheets)
#     button_for_Yandex_Disk = types.InlineKeyboardButton("Yandex Disk", url=url_Yandex_Disk)
#     button_for_BI_Design = types.InlineKeyboardButton("BIDesign", url=url_BI_Design)
#     button_for_Google_Docs = types.InlineKeyboardButton("Google Docs", url=url_Google_Docs)
#     markup.add(button_for_bim360,
#                button_for_Google_Sheets,
#                button_for_BI_Design,
#                button_for_Yandex_Disk,
#                button_for_Google_Docs)
#     bot.send_message(message.chat.id, "Пройдите по ссылке снизу:", reply_markup=markup)
#
#     return
#
#
# #######################################################################################################################
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

######################################################################################################


#     await call_button_format(message)
#     print("ok")
#     return
#
# async def call_button_format(message):
# #     global controlId
#     if message.text =='DWG' or 'NWC' or 'PDF':
#         print('format')
#         if message.text == "DWG":
#             controlId = "DWG"
#             await bot.send_message(message.chat.id, "Введите путь для DWG")
#             print(controlId)
#
#         elif message.text == "NWC":
#             controlId = "NWC"
#             await bot.send_message(message.chat.id, "Введите путь для NWC")
#             print(controlId)
#
#         elif message.text == "PDF":
#             controlId = "PDF"
#             await bot.send_message(message.chat.id, 'Введите путь для PDF')
#             print(controlId)
#         #
#         # else:


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