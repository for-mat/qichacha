# -*- coding: utf-8 -*-

'''读取company_investment表，获取对外投资机构的信息，并插入company_investment'''
import pymysql
import config
from getdata import spider
import time
import json

db = pymysql.connect(host='192.168.1.100', port=3306, user='root', passwd='123123', db='spider_qichacha',
                     charset='utf8')
cursor = db.cursor()

headers = config.headers
tokens = config.tokens
token_num = config.token_num
token = config.token

spider = spider()


# unique = '287d9caa36e789820710a762fac79ad5'
# print spider.get_fields(unique)


def get_uniques():
    cursor.execute('select investment_no from company_investment where status=0')
    results = cursor.fetchall()
    uniques = []
    for i in results:
        keyno = i[0]
        uniques.append(keyno)
    return uniques



def insert_company():
    uniques = get_uniques()
    for unique in uniques:
        create_time = time.time()
        # 判断token使用次数，使用token超过1000次，就换一个token使用
        config.change_token()
        # 获取包含所有字段的元组
        (fields,result) = spider.get_fields(unique, token)
        # 转为列表，并将unique,create_time,status加入列表
        company_fields = list(fields)
        unique = json.dumps(unique, encoding="utf-8", ensure_ascii=False)
        company_fields.append(create_time)
        company_fields.append(1)
        company_fields.append(unique)
        # 转为元组，插入数据
        company_fields = tuple(company_fields)

        # tuple = (unique,name, phone, website, email, province, city, county, address, intro, registered_capital, actual_capital,operating_state, establishment_date, uscc, taxpayer_number, registration_number, organization_code, type,industry, approval_date, registration_authority, area, english_name, used_name, insurancer_count,staff_count, operation_period, operation_scope,create_time,1)
        cursor.execute('update company_investment set name=%s, phone=%s, website=%s, email=%s, province=%s, city=%s, county=%s, address=%s, intro=%s, registered_capital=%s, actual_capital=%s, operating_state=%s, establishment_date=%s, uscc=%s, taxpayer_number=%s, registration_number=%s, organization_code=%s, type=%s, industry=%s, approval_date=%s, registration_authority=%s, area=%s, english_name=%s, used_name=%s, insurancer_count=%s, staff_count=%s, operation_period=%s, operation_scope=%s, create_time=%s, status=%s where investment_no=%s' % company_fields)

        '''将branch_no,company_id,vestin_company,name插入company_branch表中'''
        cursor.execute('select id from company_investment where investment_no=%s' % unique)
        investment_id = cursor.fetchone()[0]
        cursor.execute('select company_id from company_investment where investment_no=%s' % unique)
        company_id = cursor.fetchone()[0]
        branches = result.get('Branches')
        for i in branches:
            keyno = i.get('KeyNo')
            keyno = json.dumps(keyno, encoding="utf-8", ensure_ascii=False)
            name = i.get('Name')
            name = json.dumps(name, encoding="utf-8", ensure_ascii=False)

            cursor.execute('insert into company_branch(branch_no,company_id,investment_id,vestin_company,name) values(%s,%s,%s,%s,%s)' % (keyno,company_id, investment_id, 0, name))


        db.commit()
        time.sleep(2)
    #db.commit()


insert_company()



