from urllib.request import urlopen, Request
from urllib.parse import urlencode, unquote, quote_plus
from datetime import datetime
import json
from lib import weather_db, weather_local
global today_date, x, y

def set_date(): 
    global today_time, today_date
    now = datetime.now()
    today_time = int(str(now.hour)+str(now.minute))
    today_day = now.day
    if today_time < 215:
        today_day -= 1
        today_time = '2330'
    elif today_time < 515:
        today_time = '0230'
    elif today_time < 815:
        today_time = '0530'
    elif today_time < 1115:
        today_time = '0830'
    elif today_time < 1415:
        today_time = '1130'
    elif today_time < 1715:
        today_time = '1430'
    elif today_time < 2015:
        today_time = '1730'
    elif today_time < 2315:
        today_time = '2030'
    else:
        today_time = '2330'   
    if now.month < 10:
        today_month = '0'+str(now.month)
    else:
        today_month = str(now.month)

    if today_day < 10:
        today_day = '0'+str(today_day)
    else:
        today_day = str(today_day)
    today_date = str(now.year)+today_month+today_day # 20210905

    return today_date + '-' + today_time # 20210905-1400

        
def get_data(): 
    CallBackURL = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    params = '?' + urlencode({
        quote_plus("serviceKey"): 'XIjRFoewvUDp4EDhRpATADoatwElkiQ%2F1J0tDooGjBTKStjRtuW3Zu89iE9cBsK%2Bz299IJwkbaE%2F%2F7SzcVo2yA%3D%3D',
        quote_plus("numOfRows"): '1000',
        quote_plus('pageNo'): '1',
        quote_plus('dataType'): 'JSON',
        quote_plus('base_date'): today_date,
        quote_plus('base_time'): today_time,
        quote_plus('nx'): x.pop(0),
        quote_plus('ny'): y.pop(0)
    })
    # URL 데이터 파싱
    request = Request(CallBackURL + unquote(params))
    # API를 통해 데이터 GET
    response_body = urlopen(request).read()
    # JSON으로 변환
    data = json.loads(response_body)
    item_data = data['response']['body']['items']['item']
    return item_data

def send_data(local):
    count = 0
    weather_data = dict() 
    item_data = get_data()
    for item in item_data:
        weather_data['지역'] = str(local)
        weather_data['타임'] = item['fcstDate'] +'-' +item['fcstTime']
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
        if count == 3:
            cursor.execute("INSERT INTO seoul(local, date, tmp, rain, sky) VALUES ('"+weather_data['지역']+"', '" +
                        weather_data['타임']+"', '" + weather_data['기온']+"', '"+weather_data['강수확률']+"', '"+
                        weather_data['하늘']+"') ON DUPLICATE KEY UPDATE tmp='" +weather_data['기온'] + "'," + 
                        "rain='" + weather_data['강수확률']+"'," + "sky='" + weather_data['하늘']+"';")
            db.commit()
            count = 0
    print(local + "data sended")

if __name__ == "__main__":
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    unique_date = set_date() # 데이터 정제 후 유니크키 추출
    local, x, y = weather_local.find_location() # 엑셀에서 구마다 지역이름, x, y
    for name in local:
        send_data(name)
    print("dada finished")
    db.close()
    