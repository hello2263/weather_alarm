# https://flask-docs-kr.readthedocs.io/ko/latest/ -flask 공식 문서
# https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.save.html -werkzeug 공식문서
from urllib.request import Request, urlopen
from flask import Flask, jsonify, render_template, request, send_file
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from datetime import datetime
from bs4 import BeautifulSoup
from lib import weather_db, weather_local
import json, requests
# from lib import weather_db, weather_local, speech_tts, speech_stt
import werkzeug, os, sys, time, weather_data, weather_now, ctypes
global db, cursor

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.config import Config as cfg

sys.path.append(cfg.OPENPIBO_PATH + '/edu')
# from pibo import Edu_Pibo

app = Flask(__name__) 
api = Api(app)
# count = 0


"""                    템플릿 부분                    """
# 홈
@app.route('/')
def render_home():
    return render_template('home.html')

# 수신
@app.route('/message_receive')
def render_message_receive():
    return render_template('message_receive.html')

# 발신
@app.route('/message_send')
def render_message_send():
    return render_template('message_send.html')

# 업로드
@app.route('/upload')
def render_file_uploade():
    return render_template('upload.html')

# 다운로드
@app.route('/download')
def render_file_download():
    files_list = os.listdir("./uploads")
    return render_template('download.html', files=files_list) #files라는 변수에 files_list를 담음

# 목록
# @app.route('/list')
# def render_file_list(): # 따로 list.html을 만들지 않고 list를 표시하게 하는 방법
#     file_list = os.listdir("./uploads")
#     html = """<a href="/">홈</a><br><br>"""
#     html += "file_list: {}".format(file_list)
#     return html

# 삭제
@app.route('/delete')
def render_file_delete():
    files_list = os.listdir("./uploads")
    return render_template('delete.html', files=files_list)

# 카카오
@app.route('/kakao')
def kakao_login():
    return render_template('kakao.html')

# 토큰
@app.route('/oauth')
def oatuh():
    code = str(request.args.get('code'))
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code&client_id=91d3b37e4651a9c3ab0216abfe877a50&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth&code="+str(code)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']
    print(response.text)
     
    url = "https://kapi.kakao.com/v1/user/signup"
    headers.update({'Authorization' : "Bearer " + str(access_token)})
    response = requests.request("POST", url, headers=headers)
    print(response.text)
    
    url = "https://kapi.kakao.com/v2/user/me"
    response = requests.request("POST", url, headers=headers)
    print(response.text)
    return (response.text)
    
"""                    구동 부분                      """
# 메세지 받기
@app.route('/message_receive', methods = ['POST']) 
def message_receive():
    value = request.form['message'] # 일반적으로 form태그를 이용하여 POST 방식으로 전달받을 때 주로 사용
    return render_template('message_receive.html', data = value)

# 파일 업로드
@app.route('/upload', methods = ['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        try:
            f = request.files['file']
            f.save('./uploads/' + secure_filename(f.filename)) # 파일명을 보호하기위한 함수, 지정된 경로에 파일 저장
            message = ctypes.windll.user32.MessageBoxW(None, '업로드 성공!','success', 0)
            return render_template('upload.html')
        except:
            message = ctypes.windll.user32.MessageBoxW(None, '파일명을 확인해주세요!','error', 0)
            if message == 1:
                print('ok')
            return render_template('upload.html')

# 파일 다운로드
@app.route('/download', methods = ['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        files_list = os.listdir("./uploads")
        try:
            path = "./uploads/"        
            send_file(path + request.form['file'],
                    attachment_filename = request.form['file'],
                    as_attachment=True) #파일을 경로에 저장하는데 파일 명은 request.form으로 받고 as_attachment인자 찾아보기
            message = ctypes.windll.user32.MessageBoxW(None, '다운로드 성공!','success', 0)
            return render_template('download.html', files=files_list)
        except:
            message = ctypes.windll.user32.MessageBoxW(None, '파일명을 확인해주세요!','error', 0)
            return render_template('download.html', files=files_list)

# 파일 삭제
@app.route('/delete', methods = ['POST'])
def delete_file():
    if request.method == 'POST':
        files_list = os.listdir("./uploads")
        try:
            path = "./uploads/"
            os.remove(path+"{}".format(request.form['file']))
            message = ctypes.windll.user32.MessageBoxW(None, '삭제 성공!','success', 0)
            return render_template('delete.html', files=files_list)
        except:
                message = ctypes.windll.user32.MessageBoxW(None, '파일명을 확인해주세요!','error', 0)
                if message == 1:
                    print('ok')
                return render_template('delete.html', files=files_list)

# 유저의 날짜선택
@app.route('/weather/<user_date>', methods=['GET', 'POST'])
def weather_user_date(user_date):
    ctime, count = count_time()
    weather = now_weather(user_date)
    return render_template('weather.html', data = weather, date = user_date, time = ctime, count = count)

# 날씨
@app.route('/weather', methods=['GET', 'POST'])
def weather_alarm():
    ctime, count = count_time()
    time = weather_db.nowtime()
    weather = now_weather(time)
    today_time = weather_data.set_date()
    return render_template('weather.html', data = weather, date = today_time, time = ctime, count = count)


def now_weather(time): # html로 각 구의 기상을 담고있는 리스트 안의 딕셔너리를 만들어주는 함수
    count = 0
    weather = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
    local, x, y = weather_local.find_location()
    unique_key = time
    sql = 'SELECT * FROM seoul WHERE date = %s'
    cursor.execute(sql, (unique_key))
    for i in cursor:
        weather[count] = i
        count += 1
    return weather

def count_time(): # html에서 콤보박스에 표시될 날짜들 정하는 함수
    flag = 2
    count = 0
    count_date = []
    date = weather_data.set_date()
    sql = 'SELECT date FROM seoul WHERE local = "강남구" AND date >= %s'
    cursor.execute(sql, (date))
    for i in cursor:
        if flag == 2:
            count_date.append(i)
            count += 1
            flag = 0
        else:
            flag += 1
    return count_date, count

def speak_to_user(): # Pibo가 user에게 날씨 말해줌
    speech_tts.tts_test('날씨를 알고싶은 서울의 구를 말해줘')
    ret = speech_stt.stt_test()
    sentence = ret['data']
    local = weather_local.find_speak_local(sentence)
    x, y = weather_local.find_speak_location(local)
    if (x and y) != 0:
        weather_now.send_data_user(local, x, y)
        speech_tts.tts_test(local+'의 현재 날씨를 말해줄게')
        speech_tts.tts_test(weather_now.weather_to_speak(local))
        pibo_reset()
    else:
        pibo.eye_on('red')
        speech_tts.tts_test('원하는 지역을 찾지 못했어')
        pibo_reset()

def msg_device(msg): # 터치센서 감지하면 작동
    global count # 중요
    pibo.set_motion('stop', 1)
    print(f'message : {msg}')
    check = msg.split(':')[1]
    
    if check.find('touch') > -1:
        count +=1

    if count > 1:
        pibo.eye_on('purple')
        pibo.set_motion('welcome', 3)
        speak_to_user()
        count = 0

def device_thread_test(): # 쓰레드
    ret = pibo.start_devices(msg_device)

def pibo_reset(): # 초기화
    pibo.eye_on('aqua')
    pibo.set_motion('stop', 1)

if __name__ == '__main__': 
    # pibo = Edu_Pibo()
    # pibo_reset()
    # speech_tts.tts_test('서버를 실행할게')
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    # device_thread_test()

    app.run(debug = False, port = 8000)
    # app.run(host = '0.0.0.0', debug = False, port = 8000)



    # 동작 끝날때까지 기다리는법 -> TTS단에서 스레드로 플래그
    # 모션쪽에만 스레드
    
    # css 5
    
    # 단어 서칭


    # 발표자료 전문화 -> 플로우차트나 db쪽 발표자료 검토
    # vscode를 발표때 이용
