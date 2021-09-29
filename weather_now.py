#####################################################
#####################################################
# 지금 현재의 기상예보를 DB에 넣어줌과 동시에 사용자가 호출한 시간도 넣음

from urllib.request import urlopen, Request
from urllib.parse import urlencode, unquote, quote_plus
# quote - URL에 있는 한글을 자동으로 아스키 값으로 변환시킴
# unquote - 반대로 사람이 읽을 수 있는 값으로 변환시킴
from datetime import datetime
import json
import pymysql
import pandas as pd
from lib import weather_local, weather_db

def set_nowdate():
    global today_date, today_time, now, user_minute, user_hour
    now = datetime.now()
    if(now.minute<45):
        today_hour = now.hour - 1
        if today_hour < 10 :
            today_hour = '0' + str(today_hour)
    else:
        today_hour = now.hour
    if now.minute < 10:
        user_minute = '0'+str(now.minute)
    else :
        user_minute = str(now.minute)
    if now.hour < 10:
        user_hour = '0'+str(now.hour)
    else :
        user_hour = str(now.hour)
    today_minute = '00'
    today_time = str(today_hour) + today_minute
    if now.month < 10:
        today_month = '0'+str(now.month)
    else:
        today_month = str(now.month)
    if now.day < 10:
        today_day = '0'+str(now.day)
    else:
        today_day = str(now.day)
    today_date = str(now.year)+today_month+today_day
    return today_date

def get_data_now(x, y):
    ##################################################### 파라미터 설정
    CallBackURL = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    params = '?' + urlencode({
        quote_plus("serviceKey"): 'XIjRFoewvUDp4EDhRpATADoatwElkiQ%2F1J0tDooGjBTKStjRtuW3Zu89iE9cBsK%2Bz299IJwkbaE%2F%2F7SzcVo2yA%3D%3D',
        quote_plus("numOfRows"): '100',
        quote_plus('pageNo'): '1',
        quote_plus('dataType'): 'JSON',
        quote_plus('base_date'): set_nowdate(),
        quote_plus('base_time'): today_time,
        quote_plus('nx'): x,
        quote_plus('ny'): y
    })
    #####################################################
    # URL 데이터 파싱
    request = Request(CallBackURL + unquote(params))
    # API를 통해 데이터 GET
    response_body = urlopen(request).read()
    # JSON으로 변환
    data = json.loads(response_body)
    try:
        item_data = data['response']['body']['items']['item']
        return item_data
    except:
        print('호출날짜', set_nowdate())
        print('호출시간', today_time)
        print('잠시후 다시 시도해주세요.')
    

def send_data_user(local, x, y):
    global weather_data
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    item_data = get_data_now(x, y)
    weather_data = dict() # 테이블에 넣을 데이터로우
    weather_data['지역'] = str(local)
    ##################################################### 테이블에 넣을 데이터 정제
    for item in item_data:
        if item['category'] == 'T1H':  # 기온체크
            weather_data['기온'] = item['obsrValue']
        if item['category'] == 'PTY':  # 상태체크
            weather_code = item['obsrValue']
            if weather_code == '1':
                weather_state = 'rain'
            elif weather_code == '2':
                weather_state = 'rain'
            elif weather_code == '3':
                weather_state = 'snow'
            elif weather_code == '5':
                weather_state = 'mist'
            elif weather_code == '6':
                weather_state = 'mist'
            elif weather_code == '7':
                weather_state = 'snow'
            else:
                weather_state = 'none'
            weather_data['상태'] = weather_state
        if item['category'] == 'RN1':  # 강수량체크
            weather_data['강수량'] = item['obsrValue']
        if item['category'] == 'REH':  # 습도체크
            weather_data['습도'] = item['obsrValue']
    cursor.execute("INSERT INTO User(now_date, now_time, local, tmp, state, rainfall, humidity) VALUES "
                "('"+today_date+"', '"+user_hour+user_minute+
                "', '"+weather_data['지역']+
                "', '"+weather_data['기온']+"', '"+weather_data['상태']+
                "', '"+weather_data['강수량']+"', '"+weather_data['습도']+"')")
    db.commit()
    print("data sended")
    db.close()
    return weather_data

def weather_to_speak(local):
    flag = 0
    speak = []
    speak = '기온은 ' + weather_data['기온'] + '도이고                       '
    speak += '습도는 ' + weather_data['습도'] + '퍼센트야                     '
    if weather_data['상태'] == 'rain' :
        speak += '현재 비가 내리고 있는데                      '
        flag = 1
    elif weather_data['상태'] == 'snow' :
        speak += '현재 눈이 내리고 있는데                        '
        flag = 1
    elif weather_data['상태'] == 'mist' :
        speak += '현재 부슬비가 내리고 있는데                          '
        flag = 1
    else:
        speak += '현재 내리고 있는건 없어                             '

    if ((flag == 1) and (weather_data['강수량']) != '0'):
        speak += '강수량은 ' + weather_data['강수량'] + '밀리미터야                    '
    return str(speak)

if __name__ == "__main__":
    local, x, y = weather_local.find_user_location()
    send_data_user(local, x, y)
    print('data finished')


    