import sys
import os
from flask import Flask, request
import telepot
import re
import random
from r2d2.bot_commands import *


try:
    from Queue import Queue
except ImportError:
    from queue import Queue

# db_result=db_connect()


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    pattern = r"/"
#    bot.sendMessage (chat_id, "Hello!!")
    if content_type == 'text':
        log(msg)
        if msg['text'][0] == '!':
            send_table(find_chat_anagram(bot,msg), chat_id, ' - ')
        if (chat_type == 'private') and (re.match(pattern, msg['text']) != True):
            if in_dictionary_mode(msg) == 2:
                update_dictionary (bot, msg)
                bot.sendMessage(chat_id, 'Відправте файл словника')
                msg['text'] = '/file'
                set_command(msg)
            if in_dictionary_mode(msg) == 1:
                if get_dic_table(msg) == 1:
                    create_temp_table(msg['text'], 'dic_table', msg)
                    bot.sendMessage(chat_id, 'Відправте файл словника')
                    msg['text'] = '/file'
                else:
                    create_temp_table(msg['text'], 'dic_table', msg)
                    msg['text'] = '/table'
                    bot.sendMessage(chat_id, 'Введіть опис словника')
                set_command(msg)
        text = ''
        if re.match(pattern, msg['text']):
            if get_command(msg['text']) == '/start':
                text = bot_start()
                set_command(msg)
            if get_command(msg['text']) == '/help':
                text = bot_help()
                set_command(msg)
            if get_command(msg['text']) == '/cleartables':
                if check_father(msg) == 1:
                    set_command(msg)
                    text = clear_temp_tables()
                else:
                    text = not_have_permissions(msg)
            if get_command(msg['text']) == '/renewusers':
                text = renew_users(msg)
            if get_command(msg['text']) == '/perm':
                text = change_permissions(msg)
            if get_command(msg['text']) == '/printusr':
                results = print_usr(msg)
                if results != not_have_permissions(msg):
                    send_table(results, msg['from']['id'], ' - ')
                    text = 'QAZXCVfdsaqwer'
                else:
                    text = results
            if get_command(msg['text']) == '/addic':
                if check_father(msg) == 1:
                    text = ins_dic(msg)
                    set_command(msg)
                else:
                    text = not_have_permissions(msg)
            if get_command(msg['text']) == '/ces':
                parse_caesar(bot, msg)
                text = 'cesar'
                set_command(msg)
            if get_command(msg['text']) == '/printdic':
                if check_father(msg) == 1:
                    text = print_dic()
                    bot.sendMessage(msg['from']['id'], text)
                    text = 'QAZXCVfdsaqwer'
                    results = get_dictionary_name()
                    send_table(results, msg['from']['id'], '-')
                    set_command(msg)
                else:
                    text = not_have_permissions(msg)
            if get_command(msg['text']) == '/chatconfig':
                config_chat(bot,msg)
                set_commad(msg)
            if get_command(msg['text']) == '/defdic':
                default_dic(bot,msg)
                set_command(msg)
            if get_command(msg['text']) == '/':
                if in_anagram_mode(msg) == 1:
                    text = bot_anagramm(msg)
                    set_command(msg)
                else:
                    text = bot_end_anagramm(msg)
                    msg['text'] = '/' + str(random.random())
                    set_command(msg)
            if text == '':
                send_table(find_anagram(bot, msg), chat_id, ' - ')
            if text != 'QAZXCVfdsaqwer' and text!='':
                bot.sendMessage(chat_id, text)
        else:
            if in_anagram_mode(msg) != 1:
                send_table(find_anagram(bot, msg), chat_id, ' - ')
            if msg['text'][0] == '?':
                #               bot.sendMessage(chat_id,'find')
                send_table(find_word(bot, msg), chat_id, ' - ')
            try:
                parse_morze(bot, msg)
            except:
                parse_abc(bot, msg)


    if content_type == 'sticker':
        bot.sendSticker(chat_id, get_rand_stck())
        log_stck(msg)
    if content_type == 'document':
        if get_last_command(msg) == '/file':
            bot.download_file(msg['document']['file_id'],
                              os.path.dirname(__file__) + '/files/' +
                              msg['document']['file_name'])
            file = open(os.path.dirname(__file__) + '/files/'
                        + msg['document']['file_name'], 'rt', encoding='utf8')
            result = file_check(file, bot)
            if result == 1:
                add_new_dic(bot, file, msg)
            else:
                send_table(result, msg['from']['id'], ' - ')
            file.close()
    # print('Chat Message:', content_type, chat_type, chat_id)


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)

# need `/setinline`


def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(
        msg, flavor='inline_query')
    print('Inline Query:', query_id, from_id, query_string)

    # Compose your own answers
    articles = [{'type': 'article',
                 'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]

    bot.answerInlineQuery(query_id, articles)

# need `/setinlinefeedback`


def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(
        msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)


TOKEN = '304374255:AAG-DGCvKpj-FiWaLjZ0KbENEMHpCmsRpxk'
PORT = 443
URL = 'https://bot.rudeak.gq/' + TOKEN

app = Flask(__name__)
bot = telepot.Bot(TOKEN)
update_queue = Queue()  # channel between `app` and `bot`

bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result}, source=update_queue)  # take updates from queue


def send_table(table, chat_id, divider):
    line = ''
    if len(table) > 1:
        for i in range(len(table)):
            for y in range(len(table[i])):
                line = line + str(table[i][y]) + divider
            line = str(i + 1) + '. ' + line[:line.rindex(divider)]
            bot.sendMessage(chat_id, line)
            line = ''
    else:
        bot.sendMessage(chat_id, table[0])


@app.route('/' + TOKEN, methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'

if __name__ == '__main__':
    bot.setWebhook(URL)
    app.run(port=PORT, debug=True)
