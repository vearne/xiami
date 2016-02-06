from db import Proxy
import requests
import time


def main():
    t = Proxy.select().where(Proxy.valid == True).count()
    print 'count', t
    if t < 20:
        try:
            get_proxy()
        except Exception:
            pass

    check_and_mark()


def get_proxy():
    url = 'http://qsdrk.daili666api.com/ip/'
    dd = {
        'foreign':'none',
        'num':20,
        'tid':'556914678655241',
        'filter':'on',
        'category':2,
        'delay':2,
        'exclude_ports':'8088,18186'
    }
    res = requests.get(url, params=dd)    
    item_list = res.text.split('\n')
    for item in item_list:
        ip, port = item.split(':')
        port = int(port)
        query = Proxy.select().where(Proxy.ip==ip)
        res = query.execute()
        temp_list = [p for p in res]
        if len(temp_list) == 0 and check(ip, port):
            p = Proxy()
            p.ip = ip
            p.port = port
            p.valid = True
            p.save()


def check_and_mark():
    query = Proxy.select().where(Proxy.valid == True)
    proxy_list = query.execute()
    for proxy in proxy_list:
        flag = check(proxy.ip, proxy.port)
        if flag == False:
            print proxy
            proxy.valid = False
            proxy.save()


def check(ip, port):
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
    }
    try:
        proxies = {
            "http": 'http://%s:%s' % (ip, port)
        }
        url = 'http://up.xiaorui.cc:9000/test.json'
        res = requests.get(url, proxies=proxies, timeout=3, headers=headers)
        print res.text
        dd = res.json()
        if dd['a'] == 1:
            return True
    except Exception, e:
        print type(e), e
        return False

    return False


if __name__ == '__main__':
    while(True):
        time.sleep(10)
        main()
