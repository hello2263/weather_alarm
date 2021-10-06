import requests, json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from lib import weather_local
import weather_now, weather_server
from flask import request
import webbrowser
import selenium
from selenium import webdriver

def kakao_get_code():
    URL = "https://kauth.kakao.com/oauth/authorize?client_id=0a8a356679801891a01bdc324ec32d77&redirect_uri=https://192.168.0.19:8000/kakao&response_type=code"
    webbrowser.open(URL)
    # driver=webdriver.Chrome('D:/chromedriver.exe')
    # print(driver.current_url)
    # user_url = request.url
    # url_index = user_url.index('code=') + 5

def kakao_get_tokens(path, api, redirect_uri, code):
    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = api
    authorize_code = code
    data = {
        'grant_type':'authorization_code',
        'client_id':rest_api_key,
        'redirect_uri':redirect_uri,
        'code': authorize_code,
        }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    with open("kakao_code_"+path+".json","w") as fp:
        json.dump(tokens, fp)

def set_message(weather_message):
    message = ''
    for key, value in weather_message.items():
        message += str(key)
        message += ': '+str(value)+ '\n'
    return message

def kakao_token_check():
    with open("kakao_code_friends.json","r") as fp:
        tokens = json.load(fp)
    url="https://kapi.kakao.com/v1/user/access_token_info"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    response = requests.post(url, headers=headers)
    print(response.text)
    return response.text
    
def kakao_user_check():
    with open("kakao_code_friends.json","r") as fp:
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
                "web_url":"www.naver.com"
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

def kakao_friends_send(weather_message):
    with open("kakao_code_friends.json","r") as fp:
        tokens = json.load(fp)
    print(tokens)
    friend_url = "https://kapi.kakao.com/v1/api/talk/friends"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    result = json.loads(requests.get(friend_url, headers=headers).text)
    friends_list = result.get("elements")
    print(friends_list)
    try:
        friend_id = friends_list[0].get("uuid")
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

if __name__=='__main__':
    # kakao_get_code()
    # kakao_get_tokens('me', '0a8a356679801891a01bdc324ec32d77', 'https://example.com/oauth', 'ADht31kbxUvBs48Gm2PCQf8uiKOmhHtX3rEmvnEEP5rtPNFUOlK5Om9rRWfZTFzGPCeFMQo9dJcAAAF8TquA7w')
    # kakao_get_tokens('friends', '91d3b37e4651a9c3ab0216abfe877a50', 'https://example.com/oauth', code)
    # local, x, y = weather_local.find_user_location()
    # weather = weather_now.send_data_user(local, x, y)
    kakao_user_check()
    # kakao_me_send(weather)
    # kakao_friends_send(weather)





