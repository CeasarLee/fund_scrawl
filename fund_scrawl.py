from urllib import request
from bs4 import BeautifulSoup
import re
import requests
import pandas
import time
from utils import date_generate, get_proxy, load_data, load_data_ip, compare_time


def scrawl_seq(fund_id, start_date, end_date, save_path='./'):
    cur_date = start_date
    fund_data = pandas.DataFrame()
    fund_date = get_start_date(fund_id)
    if fund_date == '无记录':
        return
    else:
        if compare_time(fund_date, start_date):
            start_date = fund_date
    while 1:

        # 超过搜索日期时退出
        if compare_time(cur_date, end_date):
            break
        else:
            try:
                attrs, values = get_fund_price(fund_id, cur_date)
            except:
                print("IP 访问failure, 休眠3秒")
                time.sleep(3)
                continue
            cur_date = date_generate(cur_date)
            time.sleep(0.2)
            if values == []:
                continue
            if fund_data.empty:
                fund_data = pandas.DataFrame(dict(zip(attrs[:4], values)), pandas.Index(range(1)))
                h, w = fund_data.shape
                fund_data.to_csv(save_path+'/'+fund_id+'.csv', index=False)
                print(print("success save {} data in file in the path{}".format(cur_date, save_path+'/'+fund_id+'.csv')))
            else:
                assert h > 0
                assert w == 4
                fund_data.loc[0] = values
                fund_data.to_csv(save_path+'/'+fund_id+'.csv', header=False, mode='a', index=False)
                print(print("success save {} data in file in the path{}".format(cur_date, save_path+'/'+fund_id+'.csv')))

def scrawl_data(fund_code_queue, start_date='2020-01-01', end_date='2020-06-30', save_path='./', index=False):
    while not fund_code_queue.empty():
        print("start scrawl data\n")
        fund_id = fund_code_queue.get()
        scrawl_seq(fund_id, start_date, end_date, save_path)
#         print("success save file in {}".format(save_path+'/'+fund_id+'.csv'))

def get_fund_id():
    #获取所有的基金序号
    ret = []
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    rsp = request.urlopen(url)
    content = rsp.read()

    soup = BeautifulSoup(content, 'lxml')

    # bs 自动解码
    content = soup.prettify()
    stock_info = soup.contents[0].string
    pattern = re.compile(r'"(\d+)"')
    result = pattern.findall(content)
    for i in range(len(result)):
        result[i] = result[i].lstrip(").rstrip(")
    return result

def get_fund_price(fund_id='000001', search_date='2019-02-13'):
    """
    start_data example: 
    """
    ip = get_proxy()
    url="http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={}&page=1&sdate={}&edate={}&per=1".format(fund_id, search_date, search_date)
    rsp = load_data(url)
    text = rsp.content.decode('utf-8')
#     print(text)
    #获取特征名
    attrs = re.findall("([\u4E00-\u9FA5]+)</th><th>", text)
    #获取日期
    values = re.findall("<tbody><tr><td>(.*?)</td>", text)
    #获取单位净值和累计净值
    values += re.findall("<td class='tor bold'>(.*?)</td>", text)
    #获取日增长率
    values += re.findall("<td class='tor bold red'>(.*?)</td>", text)
    values += re.findall("<td class='tor bold grn'>(.*?)</td>", text)
    values += re.findall("<td class='tor bold bck'>(.*?)</td>", text)
    return attrs, values

def get_start_date(fund_id):
    #####本函数查询基金起始日期，返回日期字符串

    url = 'http://fund.eastmoney.com/'+fund_id+'.html?spm=search'
    ######获得网页内容；设置网页编码；在天天基金网获得起始日期
    ######用到 requests,re模块
    response = load_data(url)
    text = response.content.decode('utf-8')

    start_date=re.findall('<td><span class="letterSpace01">成 立 日</span>：(.*?)</td>',text)
    ######以防止输入的编码查不到信息，对无记录基金代码进行标注，后续方便剔除
    if start_date == []:
        start_date=['无记录']
    return(start_date[0])

def get_cur_manager(fund_id):
    search_url='http://fund.eastmoney.com/'+fund_id+'.html?spm=search'
    ######获得网页内容；设置网页编码；在天天基金网获得起始日期
    ######用到 requests,re模块
    response=load_data(search_url)
    text = response.content.decode('utf-8')
    manager_name = re.findall('<a href="http://fundf10.eastmoney.com/jjjl_\d+.html">(.*?)</a>', text) 
    if manager_name == []:
        manager_name=['无记录']
    return (manager_name[0])

def get_fund_size(fund_id):
    search_url='http://fund.eastmoney.com/'+fund_id+'.html?spm=search'
    ######获得网页内容；设置网页编码；在天天基金网获得起始日期
    ######用到 requests,re模块
    response=requests.get(search_url)
    text = response.content.decode('utf-8')
    target = re.findall('基金规模(.*?)亿元', text)
    if target == []:
        target=['无记录']
    return (target[0])