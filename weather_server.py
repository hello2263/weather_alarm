# https://flask-docs-kr.readthedocs.io/ko/latest/ -flask 공식 문서
# https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.save.html -werkzeug 공식문서
from urllib.request import Request, urlopen
from flask import Flask, jsonify, render_template, request, send_file
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from datetime import datetime
from bs4 import BeautifulSoup
from lib import weather_db, weather_local, speech_tts
import werkzeug, os, sys, time, weather_data, weather_now
global db, cursor 

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.config import Config as cfg

sys.path.append(cfg.OPENPIBO_PATH + '/edu')
from pibo import Edu_Pibo

app = Flask(__name__) 
api = Api(app)

# db접속
db, cursor = weather_db.db_connecting('root', 'qwe123')

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


"""                    구동 부분                      """
# 메세지 받기
@app.route('/message_receive', methods = ['POST']) 
def message_receive():
    value = request.form['message'] # 일반적으로 form태그를 이용하여 POST 방식으로 전달받을 때 주로 사용
    return render_template('message_receive.html', data = value)

# 파일 업로드
@app.route('/fileUpload', methods = ['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('./uploads/' + secure_filename(f.filename)) # 파일명을 보호하기위한 함수, 지정된 경로에 파일 저장
        return """<a href="/">홈</a><br><br>"""+'uploads 디렉토리 -> 파일 업로드 성공'

# 파일 다운로드
@app.route('/fileDownload', methods = ['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        sw = 0 # sw라는 변수가 작동하는지 의문이 듬 -> 빼고 실험해봐야 함
        files_list = os.listdir("./uploads")
        for x in files_list:
            if(x==request.form['file']):
                sw=1
        path = "./uploads/"
        return send_file(path + request.form['file'],
				attachment_filename = request.form['file'],
				as_attachment=True) #파일을 경로에 저장하는데 파일 명은 request.form으로 받고 as_attachment인자 찾아보기

# 파일 삭제
@app.route('/fileDelete', methods = ['POST'])
def delete_file():
    if request.method == 'POST':
        path = "./uploads/"
        os.remove(path+"{}".format(request.form['file']))
        return """<a href="/">홈</a><br><br>"""+'파일 삭제 성공'

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

def speak_to_user():
    local, x, y = weather_local.find_user_location()
    weather_now.send_data_user(local, x, y)
    speech_tts.tts_test(weather_now.weather_to_speak(local))

def msg_device(msg):
    print(f'message : {msg}')
    check = msg.split(':')[1]

    if check.find('touch') > -1:
        ret_text = pibo.stt()
        
        ret = decode(ret_text['data'])

        speak(ret)
        pibo.set_motion('wave1', 1)

def device_thread_test():
    ret = pibo.start_devices(msg_device)
    print(f'ret : {ret}')


if __name__ == '__main__': 
    pibo = Edu_Pibo()
    pibo.eye_on('pink')
    print('45124')
    pibo.set_motion('welcome', 1)
    pibo.eye_on('purple')
    pibo.set_motion('stop', 1)
    
    print('start check device')
    device_thread_test()


    # speech_tts.tts_test('현재 서버를 실행중이야')
    # app.run(debug = True, port = 108)
    # app.run(host = '0.0.0.0', debug = True)

    # speak_to_user()


    # 구문별 띄어서 말하는 법
    # 스레드처럼 동시에 돌리는 법
    # 가끔 speak 후 종료가 안됨
    # 좀 더 빠르게 실행하는 법
    # 2번 서버를 실행함