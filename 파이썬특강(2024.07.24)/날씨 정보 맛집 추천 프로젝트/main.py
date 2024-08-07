# 1. 접근권한 설절
#  2. API 사용 권한 받기


import requests

url = 'https://kauth.kakao.com/oauth/token'


data = {
    "grant_type" : "authorization_code",
    "client_id" : "5d6375ed074895b0e79b46afe080a347",
    "redirect_uri" : "https://localhost.com",
    "code" : "DhOYo9FbY-Gmtw1U7zxMuMVXqi6zOr2JU29MpFOwHN9ABK1W4rx9AwAAAAQKKwzSAAABkO0IqS-SBpCp5rpDbg"
}
response = requests.post(url, data=data)

if response.status_code != 200:
    print('error!', response.json())
else:
    tokken = response.json()
    print(tokken)



