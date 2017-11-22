import pymysql
import random
from r2d2.bot_commands import *

HOST = 'localhost'
USER = 'r2d2'
PASSWD = 'fkmnfdbcnf'
DB = 'r2d2'


def db_connect():
    try:
        db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DB)
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS chat_log")
        sql = """CREATE TABLE `users` ( `user_id` INT NOT NULL ,
             `permissions` CHAR NOT NULL ) ENGINE = InnoDB;"""
        cursor.execute(sql)
        sql = """CREATE TABLE `chat_log` ( `chat_id` INT NOT NULL ,
            `uid` INT NOT NULL ,
            `msg_id` INT NOT NULL ,
            `msg` TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL , 
            `msg_type` TEXT CHARACTER SET utf8 NOT NULL,
            `date_time` TIMESTAMP NOT NULL ) 
            ENGINE = InnoDB;"""
        cursor.execute(sql)
        db.close()
        return 'ok'
    except:
        return 'error connect'

#
#
# LOGGIN                                                               #
#
#


def log(msg):
    try:
        chatid = str(msg['chat']['id'])
        uid = str(msg['from']['id'])
        msg_text = msg['text']
        msg_type = 'text'
        msg_date = str(msg['date'])
        msg_id = str(msg['message_id'])
        sql = 'INSERT INTO chat_log (chat_id, uid, msg_id,msg, msg_type) VALUES (' + \
            chatid + ',' + uid + ',' + msg_id + \
            ',"' + msg_text + \
            '","' + msg_type + '");'
        db = pymysql.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
            charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return sql
    except:
        db.rollback()
        return 'error log'
    db.close()


def log_stck(msg):
    try:
        chatid = str(msg['chat']['id'])
        uid = str(msg['from']['id'])
        msg_id = str(msg['message_id'])
        file_id = msg['sticker']['file_id']
        emoj = msg['sticker']['emoji']
        sql = 'INSERT INTO stickers (chat_id, uid, msg_id,file_id) VALUES (' + \
            chatid + ',' + uid + ',' + \
            msg_id + ',"' + file_id + '");'
        db = pymysql.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
            charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return 'sticker log OK!'
    except:
        db.rollback()
        return 'error log sticker'
    db.close()


def set_command(msg):
    try:
        sql = 'SELECT uid FROM last_command WHERE uid=' + \
            str(msg['from']['id'])
        db = pymysql.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
            charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            sql = 'INSERT INTO last_command (uid, command) VALUES (' + str(
                msg['from']['id']) + ',"' + get_command(msg['text']) + '");'
        else:
            sql = 'UPDATE last_command SET command="' + \
                get_command(msg['text']) + '" WHERE uid=' + str(
                    msg['from']['id'])
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        return sql
    except:
        db.rollback()
        return 'error updating command'
    db.close()


#
#
# READING BASE                                                         #
#
#


def get_rand_stck():
    try:
        sql = 'SELECT file_id FROM stickers'
        db = pymysql.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
            charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[random.randint(1, len(result) - 1)][0]
    except:
        return 'error get sticker'
    db.close()


def get_dictionary_name():
    try:
        sql = 'SELECT * FROM voc'
        db = pymysql.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
            charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except:
        return 'error get sticker'
    db.close()


#
#
# CHECKING COMMANDS                                                    #
#
#


def in_anagram_mode(msg):
    sql = 'SELECT command FROM last_command WHERE command="/" AND uid=' + \
        str(msg['from']['id'])
    try:
        db = pymysql.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
            charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            db.close()
            return 1
        else:
            db.close()
            return 2
    except:
        return 'get anagramm mode error'
        db.close()


def in_dictionary_mode(msg):
    sql = 'SELECT command FROM last_command WHERE command="/addic" AND uid=' + \
        str(msg['from']['id'])
#    try:
    db = pymysql.connect(
        host=HOST,
        user=USER,
     passwd=PASSWD,
     db=DB,
     charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) != 0:
        db.close()
        return 1
    else:
        sql = 'SELECT command FROM last_command WHERE command="/table" AND uid=' + \
            str(msg['from']['id'])
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            db.close()
            return 2
#    except:
#        return 'get dictionary mode error'
#        db.close()

#
#
# PERMISSIONS                                                          #
#
#


def check_father(msg):
    sql = 'SELECT permissions FROM users WHERE uid=' + str(msg['from']['id'])
    try:
        db = pymysql.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
            charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            if result[0][0] == 'father':
                db.close()
                return 1
            else:
                db.close()
                return 2
        else:
            db.close()
            return 2

    except:
        return 'get permissions error'
        db.close()


def check_admin(msg):
    sql = 'SELECT permissions FROM users WHERE uid=' + str(msg['from']['id'])
    try:
        db = pymysql.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
            charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            if result[0][0] == 'admin':
                db.close()
                return 1
            else:
                db.close()
                return 2
        else:
            db.close()
            return 2

    except:
        return 'get permissions'
        db.close()


def check_user(msg):
    sql = 'SELECT permissions FROM users WHERE uid=' + str(msg['from']['id'])
    try:
        db = pymysql.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
            charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) != 0:
            if result[0][0] == 'user':
                db.close()
                return 1
            else:
                db.close()
                return 2
        else:
            db.close()
            return 2

    except:
        return 'get permissions'
        db.close()
