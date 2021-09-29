from datetime import datetime
import pymysql

def db_connecting(id, key):
    global db, cursor
    db = pymysql.connect(host='49.142.68.172',
                         user=id, password=key, charset="utf8", port=831)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('USE weather;')
    # if (cursor.execute("show status like 'Threads_connected';") == 1):
    #     print('db Connected')
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

