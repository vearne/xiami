# coding:utf-8
from lxml import etree
from StringIO import StringIO
import requests
import random

def get_proxy():
    proxy_list = []
    for i in range(1, 3):
        url = 'http://www.kuaidaili.com/proxylist/%s' % (i) 
        r = requests.get(url)
        ss = r.text
        parser = etree.HTMLParser()
        tree   = etree.parse(StringIO(ss), parser)
        item_list = tree.xpath('//*[@id="list"]/table/tbody/tr')
        print 'item_list', len(item_list)
        for item in item_list:
            #print etree.tostring(item)
            td_list = item.findall('td')
            #print type(td_list[2].text)
            if td_list[2].text == u'高匿名':
                dd = {}
                dd['ip'] = td_list[0].text
                dd['port'] = int(td_list[1].text)
                proxy_list.append(dd)
#                print td_list[2].text
            #print len(td_list)
    return proxy_list

def main():
    proxy_list = get_proxy()
    print 'len proxy_list', len(proxy_list)
    proxy = random.choice(proxy_list)
    purl = 'http://%s:%s' % (proxy['ip'], proxy['port'])
    print purl
    proxies = {
        "http": purl,
    }
    id = 1
    url = 'http://www.xiami.com/song/%s' % (id) 
    print 'url', url
    res = requests.get(url, proxies=proxies)
    print res.text


if __name__ == '__main__':
    main()



