import requests
import json
from lib import weather_local
import weather_now, weather_server
from flask import request

def kakao_get_tokens(path, api, code):
    url = 'https://kauth.kakao.com/oauth/token'
    rest_api_key = api
    redirect_uri = 'https://example.com/oauth'
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

def kakao_me_send(weather_message):
    with open("kakao_code_me.json","r") as fp:
        tokens = json.load(fp)
    print(tokens)
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
    print(message)
    response = requests.post(url, headers=headers, data=data)
    response.status_code
    print('kakao to me sended')

def kakao_friends_send(weather_message):
    with open(r"C:/python/weather_alarm/kakao_code_friends.json","r") as fp:
        tokens = json.load(fp)
    print(tokens)
    friend_url = "https://kapi.kakao.com/v1/api/talk/friends"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    result = json.loads(requests.get(friend_url, headers=headers).text)
    print("=============================================")
    print(result)
    print("=============================================")
    friends_list = result.get("elements")
    print(friends_list)
    print("=============================================")
    print(friends_list[0].get("uuid"))
    friend_id = friends_list[0].get("uuid")
    print(friend_id)
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


if __name__=='__main__':
    kakao_get_tokens('me', '0a8a356679801891a01bdc324ec32d77', weather_server.user_code)
    # kakao_get_tokens('friends', 'bff90e404d329c0e106632e1cdd42cd9', '2jQRTJM7MMjvdB0ttiJcqytn14Fi3-JPmg6mqWb-AJ2C3pp-04gui5IaNsOAusyQsdGKcQo9dNoAAAF8ObneQw')
    local, x, y = weather_local.find_user_location()
    weather = weather_now.send_data_user(local, x, y)
    kakao_me_send(weather)
    # kakao_friends_send(weather)
















