import requests, json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from lib import weather_local, weather_db
from flask import request
import webbrowser, selenium, weather_now
from selenium import webdriver


def kakao_to_me_get_mytokens(code):
    url = 'https://kauth.kakao.com/oauth/token'
    authorize_code = code
    data = {
        'grant_type':'authorization_code',
        'client_id':'0a8a356679801891a01bdc324ec32d77',
        'redirect_uri':'https://localhost:8000/kakao/oauth',
        'code': authorize_code,
        }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    with open("kakao_code_me.json","w") as fp:
        json.dump(tokens, fp)

def kakao_to_friends_get_mytokens(code):
    url = 'https://kauth.kakao.com/oauth/token'
    authorize_code = code
    data = {
        'grant_type':'authorization_code',
        'client_id':'91d3b37e4651a9c3ab0216abfe877a50',
        'redirect_uri':'https://localhost:8000/kakao/oauth',
        'code': authorize_code,
        }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    with open("kakao_code_friends_me.json","w") as fp:
        json.dump(tokens, fp)

def kakao_to_friends_get_friendstokens( code):
    url = 'https://kauth.kakao.com/oauth/token'
    authorize_code = code
    data = {
        'grant_type':'authorization_code',
        'client_id':'91d3b37e4651a9c3ab0216abfe877a50',
        'redirect_uri':'https://localhost:8000/kakao/oauth',
        'code': authorize_code,
        }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    with open("kakao_code_friends_friends.json","w") as fp:
        json.dump(tokens, fp)

def set_message(weather_message):
    message = ''
    for key, value in weather_message.items():
        message += str(key)
        message += ': '+str(value)+ '\n'
    return message

def kakao_me_token():
    with open("kakao_code_me.json","r") as fp:
        tokens = json.load(fp)
    url="https://kapi.kakao.com/v1/user/access_token_info"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    response = requests.post(url, headers=headers)
    print(response.text)
    return response.text

def kakao_owner_token():
    with open("kakao_code_friends_me.json","r") as fp:
        tokens = json.load(fp)
    url="https://kapi.kakao.com/v1/user/access_token_info"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    response = requests.post(url, headers=headers)
    print(response.text)
    return response.text

def kakao_friends_token():
    with open("kakao_code_friends_friends.json","r") as fp:
        tokens = json.load(fp)
    url="https://kapi.kakao.com/v1/user/access_token_info"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    response = requests.post(url, headers=headers)
    print(response.text)
    return response.text
    
def kakao_me_check():
    with open("kakao_code_me.json","r") as fp:
        tokens = json.load(fp)
    url="https://kapi.kakao.com/v2/user/me"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    response = requests.post(url, headers=headers)
    print(response.text)
    return response.text

def kakao_owner_check():
    with open("kakao_code_friends_me.json","r") as fp:
        tokens = json.load(fp)
    url="https://kapi.kakao.com/v2/user/me"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    response = requests.post(url, headers=headers)
    print(response.text)
    return response.text

def kakao_friends_check():
    with open("kakao_code_friends_friends.json","r") as fp:
        tokens = json.load(fp)
    url="https://kapi.kakao.com/v2/user/me"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    response = requests.post(url, headers=headers)
    print(response.text)
    return response.text

def kakao_me_send(weather_message):
    with open("kakao_code_me.json","r") as fp:
        tokens = json.load(fp)
    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers={
        "Authorization" : "Bearer " + tokens["access_token"]
    }
    message = set_message(weather_message)
    data={
        "template_object": json.dumps({
            "object_type":"text",
            "text":message,
            "link":{
                "web_url":"http://192.168.1.143:8000/"
            }
        })
    }
    try:
        print(message)
        response = requests.post(url, headers=headers, data=data)
        response.status_code
        print('kakao to me sended')
    except:
        print('kakao token check')

def kakao_friends_send(weather_message, friend):
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    user = []
    count = 0
    with open("kakao_code_friends_me.json","r") as fp:
        tokens = json.load(fp)
    print(tokens)
    friend_url = "https://kapi.kakao.com/v1/api/talk/friends"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    result = json.loads(requests.get(friend_url, headers=headers).text)
    friends_list = result.get("elements")
    sql = "SELECT * FROM friends"
    cursor.execute(sql)
    for i in cursor:
        data = []
        data.append(i['name'])
        data.append(i['uuid'])
        user.append(data)
    
    for name in user:
        if friend in name[0]:
            friend_id = name[1]
            print(friend_id)

    try:
        send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
        message = set_message(weather_message)
        data={
            'receiver_uuids':'["{}"]'.format(friend_id),
            "template_object": json.dumps({
                "object_type":"text",
                "text":message,
                "link":{
                    "web_url":"www.naver.com"
                }
            })
        }
        print(message)
        response = requests.post(send_url, headers=headers, data=data)
        response.status_code
        print('kakao to friend sended')
        
    except:
        print('kakao token check')
    

def kakao_friends_read():
    db, cursor = weather_db.db_connecting('root', 'qwe123')
    with open("kakao_code_friends_me.json","r") as fp:
        tokens = json.load(fp)
    friend_url = "https://kapi.kakao.com/v1/api/talk/friends"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    result = json.loads(requests.get(friend_url, headers=headers).text)
    friends_list = result.get("elements")
    for friend in friends_list:
        cursor.execute("INSERT INTO friends(id, name, uuid, image) VALUES ('"+
            str(friend['id'])+"', '" +friend['profile_nickname']+"', '"+
            friend['uuid']+"', '" +friend['profile_thumbnail_image']+"') ON DUPLICATE KEY UPDATE name='"+
            friend['profile_nickname']+"', uuid='" +friend['uuid']+"', image='"+friend['profile_thumbnail_image']+"';")
        db.commit()
        print(friend['profile_nickname']+"success")
    db.close()

if __name__=='__main__':
    # local, x, y = weather_local.find_user_location()
    # weather = weather_now.send_data_user(local, x, y)
    # kakao_user_check()
    kakao_friends_read()
    # kakao_me_send(weather)
    # kakao_friends_send(weather, 'ghkdtjsgml')






