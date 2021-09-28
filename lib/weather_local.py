import pandas as pd
global Location, File, user_location_x, user_location_y
location_x = []
location_y = []
location_name = []
location_code = []
Location = './source'
File = 'weather_location.xlsx'

def find_user_location(user_location_x = 0, user_location_y = 0):
    print('지역(구)을 입력해주세요. (ex - 관악구)')
    user_location= input()
    data_pd = pd.read_excel('{}/{}'.format(Location, File),
                            header=None, index_col=None, names=None)
    data_pd1 = data_pd[data_pd[1]==user_location]
    for item in data_pd1:
        user_location_x_list = list(data_pd1[2])
        user_location_x = user_location_x_list[0]
        user_location_y_list = list(data_pd1[3])
        user_location_y = user_location_y_list[0]

    if((user_location_x == 0 | user_location_y == 0) == True):
        return '지역명이 잘못 입력되었습니다.'
    else:
        print("find user_location", user_location, user_location_x, "", user_location_y)
        return user_location, user_location_x, user_location_y

def find_speak_location(user_location, user_location_x = 0, user_location_y = 0):
    try:
        data_pd = pd.read_excel('{}/{}'.format(Location, File),
                                header=None, index_col=None, names=None)
        data_pd1 = data_pd[data_pd[1]==user_location]
        for item in data_pd1:
            user_location_x_list = list(data_pd1[2])
            user_location_x = user_location_x_list[0]
            user_location_y_list = list(data_pd1[3])
            user_location_y = user_location_y_list[0]
        print("find user_location", user_location, user_location_x, "", user_location_y)
        return user_location_x, user_location_y
    except:
        print("can't find user_location")
        return user_location_x, user_location_y
def find_location():
    data_pd = pd.read_excel('{}/{}'.format(Location, File),
                            header=None, index_col=None, names=None)
    for item in data_pd.iloc:
        location_name.append(item[1])
        location_x.append(item[2])
        location_y.append(item[3])
    return location_name, location_x, location_y
