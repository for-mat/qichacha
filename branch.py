# -*- coding: UTF-8 -*-

import proxy_pool
import headers_pool
import config
import pymysql
import requests
import json
import time
import re
import random


db = pymysql.connect(host='192.168.1.100', port=3306, user='qcc', passwd='VhO4fNROWARt', db='spider_qichacha',charset='utf8')
cursor = db.cursor()


class branch(object):
    #获取company_branch中的unique
    def get_uniques(self):
        cursor.execute('select branch_no,id from company_branch where status=0')
        results = cursor.fetchall()
        for i in results:
            keyno=i[0]
            id=i[1]
            if keyno==None:
                cursor.execute('update company_branch set status=1 where id=%s' %id)
            else:
                return keyno
        db.commit()




        #keyno = results[0]
        #return results

    #向company_branch中插入数据
    def insert_data(self):
        unique = self.get_uniques()
        create_time = time.time()
        # 获取包含所有字段的元组
        p_num = 1
        #self.proxy = proxy_pool.proxy
        while True:
            try:
                self.proxy = proxy_pool.change_proxy()
                proxy = self.proxy
                html = requests.get('https://www.qichacha.com/firm_%s'%unique,headers=headers_pool.requests_headers(),proxies=proxy,timeout=2)
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,requests.exceptions.SSLError,requests.exceptions.ConnectionError):
                self.proxy = proxy_pool.change_proxy()
                global proxy
                proxy = self.proxy
                print 'changing proxy...%s...%s'%(p_num,self.proxy)
                p_num+=1
                continue
            break
        response = html.text
        print response
        # tuple = (unique,name, phone, website, email, province, city, county, address, intro, registered_capital, actual_capital,operating_state, establishment_date, uscc, taxpayer_number, registration_number, organization_code, type,industry, approval_date, registration_authority, area, english_name, used_name, insurancer_count,staff_count, operation_period, operation_scope,create_time,1)
        #cursor.execute('update company_branch set name=%s, phone=%s, website=%s, email=%s, province=%s, city=%s, county=%s, address=%s, intro=%s, registered_capital=%s, actual_capital=%s, operating_state=%s, establishment_date=%s, uscc=%s, taxpayer_number=%s, registration_number=%s, organization_code=%s, type=%s, industry=%s, approval_date=%s, registration_authority=%s, area=%s, english_name=%s, used_name=%s, insurancer_count=%s, staff_count=%s, operation_period=%s, operation_scope=%s, create_time=%s, status=%s where branch_no=%s' % company_fields)
        #db.commit()
        #cursor.execute('select id from company_branch where branch_no=%s' % unique)
        #branch_id = cursor.fetchone()[0]
        #print '第%s条插入成功,已插入%s条,剩余%s条'%(branch_id,n,len(uniques)-n)
        time.sleep(1.5)

while True:
    branch().insert_data()



