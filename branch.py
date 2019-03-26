# -*- coding: UTF-8 -*-

import proxy_pool
import headers_pool
import pymysql
import requests
import json
import time
from bs4 import BeautifulSoup
from lxml import etree
import codecs
proxy = {}

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = pymysql.connect(host='192.168.1.100', port=3306, user='qcc', passwd='VhO4fNROWARt', db='spider_qichacha',charset='utf8')
cursor = db.cursor()


class branch(object):
    #获取company_branch中的unique
    def get_uniques(self):
        cursor.execute('select branch_no,id from branch_test where status=0')
        db.commit()
        results = cursor.fetchall()
        for i in results:
            keyno=i[0]
            id=i[1]
            if keyno==None:
                cursor.execute('update branch_test set status=1 where id=%s' %id)
            else:
                return keyno
        db.commit()




        #keyno = results[0]
        #return results

    #向company_branch中插入数据
    def insert_data(self):
        unique = self.get_uniques()
        print 'unique = '+ unique
        create_time = time.time()
        # 获取包含所有字段的元组
        p_num = 1
        #self.proxy = proxy_pool.proxy
        while True:
            try:
                cookie = {
                    'Hm_lpvt_3456bee468c83cc63fb5147f119f1075': str(int(time.time()))
                    ,'QCCSESSID':'kh50oeettqgbbphg0k57p37t40'

                }

                self.proxy = proxy_pool.change_proxy()
                proxy = self.proxy
                html = requests.get('https://www.qichacha.com/firm_%s'%unique,headers=headers_pool.requests_headers(),proxies=proxy,cookies=cookie,timeout=2)
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,requests.exceptions.SSLError,requests.exceptions.ConnectionError):
                self.proxy = proxy_pool.change_proxy()
                global proxy
                proxy = self.proxy
                print 'changing proxy...%s...%s'%(p_num,self.proxy)
                p_num+=1
                continue
            break
        response = html.content
        print response

        #有时会获取不到页面,触发异常处理
        if '<script>window.location.href' in response:
            raise UnboundLocalError

        s1 = etree.HTML(response)

        #获取字段

        #注册资本
        registered_capital = s1.xpath('//*[@id="Cominfo"]/table[2]/tr[1]/td[2]//text()')[0].strip().encode('utf-8')
        if registered_capital == '-':
            registered_capital = None
        registered_capital = json.dumps(registered_capital, encoding="utf-8", ensure_ascii=False)


        test = s1.xpath('//*[@id="company-top"]/div[2]/div[2]/div[3]/div[1]/span[1]/span[2]/span//text()')
        print test
        print registered_capital

        #unique = json.dumps(unique, encoding="utf-8", ensure_ascii=False)
        #cursor.execute('update branch_test set registered_capital=%s,status=1 where branch_no=%s' %(registered_capital,unique))
        #db.commit()

        time.sleep(1)
n=0
while True:
    try:
        branch().insert_data()
        n+=1
        print 'n=' + str(n)
    except UnboundLocalError:
        print '返回页面错误'
        time.sleep(2)
        continue



