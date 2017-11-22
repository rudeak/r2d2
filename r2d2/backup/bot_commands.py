# from r2d2.db_bot import get_dictionary_name


def get_command(command):
    i = 0
    i = command.find(' ') + 1
    if i == 0:
        i = len(command)
    else:
        i -= 1
    command = command[0:i]
    return command


def bot_start():
    result = r'Привіт, я маленький, але гордий бот r2d2. Якщо ти хочеш дізнатися, що я вмію, набери /help'
    return result


def bot_help():
    result = '/start: почати спілкування \r\n /help: перечитати цей текст \r\n /: перемикання режиму анаграмування \r\n /addic: додати словник в базу \r\n /printdic: надрукувати список словників'
    return result


def bot_anagramm(msg):
    result = msg ['from']['username'] + \
        ', Все що ви введете я спробую анаграмувати'
    return result


def bot_end_anagramm(msg):
    result = msg['from']['username'] + ', ви вийшли з режиму анаграммування'
    return result


def ins_dic(msg):
    return msg['from']['username'] + ', відправте мені особистим назву таблиці словника'


def print_dic():
    return 'Назва таблиці - Тип таблиці'


def not_have_permissions(msg):
    return msg['from']['username'] + ', недостатньо прав для виконання комманди'


def unknown_command():
    return 'Я не знаю цієї команди'
