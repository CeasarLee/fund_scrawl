#!/usr/bin/env python
# coding: utf-8

import requests
import json
import random
import time
# user_agent列表
user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
]

# referer列表
referer_list = [
    'http://fund.eastmoney.com/110022.html',
    'http://fund.eastmoney.com/110023.html',
    'http://fund.eastmoney.com/110024.html',
    'http://fund.eastmoney.com/110025.html'
]
# 返回一个可用代理，格式为ip:端口
# 该接口直接调用github代理池项目给的例子，故不保证该接口实时可用
# 建议自己搭建一个本地代理池，这样获取代理的速度更快
# 代理池搭建github地址https://github.com/1again/ProxyPool
# 搭建完毕后，把下方的proxy.1again.cc改成你的your_server_ip，本地搭建的话可以写成127.0.0.1或者localhost
def get_proxy():
    #获取一个自动ip池的ip，经验证大部分ip不能用
    data_json = requests.get("http://proxy.1again.cc:35050/api/v1/proxy/").text
    data = json.loads(data_json)
    return data['data']['proxy']

def date_generate(cur_date):
    #生成下一天的日期
    year, month, day = map(int, cur_date.split('-'))
    d = {1:31, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    if (year % 400 == 0) or (year % 100 !=0 and year % 4 == 0):
        d[2] = 29
    else:
        d[2] = 28
    if d[int(month)] > int(day):
        return str(year) + '-' + str(month) + '-' + str(int(day) + 1)
    else:
        if month == 12: 
            year = str(int(year) + 1)
            return year + '-01-01'
        else:
            month = str(int(month) + 1)
            return str(year) + '-' + month +'-01'

def compare_time(time1,time2):
    s_time = time.mktime(time.strptime(time1,'%Y-%m-%d'))
    e_time = time.mktime(time.strptime(time2,'%Y-%m-%d'))
    return int(s_time) > int(e_time)

def load_data(url):
    #使用本地IP进行数据抓取
    header = {'User-Agent': random.choice(user_agent_list),
                      'Referer': random.choice(referer_list)
            }
    return requests.get(url, timeout=3, headers=header)

def load_data_ip(url, proxy):
    # 通过代理进行数据抓取的版本
    header = {'User-Agent': random.choice(user_agent_list),
                      'Referer': random.choice(referer_list)
            }
    return requests.get(url, proxies={"http": proxy}, timeout=3, headers=header)
