#####################################################
#####################################################
# DB에 접속해서 데이터를 추출하고 시각화까지 하는 모듈

import pymysql

##################################################### DB 접속 함수
# DB 접근 설정
db_user = "root"
db_password = "qwe123"


def db_connecting(id, key):
    global db, cursor
    db = pymysql.connect(host='127.0.0.1',
                         user=id, password=key, charset="utf8", port=5000)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('USE test;')
    if (cursor.execute("show status like 'Threads_connected';") == 1):
        print('test_db Connected')
#####################################################



#####################################################

# 1:호출한 시간 평균, 2:호출된 온도 평균, 3:호출된 습도 평균

#####################################################

db.connecting(db_user, db_password)

db.close()