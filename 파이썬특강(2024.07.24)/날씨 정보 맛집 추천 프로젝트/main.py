# 1. 접근권한 설절
#  2. API 사용 권한 받기


import requests

url = 'https://kauth.kakao.com/oauth/token'


data = {
    "grant_type" : "{}",
    "client_id" : "{}",
    "redirect_uri" : "https://localhost.com",
    "code" : "{}"
}
response = requests.post(url, data=data)

if response.status_code != 200:
    print('error!', response.json())
else:
    tokken = response.json()
    print(tokken)



