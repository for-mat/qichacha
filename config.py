# -*- coding: utf-8 -*-
"""
配置
"""
import json
import requests
#11
headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 8.0.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x260703FA) NetType/4G Language/zh_CN Process/appbrand2'
    ,'content-type':'application/json'
    ,'charset':'utf-8'
    ,'Accept-Encoding':'gzip'
    ,'referer':'https://servicewechat.com/wx395200814fcd7599/25/page-frame.html'
    ,'Host':'xcx.qichacha.com'
    ,'Connection':'Keep-Alive'
    ,'Server': 'Tengine'
    ,'Set-Cookie': 'acw_tc=7ae1439b15460757517813698e31f0ddcc8ef1c06b5d1b4961e6890acf;path=/;HttpOnly;Max-Age=2678401'
}

get_token_header = {
'charset': 'utf-8'
,'Accept-Encoding': 'gzip'
,'referer': 'https://servicewechat.com/wx395200814fcd7599/26/page-frame.html'
,'content-type': 'application/json'
,'User-Agent' : 'Mozilla/5.0 (Linux; Android 8.0.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x260703FA) NetType/WIFI Language/zh_CN Process/appbrand2'
,'Host': 'xcx.qichacha.com'
,'Connection': 'Keep-Alive'
#,'code': '023SkcIA12Zfhc0xUBLA13d1IA1SkcIg'
,'Server': 'Tengine'
,'Content-Type': 'application/json'
,'Access-Control-Allow-Origin': '*'
,'Access-Control-Allow-Headers': 'X-Requested-With'
,'Access-Control-Allow-Methods': 'PUT,POST,GET,DELETE,OPTIONS'
,'Timing-Allow-Origin': '*'
}

token = 'af0dcb374ec309461ccc0cbf4cabf89e'

data = {'code': '033kq38o03ymjl1Uyoao0q918o0kq381'}

#js = requests.post('https://xcx.qichacha.com/wxa/v1/admin/xcxGetAccessToken',headers = get_token_header)
#js = js.text
#print js
#exit()
