




########################################################################

##         FLAG
# @bot.message_handler(commands=['start'])
# def start(message, IsBissy=flag):
#     if False == IsBissy:
#         IsBissy = True
#         welcome = f"Добро пожаловать, <b>{message.from_user.first_name}</b>"
#         bot.send_message(message.chat.id, welcome, parse_mode='html')
#
#         menu_for_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         buttons = ["/print", "/url"]
#         for button in buttons:
#             menu_for_button.add(types.KeyboardButton(button))
#         bot.send_message(message.chat.id, "Выберите подходящую команду:", reply_markup=menu_for_button)
#     else:
#         bot.send_message(message.chat.id, " ", reply_markup= menu_for_button)
#         return
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