# -*- coding: utf-8 -*-

import requests
import codecs
from lxml import etree
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    , 'charset': 'utf-8'
    , 'Accept-Encoding': 'gzip, deflate, br'
    , 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    , 'Connection': 'closed'
    ,'Accept-Language': 'zh-CN,zh;q=0.9'
}
ao='7250c71c15526347291963438e84f2aa7dc6688ec385e87cc927ca97f2'
cookie = {'QCCSESSID':'43mhn1dj7lck7ejnac4knue3q1'
          ,'UM_distinctid':'1697b7743944f5-04c3e3c165e59-69101b7d-1fa400-1697b7743955f7'
}
'acw_tc':'b4a39f4115525546103641153e300a6fe734c0a77351e07a93b942c6bb'
cookies = {
                    'Hm_lpvt_3456bee468c83cc63fb5147f119f1075': str(int(time.time()))
                    ,'Hm_lvt_3456bee468c83cc63fb5147f119f1075': str(int(time.time())-15)
                    ,'QCCSESSID':'kh50oeettqgbbphg0k57p37t40'
                    ,'UM_distinctid':'169951344c798-076e283be7625a-69101b7d-1fa400-169951344c843b'
                }

#a= requests.get('https://share.qichacha.com/pro/app_11.7.0/features/my-product.html?deviceType=android',headers=header,cookies=cookie)
#print a.text

proxy = {'https':'socks5://119.23.238.228:1080',
         'https':'socks5://118.31.229.46:8081',
         'https':'socks5://120.79.191.248:1080'}
a = requests.get('https://www.qichacha.com/firm_429c8a1a9fad2319d8a7b6a68101982e',headers=header)
#html = a.text
#html_name ='oo'
#File = codecs.open('C:\\Users\\win7\\Desktop\\download\\' + str(html_name),'wb','utf-8')
#File.write(htmlstr)
#File.flush()


html = etree.HTML(a.content)
testfield = html.xpath('//*[@id="Cominfo"]/table[2]/tr[3]/td[2]//text()')[0].strip().encode('utf-8')









