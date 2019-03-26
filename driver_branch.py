# -*- coding: UTF-8 -*-


import headers_pool
import pymysql
import requests
import json
import time
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 设置firefox选项，使用headless模式，自定义下载位置
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.add_argument('-headless')
fireFoxOptions.add_argument("--window-size=1920,1080")
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.dir', 'C:\\Users\\win7\\Desktop')  # 现在文件存放的目录
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk',
                       'application/pdf,application/octet-stream, application/x-excel, text/html, application/zip')
profile.set_preference("browser.helperApps.alwaysAsk.force", False)
profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
profile.set_preference("browser.download.manager.focusWhenStarting", False)
profile.set_preference("browser.download.useDownloadDir", True)
profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
profile.set_preference("browser.download.manager.closeWhenDone", True)
profile.set_preference("browser.download.manager.showAlertOnComplete", False)
profile.set_preference("browser.download.manager.useWindow", False)  #
profile.set_preference("pdfjs.disabled", True)
profile.set_preference('network.proxy.type', 1)


profile.set_preference('network.proxy.socks','119.23.238.228')
profile.set_preference('network.proxy.socks_port', '1080')



brower = webdriver.Firefox(firefox_options=fireFoxOptions, executable_path='D:\\Python\\geckodriver',
                           firefox_profile=profile)

brower.get('https://www.qichacha.com/user_login')
brower.find_element_by_xpath('// *[ @ id = "qrcodeLoginPanel"] / div[2] / div / div[3] / a[2]').click()
brower.switch_to.frame(0)
brower.find_element_by_id('switcher_plogin').click()
brower.find_element_by_name('u').send_keys('546454228')
brower.find_element_by_name('p').send_keys('shangbin9719')
brower.find_element_by_id('login_button').click()
time.sleep(10)
brower.switch_to_default_content()
brower.find_element_by_xpath('//*[@id="bindwxModal"]/div[1]/div[1]/div[1]/button/span').click()


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

                }
                html = brower.get('https://www.qichacha.com/firm_%s'%unique)
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,requests.exceptions.SSLError,requests.exceptions.ConnectionError):
                print 'changing proxy...%s...%s'%(p_num,self.proxy)
                p_num+=1
                continue
            break
        response = brower.page_source
        #print response

        #有时会获取不到页面,触发异常处理
        if '<script>window.location.href' in response:
            raise UnboundLocalError

        s1 = etree.HTML(response)

        #获取字段
        time.sleep(1)
        #注册资本
        registered_capital = brower.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/div[3]/div[1]/span[1]/span[2]/span').text
        if registered_capital == '-':
            registered_capital = None
        registered_capital = json.dumps(registered_capital, encoding="utf-8", ensure_ascii=False)


        #test = s1.xpath('//*[@id="company-top"]/div[2]/div[2]/div[3]/div[1]/span[1]/span[2]/span//text()')
        #print test
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



