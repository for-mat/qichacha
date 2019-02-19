# -*- coding: utf-8 -*-
"""
获取获取(商业公司)第一级的keyno并存到数据库中,keyno就是url中的unique
"""
import pymysql
import config
import requests
import json
import time
import proxy_pool


db = pymysql.connect(host='192.168.1.100', port=3306, user='root', passwd='123123', db='spider_qichacha',charset='utf8')
cursor = db.cursor()

headers = config.headers
tokens = config.tokens
token_num = config.token_num
token = config.token
proxy = proxy_pool.proxy


# 获取数据库中的id和name并加入字典
def get_source_company():
    cursor.execute('select id,name from source_company where status=0')
    results = cursor.fetchall()
    company_dict = {}
    for i in results:
        id = i[0]
        name = i[1]
        company_dict[id] = {name}
    return company_dict

#获取(商业公司)第一级的keyno并存到数据库中
def get_keyno():
    company_dict = get_source_company()
    for com in company_dict.values():
        # 判断token使用次数，使用token超过1000次，就换一个token使用
        config.change_token()
        a = ','.join(com) #将set类型转为str
        js = requests.get('https://xcx.qichacha.com/wxa/v1/base/advancedSearchNew?searchKey=%s&token=%s' % (a, token), headers=headers, proxies=proxy)
        js = js.text
        js = json.loads(js)
        result = js.get('result')
        Result = result.get('Result')[0]
        keyno = Result.get('KeyNo')

        #print keyno
        time.sleep(2.5)
        id = list(company_dict.keys())[list(company_dict.values()).index(com)]  #根据values得到对应的key值
        #update_time = time.strftime("%Y-%m-%d %H:%M:%S")
        update_time = time.time()

        cursor.execute("update source_company set key_no='%s',update_time=%s where id='%s'" %(keyno,update_time,id))
        db.commit()


while True:
    try:
        get_keyno()
    except:
        print 'token faild or user forbidden'
        token = json.dumps(token, encoding="utf-8", ensure_ascii=False)
        cursor.execute('update token_list set token_status=0 where wx_token=%s' % token)
        token = config.token
        db.commit()
        print "please add token"
        config.send_msg()
        time.sleep(120)


