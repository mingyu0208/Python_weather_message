import requests
import json
import datetime
import random

vilage_weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?'

service_key = "40oswQz5MVL0by5JgCsA3tPCBmPFBUgYgdDsbcA6iThEntlrokTQCtGQhjCHt3sY8v2iJdQBTVgHFbX4TnCnrg%3D%3D"
base_date = datetime.datetime.today().strftime("%Y%m%d")
base_time = "0800"
nx = "61"
ny = "125"

payload = "serviceKey=" + service_key + "&" + \
    "dataType=json" + "&" + \
    "base_date=" + base_date + "&" + \
    "base_time=" + base_time + "&" + \
    "nx=" + nx + "&" + \
    "ny=" + ny

sky_code = {
    "1" : "맑음",
    "3" : "구름많음",
    "4" : "흐림",
}

pty_code = {
    "0" : "없음",
    "1" : "비",
    "2" : "비/눈",
    "3" : "눈",
    "4" : "소나기",
}

data = dict()
data['date'] = base_date
weather = dict()

res = requests.get(vilage_weather_url + payload)
try:
    items = res.json().get('response').get('body').get('items')
    for item in items['item']:
        # 기온
        if item['category'] == 'TMP':
            weather['tmp'] = item['fcstValue']
        # 하늘상태
        if item['category'] == 'SKY':
            weather['code'] = item['fcstValue']
            weather['sky'] = sky_code[item['fcstValue']]
        
        # 강수상태
        if item['category'] == 'PTY':
            weather['code'] = item['fcstValue']
            weather['pty'] = pty_code[item['fcstValue']]
except:
    print("날씨 정보 요청 실패 : ", res.text)

data['weather'] = weather
# print(data['weather'])


# ============

def get_pm10_state(pm10_value):
    if pm10_value < 30:
        pm10_state = "좋음"
    elif pm10_value < 80:
        pm10_state = "보통"
    elif pm10_value < 150:
        pm10_state = "나쁨"
    else:
        pm10_state = "매우 나쁨"
    return pm10_state

def get_pm25_state(pm25_value):
    if pm25_value < 15:
        pm25_state = "좋음"
    elif pm25_value < 35:
        pm25_state = "보통"
    elif pm25_value < 75:
        pm25_state = "나쁨"
    else:
        pm25_state = "매우 나쁨"
    return pm25_state


dust_url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?'

service_key = "40oswQz5MVL0by5JgCsA3tPCBmPFBUgYgdDsbcA6iThEntlrokTQCtGQhjCHt3sY8v2iJdQBTVgHFbX4TnCnrg%3D%3D"

payload = "serviceKey=" + service_key + "&" + \
    "returnType=json" + "&" + \
    "stationName=우현동" + "&" + \
    "dataTerm=DAILY" + "&" + \
    "ver=1.0"

# pm10과 pm2.5 수치 가져오기

res = requests.get(dust_url + payload)
result = res.json()
dust = dict()

if(res.status_code == 200) and (result['response']['header']['resultCode'] == '00'):
    dust['PM10'] = {'value' : int(result['response']['body']['items'][0]['pm10Value'])}
    dust['PM2.5'] = {'value' : int(result['response']['body']['items'][0]['pm25Value'])}

    # PM10 미세먼지 30 80 150
    pm10_value = dust.get('PM10').get('value')
    pm10_state = get_pm10_state(pm10_value)

    pm25_value = dust.get('PM2.5').get('value')
    pm25_state = get_pm25_state(pm25_value)

    dust.get('PM10')['state'] = pm10_state
    dust.get('PM2.5')['state'] = pm25_state
else:
    print('미세먼지 가져오기 실패 : ', result['response']['header']['resultMsg'])

data['dust'] = dust

# 리스트
def getFoodsList(weather, pm10, pm20):
    rain = '파전,부대찌개,막걸리,수제비,칼국수,잔치국수,해물탕,아구찜,동태탕,삼겹살,햄버거'.split(',')
    snow = "스테이크,와인,햄버거,파스타,삼겹살,샌드위치,스시,김밥,랍스터,짜장면,망고빙수".split(',')
    if weather == '1':
        weather_state = "Case1"
        food_list = random.sample(rain, k = len(rain))
    elif weather == '3':
        weather_state = "Case2"
        food_list = random.sample(snow, k = len(snow))
    else:
        weather_state = 'Case3'
        food_list = ['']
    return weather_state, food_list


def naver_local_search(query, display):
    headers = {
        "X-Naver-Client-Id" : 'UhaZO6V1eUDDeKZZfCjx',
        "X-Naver-Client-Secret" : 'Km2wPkNj32'
    }

    param = {
        "sort" : "comment",
        "query" : query,
        "display": display   
    }

    naver_local_url = "https://openapi.naver.com/v1/search/local.json?"

    res = requests.get(naver_local_url, headers=headers, params=param)
    places = res.json().get('items')
    return places


weather = data.get('weather').get('ptyCode')
dust_pm10 = data.get('dust').get('PM10').get('state')
dust_pm20 = data.get('dust').get('PM2.5').get('state')


weather_state, foods_list = getFoodsList(weather, dust_pm10, dust_pm20)

location= str(input())
# location = ""

recommands = []
for food in foods_list:
    query = location + " " + food + " 맛집"
    result_list = naver_local_search(query,3)

    if len(result_list) > 0:
        if weather_state == "Case3":
            recommands = result_list
            break
        else:
            recommands.append(result_list[0])
        if len(recommands) == 3:
            break

text = f"""
# 날씨 정보
기온 : {data['weather']['tmp']}
강수 : {data['weather']['pty']}
하늘 : {data['weather']['sky']}
미세먼지 {data['dust']['PM10']['value']} / {data['dust']['PM10']['state']}
초미세먼지 : {data['dust']['PM2.5']['value']} / {data['dust']['PM2.5']['state']}
"""

for item in recommands:
    foodText = f"""
# 날씨 추천 맛집 정보
상호명 : {item['title']}
음식종류 : {item['category']}
주소: {item['address']}
"""
print(text)    
print(foodText)
