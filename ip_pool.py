
# 获取有效ip
import urllib
from lxml import etree

def get_html(url):
    request = urllib.request.Request(url)
    request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")
    html = urllib.request.urlopen(request)
    return html.read()


def testIp(ip_list):
    #测试ip是否有效
    useFullIp = []
    for ip in ip_list:
        response = urllib.request.urlopen('https://www.baidu.com/',proxies={'https//':ip})
        if response.getcode()==200:
            useFullIp.append(ip)
    return useFullIp

def fetch_kuaidaili():
    startUrl = 'https://www.kuaidaili.com/free/'
    proxys = []
    for i in range(1,11):
        url = startUrl+str(i)+'/'
        html = etree.HTML(get_html(url))
        trs = html.xpath('//*[@id="index_free_list"]/table/tbody/tr')
        for line in range(len(trs)):
            td_type = trs[line].xpath('td[4]/text()')[0]
            if 'HTTPS' in td_type:  #判断是否为HTTPS代理，不是则不抓取
                td_speed = trs[line].xpath('td[7]/text()')[0][:-1:]
                if float(td_speed)<1.0:
                    td_ip = trs[line].xpath('td[1]/text()')[0]
                    td_port = trs[line].xpath('td[2]/text()')[0]
                    ip = td_ip+':'+str(td_port)
                    proxys.append(ip)
    useFullIp = testIp(map(lambda x:x.strip(),proxys))
    print('from kuaidaili...%s'%len(useFullIp))
    return useFullIp

def fetch_kxdaili():
    startUrl = 'http://www.kxdaili.com/ipList/' #地址随时可能变动需要添加处理机制
    proxys = []
    for i in range(1,11):
        url = startUrl+str(i)+'.html'
        html = etree.HTML(get_html(url))
        trs = html.xpath('//*[@id="nav_btn01"]/div[5]/table/tbody/tr')
        for line in range(len(trs)):
            td_type = trs[line].xpath('td[4]/text()')[0]
            if 'HTTPS' in td_type:  #判断是否为HTTPS代理，不是则不抓取
                td_speed = trs[line].xpath('td[5]/text()')[0].split('.')[0]
                if int(td_speed)<1:
                    td_ip = trs[line].xpath('td[1]/text()')[0]
                    td_port = trs[line].xpath('td[2]/text()')[0]
                    ip = td_ip+':'+str(td_port)
                    proxys.append(ip)
    useFullIp = testIp(map(lambda x:x.strip(),proxys))

    print('from kxdaili...%s'%len(useFullIp))
    # print useFullIp
    return useFullIp

def fetch_xici():
    startUrl = 'http://www.xicidaili.com/wn/1'
    proxys = []
    html = etree.HTML(get_html(startUrl))
    tables = html.xpath('//table[@id="ip_list"]')
    trs = tables[0].xpath('tr')
    for line in trs[1:]:
        td_type = line.xpath('td[6]/text()')[0].strip()
        if 'HTTPS' == td_type:
            td_speed = line.xpath('td[7]/div/@title')[0].strip()[:-1]
            if float(td_speed) < 5:
                td_ip = line.xpath('td[2]/text()')[0].strip()
                td_port = line.xpath('td[3]/text()')[0].strip()
                ip = td_ip +':'+td_port
                proxys.append(ip)
    useFullIp = testIp(map(lambda x:x.strip(),proxys))
    print ("from xici ... %s"%len(useFullIp))
    return useFullIp

