import requests
import json
import datetime


#requests 요청을 날릴 사이트 주소
weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?'

service_key = 'SN38WJfkXEtaRNKyTUhjQKX6yzFvh1nFWx3X9OO0L%2BUmrF2PwVQwFs3QGorCfoafuyIe2L8U66I8k4TPK9d4%2FA%3D%3D'

base_date = datetime.datetime.today().strftime('%Y%m%d')

base_time = '0800'
nx = '99'
ny = '90'


payload = 'serviceKey=' + service_key + '&' + \
    "dataType=json" + '&' + \
    "base_date=" + base_date + '&' + \
    "base_time=" + base_time + '&' + \
    "nx=" + nx + '&' + \
    "ny=" + ny


res = requests.get(weather_url + payload)

try:
    items = res.json().get('response').get('body').get('items')
    print(items)
except:
    print('날씨 정보 요처 실패: ', res.text)


