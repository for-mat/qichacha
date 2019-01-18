# -*- coding: utf-8 -*-
"""
配置
"""
import pymysql
import json
import time
from dingtalkchatbot.chatbot import DingtalkChatbot

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
    if token_num > 800:
        token = json.dumps(token, encoding="utf-8", ensure_ascii=False)
        cursor.execute('update token_list set token_status=0 where wx_token=%s' % token)
        db.commit()
        while len(tokens) == 0:
            print 'need to add token~'
            send_msg()
            time.sleep(60)
            tokens = get_tokens()
        else:
                print 'ok'
        token = tokens.pop()
        token_num = 0

now_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

#发消息
def send_msg():
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=%s' %dingtoken
    xiaoding = DingtalkChatbot(webhook)
    xiaoding.send_text(msg='QCC-token失效'+now_time, is_at_all=True)




#ding talk token
dingtoken="f3d898ede5e9f8482fe4919e05aabfa173c7bec6ca9ff0e2b1d392d989d90710"




