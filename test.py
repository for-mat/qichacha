# -*- coding: utf-8 -*-

import requests


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    , 'charset': 'utf-8'
    , 'Accept-Encoding': 'gzip, deflate, br'
    , 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    , 'Host': 'share.qichacha.com'
    , 'Connection': 'closed'
    ,'Accept-Language': 'zh-CN,zh;q=0.9'
}
cookie = {'Cookie':'acw_tc=b4a39f4415518383176684042ee47ef851dd23ec2b618f085e559bdba8'}



#a= requests.get('https://share.qichacha.com/pro/app_11.7.0/features/my-product.html?deviceType=android',headers=header,cookies=cookie)
#print a.text

proxy = {'https':'socks5://119.23.238.228:1080',
         'https':'socks5://118.31.229.46:8081',
         'https':'socks5://120.79.191.248:1080'}
a = requests.get('https://icanhazip.com/',headers=header,proxies=proxy,verify=False)
print a.text












