# https://flask-docs-kr.readthedocs.io/ko/latest/ -flask 공식 문서
# https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.save.html -werkzeug 공식문서
from urllib.request import Request, urlopen
from flask import Flask, jsonify, render_template, request, send_file
from flask.helpers import send_from_directory
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from datetime import datetime
from bs4 import BeautifulSoup
from lib import weather_db, weather_local
# import pyautogui as pg
from lib import weather_db, weather_local, speech_tts, speech_stt
import werkzeug, os, sys, time, ctypes, threading, weather_data, weather_now, weather_kakao, json, requests
global db, cursor

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.config import Config as cfg

sys.path.append(cfg.OPENPIBO_PATH + '/edu')
from pibo import Edu_Pibo

app = Flask(__name__) 
api = Api(app)
pibo = Edu_Pibo()
count = 0

"""                    템플릿 부분                    """
# 홈
@app.route('/')
def render_home():
    return render_template('home.html')


# 발신
@app.route('/message_send', methods = ['GET', "POST"])
def render_message_send():
    if request.method == 'POST':
        from weather_now import set_nowdate
        db, cursor = weather_db.db_connecting('root', 'qwe123')
        nick = request.form['nick']
        msg = request.form['msg']
        now_date = set_nowdate()
        try:
            cursor.execute("INSERT INTO faq(now_date, user, message) VALUES('"+now_date+"', '"
                        +nick+"', '"+msg+"')")
            db.commit()
            db.close()
        except:
            print('error')
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

@app.route('/kakao_me')
def kakao_me_login():
    return render_template('kakao_me.html')

@app.route('/kakao_friends')
def kakao_friends_login():
    return render_template('kakao_friends.html')

# 토큰
@app.route('/kakao/oauth?code=<code>')
def oatuh(code):
    print(code)
    # global user_code
    # code = str(request.args.get('code'))
    # url = "https://kauth.kakao.com/oauth/token"
    # payload = "grant_type=authorization_code&client_id=0a8a356679801891a01bdc324ec32d77&redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2Foauth&code="+str(code)
    # headers = {
    #     'Content-Type': "application/x-www-form-urlencoded",
    #     'Cache-Control': "no-cache",
    # }
    # response = requests.request("POST", url, data=payload, headers=headers)
    # access_token = json.loads(((response.text).encode('utf-8')))['access_token']
    # print(response.text)
     
    # url = "https://kapi.kakao.com/v1/user/signup"
    # headers.update({'Authorization' : "Bearer " + str(access_token)})
    # response = requests.request("POST", url, headers=headers)
    # print(response.text)
    
    # url = "https://kapi.kakao.com/v2/user/me"
    # response = requests.request("POST", url, headers=headers)
    # print(response.text)
    return render_template('kakao.html')

@app.route('/check_me', methods = ['POST', 'GET'])
def kakao_check_me():
    if request.method == 'POST':
        code = request.form['code']
        print(code)
        weather_kakao.kakao_to_me_get_mytokens(code)
        weather_kakao.kakao_me_token()
        user = weather_kakao.kakao_me_check()
        return render_template('check_me.html', user = user)
    else:
        return render_template('check_me.html')

@app.route('/check_owner', methods = ['POST', 'GET'])
def kakao_check_owner():
    if request.method == 'POST':
        code = request.form['code']
        print(code)
        weather_kakao.kakao_to_friends_get_mytokens(code)
        weather_kakao.kakao_owner_token()
        user = weather_kakao.kakao_owner_check()
        weather_kakao.kakao_friends_read()
        return render_template('check_owner.html', user = user)
    else:
        return render_template('check_owner.html')


@app.route('/check_friend', methods = ['POST', 'GET'])
def kakao_check_friend():
    if request.method == 'POST':
        code = request.form['code']
        print(code)
        weather_kakao.kakao_to_friends_get_friendstokens(code)
        weather_kakao.kakao_friends_token()
        user = weather_kakao.kakao_friends_check()
        return render_template('check_friend.html', user = user)
    else:
        return render_template('check_friend.html')



    
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
            # pg.alert(text='업로드 성공', title='결과', button='OK')
            return render_template('upload.html')
        except:
            # pg.alert(text='업로드에 실패했습니다', title='결과', button='OK')
            return render_template('upload.html')

# 파일 다운로드
@app.route('/download', methods = ['GET', 'POST'])
def download_file():
    files_list = os.listdir("./uploads")
    if request.method == 'POST':
        sw = 0
        for x in files_list:
            if(x==request.form['file']):
                sw=1
        try:
            path = "./uploads/"
            # pg.alert(text='다운로드 성공', title='결과', button='OK')
            return send_file(path + request.form['file'],
                    attachment_filename = request.form['file'],
                    as_attachment=True) 
        except:
            # pg.alert(text='파일명을 확인해주세요', title='결과', button='OK')
            return render_template('download.html', files=files_list)

# 파일 삭제
@app.route('/delete', methods = ['POST'])
def delete_file():
    files_list = os.listdir("./uploads")
    if request.method == 'POST':
        try:
            path = "./uploads/"
            os.remove(path+"{}".format(request.form['file']))
            # pg.alert(text='삭제됐습니다', title='결과', button='OK')
            files_list = os.listdir("./uploads")
            return render_template('delete.html', files=files_list)
        except:
            # pg.alert(text='파일명을 확인해주세요', title='결과', button='OK')
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
    # today_time = weather_data.set_date()
    return render_template('weather.html', data = weather, date = time, time = ctime, count = count)

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
    speech_tts.tts_test('날씨와 관련해서 무엇을 도와드릴까요?')
    ret = speech_stt.stt_test()
    sentence = ret['data']
    local = weather_local.find_speak_local(sentence)
    x, y = weather_local.find_speak_location(local)

    if ('카톡' in sentence) or ('보내' in sentence):
        if (x and y) != 0:
            speech_tts.tts_test('누구한테 보낼까요?')
            ret = speech_stt.stt_test()
            sentence = ret['data']

            if  ('황도규' in sentence) or ('나' in sentence):
                weather = weather_now.send_data_user(local, x, y)
                weather_kakao.kakao_me_send(weather)
                speech_tts.tts_test('나한테 카톡으로 보냈어')
                pibo_reset()

            else:
                weather = weather_now.send_data_user(local, x, y)
                weather_kakao.kakao_friends_send(weather, sentence)
                speech_tts.tts_test(sentence+'에게 카톡으로 보냈어')
                pibo_reset()

            
        else:
            speech_tts.tts_test('카톡으로 보낼 지역을 찾지 못했어')
            pibo_reset()

    else:
        if (x and y) != 0:
            weather_now.send_data_user(local, x, y)
            speech_tts.tts_test(local+'의 현재 날씨를 말해줄게')
            speech_tts.tts_test(weather_now.weather_to_speak(local))
            pibo_reset()
        else:
            speech_tts.tts_test('원하는 지역을 찾지 못했어')
            pibo_reset()


def msg_device(msg): # 터치센서 감지하면 작동
    global count # 중요
    print(f'message : {msg}')
    check = msg.split(':')[1]

    if check.find('touch') > -1:

        count += 1
    if count > 1:
        t2 = threading.Thread(target=pibo_welcome, args=(3,))
        t2.daemon = True
        t2.start()
        speak_to_user()
        count = 0
        time.sleep(3)

def device_thread_test(): # pibo 쓰레드
    ret = pibo.start_devices(msg_device)

def pibo_reset(): # 초기화
    pibo.eye_on('aqua')
    pibo.set_motion('stop', 2)

def pibo_eye(color):
    pibo.eye_on(color)

def pibo_welcome(num):
    pibo.set_motion('welcome', num)

if __name__ == '__main__': 
    pibo_reset()
    speech_tts.tts_test('서버를 실행하겠습니다.')
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    device_thread_test()

    # app.run(debug = False, port = 8000)
    app.run(host = '0.0.0.0', debug = False, port = 8000)

    # html을 파이보와 연계되게 날씨 누르면 파이보에서 대답 


    

