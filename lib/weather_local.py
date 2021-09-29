import pandas as pd
# import weather_db
from lib import weather_db

global Location, File, user_location_x, user_location_y
location_x = []
location_y = []
location_name = []
location_code = []
# Location = './source'
Location = '/home/pi/weather_alarm/source'
File = 'weather_location.xlsx'

def update_local_db():
    count = 0
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    data_pd = pd.read_excel('{}/{}'.format(Location, File),
                            header=None, index_col=None, names=None)
    try:
        for row in data_pd.loc():
            count += 1
            if count > 26:
                break
            param = []
            for item in row:
                param.append(item)
            cursor.execute("INSERT INTO local(area, city, x, y) VALUES ('"+param[0]+"', '"+param[1]+
            "', '"+str(param[2])+"', '"+str(param[3])+"') ON DUPLICATE KEY UPDATE x='"+str(param[2])+"', y='"+
            str(param[3])+"';")
    except:
        print("local updated")
    db.commit()
    db.close()

def find_speak_local(sentence):
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    cursor.execute("SELECT city FROM local;")
    cur = cursor.fetchall()
    try:
        for item in cur:
            test = item['city'][:-1]
            if len(test) == 1:
                test = test + '구'
            if test in sentence:
                return item['city']
    except:
        print('지역을 이해하지 못했습니다.')


def find_user_location(user_location_x = 0, user_location_y = 0):
    print('지역(구)을 입력해주세요. (ex - 관악구)')
    user_location= input()
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    # data_pd = pd.read_excel('{}/{}'.format(Location, File),
    #                         header=None, index_col=None, names=None)
    # data_pd1 = data_pd[data_pd[1]==user_location]
    # for item in data_pd1:
    #     user_location_x_list = list(data_pd1[2])
    #     user_location_x = user_location_x_list[0]
    #     user_location_y_list = list(data_pd1[3])
    #     user_location_y = user_location_y_list[0]
    cursor.execute("SELECT x FROM local WHERE city = '"+user_location+"';")
    curX = cursor.fetchall()
    user_location_x = int((curX[0])['x'])
    cursor.execute("SELECT y FROM local WHERE city = '"+user_location+"';")
    curY = cursor.fetchall()
    user_location_y = int((curY[0])['y'])
    if((user_location_x == 0 | user_location_y == 0) == True):
        return '지역명이 잘못 입력되었습니다.'
    else:
        print("find user_location", user_location, user_location_x, "", user_location_y)
        return user_location, user_location_x, user_location_y

def find_speak_location(user_location, user_location_x = 0, user_location_y = 0):
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    try:
        # data_pd = pd.read_excel('{}/{}'.format(Location, File),
        #                         header=None, index_col=None, names=None)
        # data_pd1 = data_pd[data_pd[1]==user_location]
        # for item in data_pd1:
        #     user_location_x_list = list(data_pd1[2])
        #     user_location_x = user_location_x_list[0]
        #     user_location_y_list = list(data_pd1[3])
        #     user_location_y = user_location_y_list[0]
        cursor.execute("SELECT x FROM local WHERE city = '"+user_location+"';")
        curX = cursor.fetchall()
        user_location_x = int((curX[0])['x'])
        cursor.execute("SELECT y FROM local WHERE city = '"+user_location+"';")
        curY = cursor.fetchall()
        user_location_y = int((curY[0])['y'])
        print("find user_location", user_location, user_location_x, "", user_location_y)
        return user_location_x, user_location_y
    except:
        print("can't find user_location")
        return user_location_x, user_location_y

def find_location():
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    # data_pd = pd.read_excel('{}/{}'.format(Location, File),
    #                         header=None, index_col=None, names=None)
    cursor.execute("SELECT city, x, y FROM local;")
    cur = cursor.fetchall()
    for item in cur:
        location_name.append(item['city'])
        location_x.append(item['x'])
        location_y.append(item['y'])
    return location_name, location_x, location_y

if __name__ == '__main__':
    find_speak_location('강남구')