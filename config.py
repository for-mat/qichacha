# -*- coding: utf-8 -*-
"""
配置
"""
import pymysql
import json
import time

db = pymysql.connect(host='192.168.1.100', port=3306, user='root', passwd='123123', db='spider_qichacha',charset='utf8')
cursor = db.cursor()

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
def get_tokens():

    cursor.execute('select wx_token from token_list where token_status=1')
    db.commit()
    results = cursor.fetchall()
    tokens = []
    for i in results:
        wx_token = i[0]
        tokens.append(wx_token)
    return tokens

tokens = get_tokens()
token_num = 0
tokens.reverse()
token = tokens.pop()

def change_token():
    global token_num
    global tokens
    global token
    token_num += 1
    if token_num > 3:
        token = json.dumps(token, encoding="utf-8", ensure_ascii=False)
        cursor.execute('update token_list set token_status=0 where wx_token=%s' % token)
        db.commit()
        while len(tokens) == 0:
            print 'need to add token~'
            time.sleep(5)
            tokens = get_tokens()
        else:
                print 'ok'
        token = tokens.pop()
        token_num = 0










#tokens = ['9c749a0100ea9bff4e24925346e7d08e']



