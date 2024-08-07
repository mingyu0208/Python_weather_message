import json
import requests
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from res import kakao_tokken

#  토큰 가져오기
KAKAO_TOKKEN_FILENAME = 'D:/학교/ALL/코딩/포트폴리오/프로젝트 모음/파이썬특강(2024.07.24)/날씨 정보 맛집 추천 프로젝트/res/kakao_token.json'
tokens = kakao_tokken.load_tokens(KAKAO_TOKKEN_FILENAME)

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

headers = {
    "Authorization" : "Bearer " + tokens['access_token'] 
}

data = {
    "template_object" : json.dumps({
        "object_type": "text",
        "text" : "Hello, KAKAO",
        "link" : {"web_rul" : "www.naver.com"}
    })
}

response = requests.post(url, headers=headers, data=data)
if response.status_code !=200:
    print("Error! ", response.json())
else:
    print("메시지 발송 성공")
