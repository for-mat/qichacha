# -*- coding: utf-8 -*-
"""
获取网页字段信息
"""

import os
import json
import requests
import chardet
import config
import re
import time
import pymysql
import random

db = pymysql.connect(host='192.168.1.100', port=3306, user='root', passwd='123123', db='spider_qichacha',charset='utf8')
cursor = db.cursor()


# 获取所有unique
def get_uniques():
    cursor.execute('select key_no from source_company where status =0')
    results = cursor.fetchall()
    uniques = []
    for i in results:
        keyno = i[0]
        uniques.append(keyno)
    return uniques

headers = config.headers
#token = config.token
tokens = config.tokens
token_num = config.token_num
token = config.token



#first_keynos = get_keyno_unique.get_keyno()

#print json.dumps(a, encoding="utf-8", ensure_ascii=False)

class spider(object):

    #获取字段
    def get_fields(self,unique,token):
        #获取网页，取出json中的公司信息
        js = requests.get('https://xcx.qichacha.com/wxa/v1/base/getMoreEntInfo?unique=%s&token=%s' %(unique,token),headers = headers)
        js = js.text
        js = json.loads(js)
        result = js.get('result')
        self.result = result
        #company = result.get('Company')


        #获取字段
        self.name = result.get('Name')
        self.phone = result.get('ContactInfo').get('PhoneNumber')

        try:
            self.website = result.get('ContactInfo').get('WebSite')[0].get('Url')
        except TypeError:
            self.website = None

        self.email = result.get('ContactInfo').get('Email')
        self.province = result.get('Area').get('Province')
        self.city = result.get('Area').get('City')
        self.county = result.get('Area').get('County')
        self.address = result.get('Address')

        reg = re.compile('<[^>]*>')
        intro = result.get('ProfileDesc')
        self.intro = reg.sub('',intro).strip()

        self.registered_capital = result.get('RegistCapi')
        self.actual_capital = result.get('RecCap')
        self.operating_state = result.get('Status')
        self.establishment_date = result.get('StartDate')
        self.uscc = result.get('CreditCode')
        self.taxpayer_number = result.get('TaxNo')
        self.registration_number = result.get('No')
        self.organization_code = result.get('OrgNo')
        self.type = result.get('EconKind')
        self.industry = result.get('Industry').get('Industry')

        approval_date = result.get('CheckDate')
        if approval_date < 0:
            approval_date = 0
        approval_date = time.localtime(approval_date)
        self.approval_date = time.strftime("%Y-%m-%d",approval_date)

        self.registration_authority = result.get('BelongOrg')
        self.area = result.get('Area').get('Province')
        self.english_name =result.get('EnglishName')

        used_name_list =result.get('OriginalName')
        used_name = ""
        if type(used_name_list) == list:
            for i in used_name_list:
                used_name = used_name +(i.get('Name')) + " "
                self.used_name = used_name
        else:
            self.used_name = None

        try:
            self.insurancer_count = result.get('CommonList')[3].get('Value')
        except:
            self.insurancer_count = None

        self.staff_count = result.get('profile').get('Info')

        StartDate = result.get('StartDate')
        StartDate = str(StartDate)
        EndDate = result.get('EndDate')
        EndDate = str(EndDate)
        if EndDate == '0':
            EndDate = 'Indefinite'
        self.operation_period = StartDate + ' unitl ' + EndDate

        self.operation_scope = result.get('Scope')

        name = json.dumps(self.name, encoding="utf-8", ensure_ascii=False)
        phone = json.dumps(self.phone, encoding="utf-8", ensure_ascii=False)
        website = json.dumps(self.website, encoding="utf-8", ensure_ascii=False)
        email = json.dumps(self.email, encoding="utf-8", ensure_ascii=False)
        province = json.dumps(self.province, encoding="utf-8", ensure_ascii=False)
        city = json.dumps(self.city, encoding="utf-8", ensure_ascii=False)
        county = json.dumps(self.county, encoding="utf-8", ensure_ascii=False)
        address = json.dumps(self.address, encoding="utf-8", ensure_ascii=False)
        intro = json.dumps(self.intro, encoding="utf-8", ensure_ascii=False)
        registered_capital = json.dumps(self.registered_capital, encoding="utf-8", ensure_ascii=False)
        actual_capital = json.dumps(self.actual_capital, encoding="utf-8", ensure_ascii=False)
        operating_state = json.dumps(self.operating_state, encoding="utf-8", ensure_ascii=False)
        establishment_date = json.dumps(self.establishment_date, encoding="utf-8", ensure_ascii=False)
        uscc = json.dumps(self.uscc, encoding="utf-8", ensure_ascii=False)
        taxpayer_number = json.dumps(self.taxpayer_number, encoding="utf-8", ensure_ascii=False)
        registration_number = json.dumps(self.registration_number, encoding="utf-8", ensure_ascii=False)
        organization_code = json.dumps(self.organization_code, encoding="utf-8", ensure_ascii=False)
        type1 = json.dumps(self.type, encoding="utf-8", ensure_ascii=False)
        industry = json.dumps(self.industry, encoding="utf-8", ensure_ascii=False)
        approval_date = json.dumps(self.approval_date, encoding="utf-8", ensure_ascii=False)
        registration_authority = json.dumps(self.registration_authority, encoding="utf-8", ensure_ascii=False)
        area = json.dumps(self.area, encoding="utf-8", ensure_ascii=False)
        english_name = json.dumps(self.english_name, encoding="utf-8", ensure_ascii=False)
        used_name = json.dumps(self.used_name, encoding="utf-8", ensure_ascii=False)
        insurancer_count = json.dumps(self.insurancer_count, encoding="utf-8", ensure_ascii=False)
        staff_count = json.dumps(self.staff_count, encoding="utf-8", ensure_ascii=False)
        operation_period = json.dumps(self.operation_period, encoding="utf-8", ensure_ascii=False)
        operation_scope = json.dumps(self.operation_scope, encoding="utf-8", ensure_ascii=False)



        fields = (name, phone, website, email, province, city, county, address, intro, registered_capital, actual_capital,operating_state, establishment_date, uscc, taxpayer_number, registration_number, organization_code, type1,industry, approval_date, registration_authority, area, english_name, used_name, insurancer_count,staff_count, operation_period, operation_scope)
        return fields,result


    def get_branches(self):
        # 得到分支机构的keyno列表
        result = self.result
        branches = result.get('Branches')
        branch_keyno = []
        for i in branches:
            keyno = i.get('KeyNo')
            name = i.get('Name')
            # print str(json.dumps(name, encoding="utf-8", ensure_ascii=False))
            branch_keyno.append(keyno)
        return branch_keyno

    #根据商业公司往三个表中插入数据
    def insert_company(self):
        uniques = get_uniques()
        for unique in uniques:

            create_time = time.time()
            # 判断token使用次数，使用token超过1000次，就换一个token使用
            config.change_token()
            # 获取包含所有字段的元组
            (fields,result) = self.get_fields(unique,token)
            # 转为列表，并将unique,create_time,status加入列表
            company_fields = list(fields)
            unique = json.dumps(unique, encoding="utf-8", ensure_ascii=False)
            company_fields.insert(0, unique)
            company_fields.append(create_time)
            company_fields.append(1)
            # 转为元组，插入数据
            company_fields = tuple(company_fields)


            #tuple = (unique,name, phone, website, email, province, city, county, address, intro, registered_capital, actual_capital,operating_state, establishment_date, uscc, taxpayer_number, registration_number, organization_code, type,industry, approval_date, registration_authority, area, english_name, used_name, insurancer_count,staff_count, operation_period, operation_scope,create_time,1)

            cursor.execute('insert into company(company_no,name,phone,website,email,province,city,county,address,intro,registered_capital,actual_capital,operating_state,establishment_date,uscc,taxpayer_number,registration_number,organization_code,type,industry,approval_date,registration_authority,area,english_name,used_name,insurancer_count,staff_count,operation_period,operation_scope,create_time,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' % company_fields)
            #cursor.execute('insert into company(company_no,name,phone,website,email,province,city,county,address,intro,registered_capital,actual_capital,operating_state,establishment_date,uscc,taxpayer_number,registration_number,organization_code,type,industry,approval_date,registration_authority,area,english_name,used_name,insurancer_count,staff_count,operation_period,operation_scope,create_time,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %(unique,name,phone,website,email,province,city,county,address,intro,registered_capital,actual_capital,operating_state,establishment_date,uscc,taxpayer_number,registration_number,organization_code,type,industry,approval_date,registration_authority,area,english_name,used_name,insurancer_count,staff_count,operation_period,operation_scope,create_time,1))




            '''将branch_no,company_id,vestin_company,name插入company_branch表中'''
            branches = self.result.get('Branches')
            cursor.execute('select id from company where company_no=%s' % unique)
            company_id = cursor.fetchone()[0]
            for i in branches:
                keyno = i.get('KeyNo')
                keyno = json.dumps(keyno, encoding="utf-8", ensure_ascii=False)
                name = i.get('Name')
                name = json.dumps(name, encoding="utf-8", ensure_ascii=False)

                #self.company_id = company_id

                cursor.execute('insert into company_branch(branch_no,company_id,vestin_company,name) values(%s,%s,%s,%s)' % (keyno, company_id, 1, name))

                #time.sleep(2)
                #db.commit()



            '''将investment_no,company_id,name插入company_investment'''
            #unique = '287d9caa36e789820710a762fac79ad5'
            unique = json.loads(unique)
            global token_num
            token_num+=1
            js = requests.get('https://xcx.qichacha.com/wxa/v1/base/getInvestments?unique=%s&token=%s' % (unique, token),headers=headers)
            js = js.text
            js = json.loads(js)
            investments = js.get('result').get('Result')


            for i in investments:
                keyno = i.get('KeyNo')
                keyno = json.dumps(keyno, encoding="utf-8", ensure_ascii=False)
                name = i.get('Name')
                name = json.dumps(name, encoding="utf-8", ensure_ascii=False)
                #company_id = self.company_id

                cursor.execute('insert into company_investment(investment_no,company_id,name) values(%s,%s,%s)' % (keyno, company_id, name))
                #time.sleep(2)
                #db.commit()


            #因为对外投资公司的网页有分页，20家为一页，因此判断公司数量（Total_investment）是否超过20，来翻页获取数据
            Total_investment = js.get('result').get('Paging').get('TotalRecords')
            index = 1
            num = (Total_investment-1)/20

            #while Total_investment>20:
            for i in range(num):
                index+=1
                token_num += 1
                js = requests.get('https://xcx.qichacha.com/wxa/v1/base/getInvestments?unique=%s&token=%s&pageIndex=%s' % (unique, token,index),headers=headers)
                js = js.text
                js = json.loads(js)
                investments = js.get('result').get('Result')
                Total_investment = js.get('result').get('Paging').get('TotalRecords')
                for i in investments:
                    keyno = i.get('KeyNo')
                    keyno = json.dumps(keyno, encoding="utf-8", ensure_ascii=False)
                    name = i.get('Name')
                    name = json.dumps(name, encoding="utf-8", ensure_ascii=False)
                    #company_id = self.company_id

                    cursor.execute('insert into company_investment(investment_no,company_id,name) values(%s,%s,%s)' % (keyno, company_id, name))
                    #db.commit()
                    #time.sleep(3)
                time.sleep(2)
                #db.commit()


            #一个商业公司插入完成后，将source_company中的status更新为1，如果中间中断，直接从status=0的开始重新插入。到这里，一条商业公司的信息就插入完成了
            unique = json.dumps(unique, encoding="utf-8", ensure_ascii=False)
            cursor.execute('update source_company set status=1 where key_no=%s' %unique)
            #在三个表中都插入数据后，也就是一个商业公司插入完成后，提交事务
            db.commit()
            time.sleep(3)







    def main(self):
        #self.insert_company()
        #token失效判断，避免程序中断
        while True:
            try:
                self.insert_company()
            except AttributeError:
                print 'token faild or user forbidden'
                token = json.dumps(token, encoding="utf-8", ensure_ascii=False)
                cursor.execute('update token_list set token_status=0 where wx_token=%s' % token)
                db.commit()
                print "please add token"
                time.sleep(60)





if __name__ == "__main__":
    s = spider()
    s.main()





