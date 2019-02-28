# -*- coding: utf-8 -*-

'''读取company_branch表，获取分支机构的信息，并插入company_branch'''
import pymysql
import config
from getdata import spider
import time
import json
import proxy_pool
import headers_pool
import requests

db = pymysql.connect(host='192.168.1.100', port=3306, user='root', passwd='123123', db='spider_qichacha',charset='utf8')
cursor = db.cursor()

headers = config.headers
#token = config.token

tokens = config.tokens
token_num = config.token_num
token = config.token

spider = spider()
#unique = '287d9caa36e789820710a762fac79ad5'
#print spider.get_fields(unique)




def get_uniques():
    cursor.execute('select branch_no from company_branch where status=0')
    results = cursor.fetchall()
    uniques = []
    for i in results:
        keyno = i[0]
        uniques.append(keyno)
    return uniques

def insert_company():
    uniques = get_uniques()

    for unique in uniques:
        if unique == None:
            continue

        #判断token使用次数，使用token超过1000次，就换一个token使用
        config.change_token()

        create_time = time.time()
        # 获取包含所有字段的元组
        while True:
            try:
                headers = headers_pool.requests_headers()
                (fields, result) = spider.get_fields(unique, token,proxy,headers)
            except (requests.exceptions.ProxyError,requests.exceptions.ConnectTimeout):
                global proxy
                proxy = proxy_pool.change_proxy()
                continue
            break
        #(fields,result) = spider.get_fields(unique,token)
        # 转为列表，并将unique,create_time,status加入列表
        company_fields = list(fields)
        unique = json.dumps(unique, encoding="utf-8", ensure_ascii=False)
        company_fields.append(create_time)
        company_fields.append(1)
        company_fields.append(unique)
        # 转为元组，插入数据
        company_fields = tuple(company_fields)

        #tuple = (unique,name, phone, website, email, province, city, county, address, intro, registered_capital, actual_capital,operating_state, establishment_date, uscc, taxpayer_number, registration_number, organization_code, type,industry, approval_date, registration_authority, area, english_name, used_name, insurancer_count,staff_count, operation_period, operation_scope,create_time,1)
        cursor.execute('update company_branch set name=%s, phone=%s, website=%s, email=%s, province=%s, city=%s, county=%s, address=%s, intro=%s, registered_capital=%s, actual_capital=%s, operating_state=%s, establishment_date=%s, uscc=%s, taxpayer_number=%s, registration_number=%s, organization_code=%s, type=%s, industry=%s, approval_date=%s, registration_authority=%s, area=%s, english_name=%s, used_name=%s, insurancer_count=%s, staff_count=%s, operation_period=%s, operation_scope=%s, create_time=%s, status=%s where branch_no=%s' % company_fields)

        time.sleep(2.5)
        db.commit()

#token失效判断，避免程序中断
while True:
    try:
        insert_company()
    except:
        print 'token faild or user forbidden'
        token = json.dumps(token, encoding="utf-8", ensure_ascii=False)
        cursor.execute('update token_list set token_status=0 where wx_token=%s' % token)
        token = config.token
        db.commit()
        print "please add token"
        config.send_msg()
        time.sleep(120)