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
from lib import weather_local, weather_db, weatehr_data

# db접속
db, cursor = weather_db.db_connecting('root', 'qwe123')

# user의 지역 x, y좌표 따기
x, y = weather_local.find_user_location()

def set_nowdate():
    now = datetime.now()

    if(now.minute<45):
        today_hour = now.hour - 1
    else:
        today_hour = now.hour

    today_minute = '00'


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


##################################################### 파라미터 설정
CallBackURL = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params = '?' + urlencode({
    quote_plus("serviceKey"): 'XIjRFoewvUDp4EDhRpATADoatwElkiQ%2F1J0tDooGjBTKStjRtuW3Zu89iE9cBsK%2Bz299IJwkbaE%2F%2F7SzcVo2yA%3D%3D',
    quote_plus("numOfRows"): '100',
    quote_plus('pageNo'): '1',
    quote_plus('dataType'): 'JSON',
    quote_plus('base_date'): str(today_date),
    # quote_plus('base_time'): '1500',
    quote_plus('base_time'): str(today_hour)+today_minute,
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
item_data = data['response']['body']['items']['item']

weather_data = dict() # 테이블에 넣을 데이터로우

# Pandas_DataFrame으로 출력
# table = pd.DataFrame(data['response']['body']['items']['item'])
# print(table)

##################################################### 테이블에 넣을 데이터 정제
for item in item_data:
    if item['category'] == 'T1H':  # 기온체크
        weather_data['기온'] = item['obsrValue']

    if item['category'] == 'PTY':  # 상태체크
        weather_code = item['obsrValue']
        if weather_code == '1':
            weather_state = 'rain'
        elif weather_code == '2':
            weather_state = 'rain or snow'
        elif weather_code == '3':
            weather_state = 'snow'
        elif weather_code == '5':
            weather_state = 'mist'
        elif weather_code == '6':
            weather_state = 'mist or snowing'
        elif weather_code == '7':
            weather_state = 'snowing'
        else:
            weather_state = 'none'
        weather_data['상태'] = weather_state

    if item['category'] == 'RN1':  # 강수량체크
        weather_data['강수량'] = item['obsrValue']

    if item['category'] == 'REH':  # 강수량체크
        weather_data['습도'] = item['obsrValue']


cursor.execute("INSERT INTO User(now_date, now_time, tmp, state, rainfall, humidity) VALUES "
               "('"+today_date+"', '"+str(now.hour)+str(now.minute)+
               "', '"+weather_data['기온']+"', '"+weather_data['상태']+
               "', '"+weather_data['강수량']+"', '"+weather_data['습도']+"')")


db.commit()
print('Update Success')
db.close()