# 村里街路門牌查詢-桃園市桃園區
import requests, json, time, random
from fake_useragent import UserAgent 
from datetime import datetime
import ddddocr
from bs4 import  BeautifulSoup as bs

#先找captchaKey
url_doorplate = 'https://www.ris.gov.tw/info-doorplate/app/doorplate/query?cityCode=68000000&searchType=date'
res_doorplate = requests.post(url_doorplate)

obj_doorplate = bs(res_doorplate.text, 'lxml')
captcha = obj_doorplate.find_all('input', id="captchaKey_captchaKey")[0]["value"]
print(f'captcahkey: {captcha}')

# timestamp
dt_now = datetime.now()
ts = str(int(datetime.timestamp(dt_now)*1000))
print(f'timestamp: {ts}')
time.sleep(2)

# 利用captcahkey & ts 請求驗證碼
verifypic_url = f'https://www.ris.gov.tw/info-doorplate/captcha/image?CAPTCHA_KEY={captcha}&time={ts}'
r_pic=requests.get(verifypic_url)

#將圖片下載下來確認
# with open('verifypic','wb') as f:
#     f.write(r_pic.content)

ocr = ddddocr.DdddOcr()
pic = ocr.classification(r_pic.content)
pic_upper = str.upper(pic)
print(f'驗證碼： {pic_upper}')
time.sleep(2)

# 先爬第一頁
ua = UserAgent()

cookies = {
    'JSESSIONID': '02FE1CABD99B0B16BF7862729E4CBEEA.sris-aw-info-doorplate-2',
    '_ga': 'GA1.3.787644152.1680751765',
    '_gid': 'GA1.3.79966356.1680751765',
}

headers = {
    'User-Agent': ua.random
}

data_first_page = {
    'searchType': 'date',
    'cityCode': '68000000',
    'tkt': '-1',
    'areaCode': '68000010',
    'village': '',
    'neighbor': '',
    'sDate': '112-03-01',
    'eDate': '112-03-31',
    '_includeNoDate': 'on',
    'registerKind': '0',
    'captchaInput': pic_upper,
    'captchaKey': captcha,
    'floor': '',
    'lane': '',
    'alley': '',
    'number': '',
    'number1': '',
    'ext': '',
    '_search': 'false',
    'nd': ts,
    'rows': '50',
    'page': '1',
    'sidx': '',
    'sord': 'asc',
}

    
url_page = 'https://www.ris.gov.tw/info-doorplate/app/doorplate/inquiry/date'
rs = requests.Session()
response_first = rs.post(url=url_page, 
                   cookies=cookies,
                   headers=headers,
                   data=data_first_page)

# 往下一頁的token
token = json.loads(response_first.json()['errorMsg'])['token']
print(f'token: {token}')

# 總頁數
page = response_first.json()['total']
print(f'total page: {page}')

# 擷取第一頁資料
doorplate_all = []
doorplate_first = response_first.json()['rows']
for ele in doorplate_first:
    doorplate_all.append(ele)
time.sleep(2)


# 接下來的頁數
for i in range(2,page+1):
    data = {
        'searchType': 'date',
        'cityCode': '68000000',
        'tkt': '-1',
        'areaCode': '68000010',
        'village': '',
        'neighbor': '',
        'sDate': '112-03-01',
        'eDate': '112-03-31',
        '_includeNoDate': 'on',
        'registerKind': '0',
        'captchaInput': pic_upper,
        'captchaKey': captcha,
        'floor': '',
        'lane': '',
        'alley': '',
        'number': '',
        'number1': '',
        'ext': '',
        '_search': 'false',
        'nd': ts,
        'rows': '50',
        'page': i,
        'sidx': '',
        'sord': 'asc',
        'token': token
        }

    url_page = 'https://www.ris.gov.tw/info-doorplate/app/doorplate/inquiry/date'
    rs = requests.Session()
    response_next = rs.post(url=url_page, 
                       cookies=cookies,
                       headers=headers,
                       data=data)
    
    token = json.loads(response_next.json()['errorMsg'])['token']
    doorplate = response_next.json()['rows']
    for element in doorplate:
        doorplate_all.append(element)
    time.sleep(random.uniform(2,5))

print(len(doorplate_all))
