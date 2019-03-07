# -*- coding: utf-8 -*-
"""
配置
"""
import pymysql
import json
import time
from dingtalkchatbot.chatbot import DingtalkChatbot

db = pymysql.connect(host='192.168.1.100', port=3306, user='qcc', passwd='VhO4fNROWARt', db='spider_qichacha',charset='utf8')
cursor = db.cursor()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    ,'content-type':'application/json'
    ,'charset':'utf-8'
    ,'Accept-Encoding':'gzip'
    ,'Host':'xcx.qichacha.com'
    ,'Connection':'closed'
    ,'Server': 'Tengine'
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
def check_token():
    try:         #如果一开始就没有token，自定义一个token=123
        tokens = get_tokens()
        tokens.reverse()
        token = tokens.pop()
    except IndexError:
        #print 'Please provide a available token'
        #exit()
        token = '123'
    return token

token = check_token()


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



#发消息
def send_msg():
    now_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=%s' %dingtoken
    xiaoding = DingtalkChatbot(webhook)
    xiaoding.send_text(msg='QCC-token失效'+now_time, is_at_all=True)




#ding talk token
dingtoken="8bbe93c55b7aaff815f620f7331a1cfe06f46163a132b4c30877b47b9d28c109"



print 'token = ' + token
