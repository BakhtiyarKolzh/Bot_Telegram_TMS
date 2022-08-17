




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
