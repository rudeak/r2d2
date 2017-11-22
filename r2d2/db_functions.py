import pymysql


HOST = 'localhost'
USER = 'r2d2'
PASSWD = 'fkmnfdbcnf'
DB = 'r2d2'
CHARSET = 'utf8mb4'

def db_connect():
    try:
        db = pymysql.connect(
            host=HOST,
            user=USER,
            passwd=PASSWD,
            db=DB,
            charset=CHARSET)
        return db
    except:
        return 'error connect'
