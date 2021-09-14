#####################################################
#####################################################
# excel에 있는 지역코드를 조회해서 리턴해주는 모듈

import pandas as pd
global Location, File, user_location_x, user_location_y
location_x = []
location_y = []
location_name = []
location_code = []

# Location = './source'
# Location = '/home/pi/Desktop/circulus/source'
Location = '/home/pi/weather_alarm/source'
File = 'weather_location.xlsx'


##################################################### 엑셀파일 읽고 user x, y좌표 따기함수
def find_user_location(user_location_x = 0, user_location_y = 0):

    print('지역을 입력해주세요. (ex - 서울특별시 관악구)')
    user_location= input().split(' ')

    data_pd = pd.read_excel('{}/{}'.format(Location, File),
                            header=None, index_col=None, names=None)
    data_pd1 = data_pd[data_pd[1]==user_location[1]]
    for item in data_pd1:
        user_location_x_list = list(data_pd1[3])
        user_location_x = user_location_x_list[0]
        user_location_y_list = list(data_pd1[4])
        user_location_y = user_location_y_list[0]

    if((user_location_x == 0 | user_location_y == 0) == True):
        return '지역명이 잘못 입력되었습니다.'
    else:
        print("find user_location", user_location[1], user_location_x, "", user_location_y)
        return user_location_x, user_location_y


#####################################################

# find_user_location()

##################################################### 엑셀파일 읽고 서울 구마다 x, y좌표 따기함수
def find_location():

    data_pd = pd.read_excel('{}/{}'.format(Location, File),
                            header=None, index_col=None, names=None)
    for item in data_pd.iloc:
        location_name.append(item[1])
        if item[2] < 10:
            test = "0" + str(item[2])
        else:
            test = str(item[2])
        location_code.append(test)
        location_x.append(item[3])
        location_y.append(item[4])

    return location_name, location_code, location_x, location_y
#####################################################
# find_location()
