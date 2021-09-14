# https://flask-docs-kr.readthedocs.io/ko/latest/ -flask 공식 문서
# https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.save.html -werkzeug 공식문서
from flask import Flask, jsonify, render_template, request, send_file
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from datetime import datetime
from lib import weather_db

import werkzeug, os

# jsonify?
# json data를 내보내도록 제공하는 flask의 함수
# jsonify가 편하지만 지원되지 않는 형식(한글 등)을 주고 받으려면 별도의 인코더가 필요함.
# Flask처럼 웹서버로 쓰이는 환경에서 이런식으로 데이터를 내려보내면
# 프론트엔드에서는 다시 이 코드포인트들을 문자열로 변환해야 한다는 문제점이 생긴다.

app = Flask(__name__) # 단일 모듈을 사용하면 __name__을 사용해야함 (?), flask class 인스턴스 생성
api = Api(app)

# @app.route('/') -> http://localhost:5000/을 가리키며
# @app.route('/hello') -> http://localhost:5000/hello를 가리킴

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
@app.route('/list')
def render_file_list(): # 따로 list.html을 만들지 않고 list를 표시하게 하는 방법
    file_list = os.listdir("./uploads")
    html = """<a href="/">홈</a><br><br>"""
    html += "file_list: {}".format(file_list)
    return html

# 삭제
@app.route('/delete')
def render_file_delete():
    files_list = os.listdir("./uploads")
    return render_template('delete.html', files=files_list)

# 날씨
@app.route('/weather')
def render_weather():
    return render_template('weather.html')




"""                    구동 부분                      """
# 메세지 받기
@app.route('/message_receive', methods = ['POST']) # method가 이 페이지에서 하는 동작을 의미하는 것 같음
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

# 날씨
@app.route('/weather_alarm', methods = ['GET'])
def weather_alarm():
    if request.method == 'POST':
        db, cursor = weather_db.db_connecting('root', 'qwe123')
        if now.month < 10:
            today_month = '0'+str(now.month)
        else:
            today_month = str(now.month)

        if now.day < 10:
            today_day = '0'+str(now.day)
        else:
            today_day = str(now.day)
        date = str(now.year)+today_month+str(today_day)

        if now.hour < 10:
            hour = '0'+str(now.hour)
        else:
            hour = str(now.hour)
        time = hour+'00'

        return """time : <br><br>""".format(time)




# @app.route('/user/<userName>') # URL뒤에 <>을 이용해 가변 경로를 적는다, 이런식도 가능함
# def hello_user(userName):
#     return 'Hello, %s'%(userName)

# 여러 줄을 텍스트로 입력하고 싶을때
# https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=sonicheroes1&logNo=220676215649


if __name__ == '__main__': 
    app.run(host = '0.0.0.0', debug = True)
