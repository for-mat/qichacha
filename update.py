# -*- coding: utf-8 -*-

"""
更新表信息
"""
import proxy_pool
import headers_pool
import config
import pymysql
import requests
import json
import time
import re

db = pymysql.connect(host='192.168.1.100', port=3306, user='qcc', passwd='VhO4fNROWARt', db='spider_qichacha',charset='utf8')
cursor = db.cursor()

#tokens = config.tokens
token_num = config.token_num
token = config.token


class get_all_fields(object):
    @staticmethod
    #获取网页中的字段，返回字段列表和result(用于获取分支机构名称和unique)
    def get_fields(unique ,token ,proxy):
        proxy = proxy
        print proxy
        headers = headers_pool.requests_headers()
        # print headers
        # 获取网页，取出json中的公司信息
        # 设置代理ip
        js = requests.get('https://xcx.qichacha.com/wxa/v1/base/getMoreEntInfo?unique=%s&token=%s' % (unique ,token), headers = headers,verify=False, proxies=proxy , timeout=2)
        # print js.cookies
        js = js.text
        print js
        js = json.loads(js)
        result = js.get('result')
        result = result
        # company = result.get('Company')

        # 获取字段
        name = result.get('Name')
        phone = result.get('ContactInfo').get('PhoneNumber')

        try:
            website = result.get('ContactInfo').get('WebSite')[0].get('Url')
        except TypeError:
            website = None

        email = result.get('ContactInfo').get('Email')
        province = result.get('Area').get('Province')
        city = result.get('Area').get('City')
        county = result.get('Area').get('County')
        address = result.get('Address')

        reg = re.compile('<[^>]*>')
        intro = result.get('ProfileDesc')
        intro = reg.sub('' ,intro).strip()

        registered_capital = result.get('RegistCapi')
        actual_capital = result.get('RecCap')
        operating_state = result.get('Status')
        establishment_date = result.get('StartDate')
        uscc = result.get('CreditCode')
        taxpayer_number = result.get('TaxNo')
        registration_number = result.get('No')
        organization_code = result.get('OrgNo')
        type1 = result.get('EconKind')
        industry = result.get('Industry').get('Industry')

        approval_date = result.get('CheckDate')
        if approval_date < 0:
            approval_date = 0
        approval_date = time.localtime(approval_date)
        approval_date = time.strftime("%Y-%m-%d" ,approval_date)

        registration_authority = result.get('BelongOrg')
        area = result.get('Area').get('Province')
        english_name =result.get('EnglishName')

        used_name_list = result.get('OriginalName')
        if type(used_name_list) == list:
            used_name1 = ""
            for i in used_name_list:
                used_name1 = used_name1 + (i.get('Name')) + " "
            used_name = used_name1
        else:
            used_name = None

        try:
            insurancer_count = result.get('CommonList')[3].get('Value')
        except:
            insurancer_count = None

        staff_count = result.get('profile').get('Info')

        StartDate = result.get('StartDate')
        StartDate = str(StartDate)
        EndDate = result.get('EndDate')
        EndDate = str(EndDate)
        if EndDate == '0':
            EndDate = 'Indefinite'
        operation_period = StartDate + ' unitl ' + EndDate

        operation_scope = result.get('Scope')

        name = json.dumps(name, encoding="utf-8", ensure_ascii=False)
        phone = json.dumps(phone, encoding="utf-8", ensure_ascii=False)
        website = json.dumps(website, encoding="utf-8", ensure_ascii=False)
        email = json.dumps(email, encoding="utf-8", ensure_ascii=False)
        province = json.dumps(province, encoding="utf-8", ensure_ascii=False)
        city = json.dumps(city, encoding="utf-8", ensure_ascii=False)
        county = json.dumps(county, encoding="utf-8", ensure_ascii=False)
        address = json.dumps(address, encoding="utf-8", ensure_ascii=False)
        intro = json.dumps(intro, encoding="utf-8", ensure_ascii=False)
        registered_capital = json.dumps(registered_capital, encoding="utf-8", ensure_ascii=False)
        actual_capital = json.dumps(actual_capital, encoding="utf-8", ensure_ascii=False)
        operating_state = json.dumps(operating_state, encoding="utf-8", ensure_ascii=False)
        establishment_date = json.dumps(establishment_date, encoding="utf-8", ensure_ascii=False)
        uscc = json.dumps(uscc, encoding="utf-8", ensure_ascii=False)
        taxpayer_number = json.dumps(taxpayer_number, encoding="utf-8", ensure_ascii=False)
        registration_number = json.dumps(registration_number, encoding="utf-8", ensure_ascii=False)
        organization_code = json.dumps(organization_code, encoding="utf-8", ensure_ascii=False)
        type1 = json.dumps(type1, encoding="utf-8", ensure_ascii=False)
        industry = json.dumps(industry, encoding="utf-8", ensure_ascii=False)
        approval_date = json.dumps(approval_date, encoding="utf-8", ensure_ascii=False)
        registration_authority = json.dumps(registration_authority, encoding="utf-8", ensure_ascii=False)
        area = json.dumps(area, encoding="utf-8", ensure_ascii=False)
        english_name = json.dumps(english_name, encoding="utf-8", ensure_ascii=False)
        used_name = json.dumps(used_name, encoding="utf-8", ensure_ascii=False)
        insurancer_count = json.dumps(insurancer_count, encoding="utf-8", ensure_ascii=False)
        staff_count = json.dumps(staff_count, encoding="utf-8", ensure_ascii=False)
        operation_period = json.dumps(operation_period, encoding="utf-8", ensure_ascii=False)
        operation_scope = json.dumps(operation_scope, encoding="utf-8", ensure_ascii=False)

        fields = (name, phone, website, email, province, city, county, address, intro, registered_capital, actual_capital,
                  operating_state, establishment_date, uscc, taxpayer_number, registration_number, organization_code, type1,
                  industry, approval_date, registration_authority, area, english_name, used_name, insurancer_count,
                  staff_count, operation_period, operation_scope)
        return fields, result

class insert_company(object):
    # 获取所有商业公司的unique
    def get_uniques(self):
        cursor.execute('select key_no from source_company where status =1')
        results = cursor.fetchall()
        uniques = []
        for i in results:
            keyno = i[0]
            uniques.append(keyno)
        return uniques

    #根据商业公司往三个表中插入数据
    def insert_data(self):
        uniques = self.get_uniques()
        if len(uniques) == 0:
            print 'table company is ok'
        else:
            print '正在向company插入数据...'
        for unique in uniques:
            n=1
            create_time = time.time()
            # 判断token使用次数，使用token超过1000次，就换一个token使用
            config.change_token()
            # 获取包含所有字段的元组
            p_num = 1
            #self.proxy = proxy_pool.proxy
            while True:
                try:
                    self.proxy = proxy_pool.change_proxy()
                    proxy = self.proxy
                    (fields, result) = get_all_fields.get_fields(unique, token, proxy)
                except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,requests.exceptions.SSLError,requests.exceptions.ConnectionError):
                    self.proxy = proxy_pool.change_proxy()
                    global proxy
                    proxy = self.proxy
                    print 'changing proxy...%s...%s'%(p_num,self.proxy)
                    p_num+=1
                    continue
                break
            # 转为列表，并将unique,create_time,status加入列表
            company_fields = list(fields)
            unique = json.dumps(unique, encoding="utf-8", ensure_ascii=False)
            company_fields.insert(0, unique)
            company_fields.append(create_time)
            company_fields.append(1)
            # 转为元组，插入数据
            company_fields = tuple(company_fields)


            #tuple = (unique,name, phone, website, email, province, city, county, address, intro, registered_capital, actual_capital,operating_state, establishment_date, uscc, taxpayer_number, registration_number, organization_code, type,industry, approval_date, registration_authority, area, english_name, used_name, insurancer_count,staff_count, operation_period, operation_scope,create_time,1)

            cursor.execute('replace into company(company_no,name,phone,website,email,province,city,county,address,intro,registered_capital,actual_capital,operating_state,establishment_date,uscc,taxpayer_number,registration_number,organization_code,type,industry,approval_date,registration_authority,area,english_name,used_name,insurancer_count,staff_count,operation_period,operation_scope,create_time,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' % company_fields)
            #cursor.execute('insert into company(company_no,name,phone,website,email,province,city,county,address,intro,registered_capital,actual_capital,operating_state,establishment_date,uscc,taxpayer_number,registration_number,organization_code,type,industry,approval_date,registration_authority,area,english_name,used_name,insurancer_count,staff_count,operation_period,operation_scope,create_time,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %(unique,name,phone,website,email,province,city,county,address,intro,registered_capital,actual_capital,operating_state,establishment_date,uscc,taxpayer_number,registration_number,organization_code,type,industry,approval_date,registration_authority,area,english_name,used_name,insurancer_count,staff_count,operation_period,operation_scope,create_time,1))



            '''将branch_no,company_id,vestin_company,name插入company_branch表中'''
            branches = result.get('Branches')
            cursor.execute('select id from company where company_no=%s' % unique)
            company_id = cursor.fetchone()[0]
            for i in branches:
                keyno = i.get('KeyNo')
                keyno = json.dumps(keyno, encoding="utf-8", ensure_ascii=False)
                name = i.get('Name')
                name = json.dumps(name, encoding="utf-8", ensure_ascii=False)

                #self.company_id = company_id

                cursor.execute('update company_branch set branch_no=%s,company_id=%s,vestin_company=%s,name=%s where  name=%s' % (keyno, company_id, 1, name,keyno,name))
                print name

                #time.sleep(2)
                #db.commit()


            '''将investment_no,company_id,name插入company_investment'''
            #unique = '287d9caa36e789820710a762fac79ad5'
            unique = json.loads(unique)
            global token_num
            token_num+=1
            while True:
                try:
                    js = requests.get('https://xcx.qichacha.com/wxa/v1/base/getInvestments?unique=%s&token=%s' % (unique, token), headers=config.headers, proxies=self.proxy,verify=False,timeout=2)
                except:
                    self.proxy = proxy_pool.change_proxy()
                    continue
                break
            js = js.text
            js = json.loads(js)
            investments = js.get('result').get('Result')


            for i in investments:
                keyno = i.get('KeyNo')
                keyno = json.dumps(keyno, encoding="utf-8", ensure_ascii=False)
                name = i.get('Name')
                name = json.dumps(name, encoding="utf-8", ensure_ascii=False)
                #company_id = self.company_id

                cursor.execute('update company_investment set investment_no=%s,company_id=%s,name=%s where investment_no=%s or name=%s' %(keyno, company_id, name,keyno,name))
                print name
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
                while True:
                    try:
                        js = requests.get('https://xcx.qichacha.com/wxa/v1/base/getInvestments?unique=%s&token=%s&pageIndex=%s' % (unique, token,index), headers=config.headers, proxies=self.proxy,verify=False,timeout=2)
                    except:
                        self.proxy = proxy_pool.change_proxy()
                        continue
                    break
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

                    cursor.execute('update company_investment set investment_no=%s,company_id=%s,name=%s where investment_no=%s or name=%s' % (keyno, company_id, name, keyno, name))
                    print name
                    #db.commit()
                    #time.sleep(3)
                time.sleep(2)
                #db.commit()


            #一个商业公司插入完成后，将source_company中的status更新为1，如果中间中断，直接从status=0的开始重新插入。到这里，一条商业公司的信息就插入完成了
            unique = json.dumps(unique, encoding="utf-8", ensure_ascii=False)
            cursor.execute('update source_company set update_time=%s where key_no=%s' %(int(time.time()),unique))
            #在三个表中都插入数据后，也就是一个商业公司插入完成后，提交事务
            db.commit()
            time.sleep(2)
            print '已插入%s条,剩余%s条' % (n,len(uniques)-n)
            n += 1


insert_company().insert_data()
