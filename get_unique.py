# -*- coding: utf-8 -*-
"""
获取获取(商业公司)第一级的keyno并存到数据库中,keyno就是url中的unique
"""
import pymysql
import config
import requests
import json
import time


headers = config.headers
token = config.token

db = pymysql.connect(host='192.168.1.100', port=3306, user='root', passwd='123123', db='spider_qichacha',charset='utf8')
cursor = db.cursor()

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
        a = ','.join(com) #将set类型转为str
        js = requests.get('https://xcx.qichacha.com/wxa/v1/base/advancedSearchNew?searchKey=%s&token=%s' % (a, token), headers=headers)
        js = js.text
        js = json.loads(js)
        result = js.get('result')
        Result = result.get('Result')[0]
        keyno = Result.get('KeyNo')

        #print keyno
        time.sleep(1)
        id = list(company_dict.keys())[list(company_dict.values()).index(com)]  #根据values得到对应的key值
        #update_time = time.strftime("%Y-%m-%d %H:%M:%S")
        update_time = time.time()

        cursor.execute("update source_company set key_no='%s',update_time=%s where id='%s'" %(keyno,update_time,id))
        db.commit()


try:
    get_keyno()
except:
    print 'False'
    exit()


