#####################################################
#####################################################
# 실행할 경우 DB에 3일간의 일기예보를 저장함

from urllib.request import urlopen, Request
from urllib.parse import urlencode, unquote, quote_plus
# quote - URL에 있는 한글을 자동으로 아스키 값으로 변환시킴
# unquote - 반대로 사람이 읽을 수 있는 값으로 변환시킴
from datetime import datetime
import json
import pymysql
import weather_db
# import pandas as pd

count = 0

###################################################### 시간 계산 및 기준 시간 설정
now = datetime.now()
today_time = int(str(now.hour)+str(now.minute))
today_day = now.day
if today_time < 215:
    today_day -= 1
    today_time = '2315'
elif today_time < 515:
    today_time = '0215'
elif today_time < 815:
    today_time = '0515'
elif today_time < 1115:
    today_time = '0815'
elif today_time < 1415:
    today_time = '1115'
elif today_time < 1715:
    today_time = '1415'
elif today_time < 2015:
    today_time = '1715'
elif today_time < 2315:
    today_time = '2015'
else:
    today_time = '2315'
today_date = str(now.year)+'0'+str(now.month)+str(today_day)
#####################################################



##################################################### 파라미터 설정
CallBackURL = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
params = '?' + urlencode({
    quote_plus("serviceKey"): 'XIjRFoewvUDp4EDhRpATADoatwElkiQ%2F1J0tDooGjBTKStjRtuW3Zu89iE9cBsK%2Bz299IJwkbaE%2F%2F7SzcVo2yA%3D%3D',
    quote_plus("numOfRows"): '1000',
    quote_plus('pageNo'): '1',
    quote_plus('dataType'): 'JSON',
    quote_plus('base_date'): today_date,
    quote_plus('base_time'): today_time,
    quote_plus('nx'): '59',
    quote_plus('ny'): '125'
})
#####################################################



# URL 데이터 파싱
request = Request(CallBackURL + unquote(params))
# API를 통해 데이터 GET
response_body = urlopen(request).read()
# JSON으로 변환
data = json.loads(response_body)
item_data = data['response']['body']['items']['item']

# Pandas_DataFrame으로 출력
# table = pd.DataFrame(data['response']['body']['items']['item'])
# print(table)

weather_data = dict() # 조회한 오늘 날씨 정보

##################################################### DB연결 및 기존 테이블 삭제
db_connecting(db_user, db_password)
cursor.execute("TRUNCATE weather_future_db")
db.commit()
print('Delete Success')
#####################################################


##################################################### 테이블에 넣을 데이터 정제
for item in item_data:
    weather_data['날짜'] = item['fcstDate']
    weather_data['시간'] = item['fcstTime']
    if item['category'] =='TMP': # 기온체크
        weather_data['기온'] = item['fcstValue']
        count += 1
    if item['category'] == 'POP': # 상태체크
        weather_data['강수확률'] = item['fcstValue']
        count += 1
    if item['category'] == 'SKY': # 하늘체크
        weather_code = item['fcstValue']
        count += 1
        if weather_code == '1':
            weather_state = 'sunny'
        elif weather_code == '3':
            weather_state = 'cloudy'
        elif weather_code == '4':
            weather_state = 'gray'
        else:
            weather_state = 'none'
        weather_data['하늘'] = weather_state
    # 컬럼개수를 만족하는 데이터는 테이블에 삽입
    if count == 3:
        cursor.execute("INSERT INTO weather_future_db(date, time, tmp, rain, sky) VALUES ('"+
                       weather_data['날짜']+"', '"+weather_data['시간']+"', '" +
                       weather_data['기온']+"', '"+weather_data['강수확률']+"', '"+weather_data['하늘']+"')")
        db.commit()
        count = 0
print('Update Success')
db.close()
#####################################################

# 사용자가 입력하는 값을 넣는게 맞나?
# 먼저 그냥 db에 다 넣어놓고 호출하는게 맞나?
# 호출을 할 때 트리거? 명령어?를 선정하는게 어려움
# 현재 날씨는 db에 넣는것 까지 성공
