# https://flask-docs-kr.readthedocs.io/ko/latest/ -flask 공식 문서
# https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.save.html -werkzeug 공식문서
from flask import Flask, jsonify, render_template, request, send_file
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from datetime import datetime
from lib import weather_db, weather_local
import weather_data
import werkzeug, os

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

# 날씨
@app.route('/weather')
def weather_alarm():
    now_weather()
    return render_template('weather.html')




def now_weather():
    count = 0
    weather = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
    local, x, y = weather_local.find_location()
    unique_key = weather_db.nowtime()
    sql = 'SELECT * FROM seoul WHERE date = %s'
    cursor.execute(sql, (unique_key))
    # print([i for i in cursor])
    
    for i in cursor:
        weather[count] = i
        count += 1
    # weather[숫자]인 이유는 한글로 표현했을경우 for문을 돌려야함
    print(weather[0])
    print(weather[10])
    print(weather[24])
    
    
        
    
    # for name in local:
    #     sql = 'SELECT * FROM seoul WHERE date = %s'
    #     # print(sql, (unique_key))
    #     print(cursor.execute(sql, (unique_key)))
    #     print([i for i in cursor])


if __name__ == '__main__': 
    app.run(debug = True, port = 108)
    # app.run(host = '0.0.0.0', debug = True)