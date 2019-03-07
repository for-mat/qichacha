# -*- coding: utf-8 -*-

"配置代理"

import requests
import json
import random




#proxy = {'https':'https://172.106.164.151:8082'}
# 抓取免费代理
def fetch():
    req = requests.get('https://www.proxy-list.download/api/v0/get?l=en&t=socks5')
    response = req.text
    js = json.loads(response)
    socks_dicts = js[0].get('LISTA')
    num = len(socks_dicts)
    socks = []
    for i in range(num):
        if 'CN' or 'HK' in socks_dicts[i].values():
            ip = socks_dicts[i].get('IP')
            port = socks_dicts[i].get('PORT')
            sock = 'socks5://' + ip + ':' + port
            proxy1 = {'https':sock}
            #检查sock可用性，将可用sock加入socks列表
            try:
                requests.get('https://icanhazip.com/', proxies=proxy1, timeout=1)
                socks.append(sock)
                print ' 可用,已加入列表'
            except:
                print 'no'
                continue
    return socks

proxy_list = fetch()
print proxy_list
#proxy = {'https': str(random.choice(proxy_list))}

def change_proxy():
    proxy = {'https': str(random.choice(proxy_list))}
    return proxy

















