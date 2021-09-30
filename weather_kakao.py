# import requests
# import json

# url = 'https://kauth.kakao.com/oauth/token'
# rest_api_key = '5cf2fc401b2e16fcedfffb4f8f763dbe'
# redirect_uri = 'https://example.com/oauth'
# authorize_code = 'LBEo0jdtz4zksnZ8GVJtjlV6c0kqRPN6rvNyrfJirZZxx7R58tqui-vjSo6dhF8Sca75WgorDSAAAAF8NSTPXA'
# data = {
#     'grant_type':'authorization_code',
#     'client_id':rest_api_key,
#     'redirect_uri':redirect_uri,
#     'code': authorize_code,
#     }
# response = requests.post(url, data=data)
# tokens = response.json()
# print(tokens)
# with open("kakao_code.json","w") as fp:
#     json.dump(tokens, fp)


# with open("kakao_code.json","r") as fp:
#     ts = json.load(fp)
# print(ts)
# print(ts["access_token"])


# with open("kakao_code.json","r") as fp:
#     tokens = json.load(fp)
# url="https://kapi.kakao.com/v2/api/talk/memo/default/send"
# headers={
#     "Authorization" : "Bearer " + tokens["access_token"]
# }
# data={
#     "template_object": json.dumps({
#         "object_type":"text",
#         "text":"Hello, world!",
#         "link":{
#             "web_url":"www.naver.com"
#         }
#     })
# }
# response = requests.post(url, headers=headers, data=data)
# response.status_code


# import requests

# url = 'https://kauth.kakao.com/oauth/token'
# rest_api_key = 'bff90e404d329c0e106632e1cdd42cd9'
# redirect_uri = 'https://example.com/oauth'
# authorize_code = 'cECq8_eCIjQ4kWqlzksYh3Ei3SJpCYEx3-lr9drNbIM1KZ7Q9Ji0F0w0PBpwmbRxcZpMfQo9dRsAAAF8NYy1Kw'

# data = {
#     'grant_type':'authorization_code',
#     'client_id':rest_api_key,
#     'redirect_uri':redirect_uri,
#     'code': authorize_code,
#     }

# response = requests.post(url, data=data)
# tokens = response.json()
# print(tokens)

# # json 저장
# import json
# with open(r"C:/python/weather_alarm/kakao_code.json","w") as fp:
#     json.dump(tokens, fp)


# import requests
# import json

# #1.
# with open(r"C:/python/weather_alarm/kakao_code.json","r") as fp:
#     tokens = json.load(fp)

# # print(tokens)
# # print(tokens["access_token"])

# friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

# # GET /v1/api/talk/friends HTTP/1.1
# # Host: kapi.kakao.com
# # Authorization: Bearer {ACCESS_TOKEN}

# headers={"Authorization" : "Bearer " + tokens["access_token"]}

# result = json.loads(requests.get(friend_url, headers=headers).text)

# print(type(result))
# print("=============================================")
# print(result)
# print("=============================================")
# friends_list = result.get("elements")
# print(friends_list)
# # print(type(friends_list))
# print("=============================================")
# print(friends_list[0].get("uuid"))
# friend_id = friends_list[0].get("uuid")
# print(friend_id)



import requests
import json

with open(r"C:/python/weather_alarm/kakao_code.json","r") as fp:
    tokens = json.load(fp)
# print(tokens)
# print(tokens["access_token"])

friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

# GET /v1/api/talk/friends HTTP/1.1
# Host: kapi.kakao.com
# Authorization: Bearer {ACCESS_TOKEN}

headers={"Authorization" : "Bearer " + tokens["access_token"]}

result = json.loads(requests.get(friend_url, headers=headers).text)

print(type(result))
print("=============================================")
print(result)
print("=============================================")
friends_list = result.get("elements")
print(friends_list)
# print(type(friends_list))
print("=============================================")
print(friends_list[0].get("uuid"))
friend_id = friends_list[0].get("uuid")
print(friend_id)

send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

data={
    'receiver_uuids': '["{}"]'.format(friend_id),
    "template_object": json.dumps({
        "object_type": "feed",
        "content": {
            "title": "오늘의 디저트",
            "description": "아메리카노, 빵, 케익",
            "image_url": "http://mud-kage.kakao.co.kr/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg",
            "image_width": 640,
            "image_height": 640,
            "link": {
                "web_url": "http://www.daum.net",
                "mobile_web_url": "http://m.daum.net",
                "android_execution_params": "contentId=100",
                "ios_execution_params": "contentId=100"
            }
        }
    })
}

response = requests.post(send_url, headers=headers, data=data)
response.status_code
















