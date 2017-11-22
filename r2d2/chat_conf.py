def max_anagram(bot, msg, db):
    cursor = db.cursor()
    s = msg['text']
    s = s[s.rindex(' '):]
    bot.sendMessage(msg['chat']['id'], s)



