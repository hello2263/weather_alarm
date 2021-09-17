from datetime import datetime
import pymysql

# DB 접근 설정
db_user = "root"
db_password = "qwe123"


def db_connecting(id, key):
    global db, cursor
    db = pymysql.connect(host='192.168.0.14',
                         user=id, password=key, charset="utf8", port=3306)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('USE weather;')
    if (cursor.execute("show status like 'Threads_connected';") == 1):
        print('db Connected')

    return db, cursor

def nowtime():
    now = datetime.now()

    if now.month < 10:
        today_month = '0'+str(now.month)
    else:
        today_month = str(now.month)
        
    if now.day < 10:
        today_day = '0'+str(now.day)
    else:
        today_day = str(now.day)

    if now.hour < 10:
        today_hour = '0'+str(now.hour)
    else:
        today_hour = str(now.hour)

    today_date = str(now.year)+today_month+today_day
    today_time = today_hour+'00'

    return str(today_date + '-' + today_time)

