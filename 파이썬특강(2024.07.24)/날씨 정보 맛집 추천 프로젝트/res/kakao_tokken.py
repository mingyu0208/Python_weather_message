import json
import requests
import datetime
import os


KAKAO_TOKKEN_FILENAME = 'D:/학교/ALL/코딩/포트폴리오/프로젝트 모음/파이썬특강(2024.07.24)/날씨 정보 맛집 추천 프로젝트/res/kakao_token.json'

def save_tokens(filename, tokens):
    with open(filename, 'w') as fp:
        json.dump(tokens, fp)

def load_tokens(filename):
    with open(filename) as fp:
        tokens = json.load(fp)
    return tokens


def update_tokens(app_key, filename):
    tokens = load_tokens(filename)

    url = 'https://kauth.kakao.com/oauth/token'

    data = {
    "grant_type" : "refresh_token",
    "client_id" : app_key,
    "refresh_token" : tokens['refresh_token']}
    
    response = requests.post(url, data=data)

    if response.status_code != 200:
        print("Erro!", response.json())
        tokens = None

    else:
        print(response.json())
        now = datetime.datetime.now().strftime("%Y%m%d_%H%m%S")
        backup_filename = filename + "." + now
        os.rename(filename, backup_filename)
        tokens['access_token'] = response.json()['access_token']
        save_tokens(filename, tokens)
    return tokens


KAKAO_APP_KEY = "5d6375ed074895b0e79b46afe080a347"
tokens = update_tokens(KAKAO_APP_KEY, KAKAO_TOKKEN_FILENAME)
save_tokens (KAKAO_TOKKEN_FILENAME, tokens)


