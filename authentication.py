
# Органичение выполнение команды start

config ={
    'name': "@zserdxbot",
    "token": "5357562508:AAGRmz_kvhoYqV0ZpBgxufOWOxgQQ5ITrDI",
    'url': f'https://git.heroku.com/telegram-tms-bot.git{"token"}'
}



users_start = [315207431,385753167]  # последнее - id группы если бот что-то должен делать в группе

@bot.message_handler(func=lambda message: message.chat.id not in users_start, commands=['start', "print", "url"])
def some(message):
    bot.send_message(message.chat.id, 'У Вас нет прав на выполнение данной команды, обратитесь к администратору')
    return

