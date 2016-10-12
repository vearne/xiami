# coding:utf-8
from lxml import etree
from StringIO import StringIO
import requests
from db import Artist
from datetime import datetime
from log import init_logger
import threading
from db import Proxy
import random

logger = init_logger()


class AtomicInteger():
    def __init__(self, value):
        self.mutex = threading.Lock()
        self.value = value

    def incre(self):
        self.mutex.acquire()
        self.value += 1
        self.mutex.release()
        return self.value


class FetchWorker(threading.Thread):
    '''
        实际从sina API 抓取数据
    '''

    def __init__(self, counter):
        super(FetchWorker, self).__init__()
        self.counter = counter
        self.proxy_list = self.fetch_proxy()

    def run(self):
        i = 0
        while(True):
            i += 1
            id = self.counter.incre()
            retry_flag = True
            while retry_flag:
                try:
                    self.fetch(id)
                    retry_flag = False
                except requests.exceptions.ConnectionError:
                    retry_flag = True
                except requests.exceptions.ReadTimeout:
                    retry_flag = True
                except:
                    retry_flag = False
                    logger.error('http://www.xiami.com/song/%s', id, exc_info=1)

            if i % 50 == 0:
                self.fetch_proxy()

    def fetch_proxy(self):
        proxy_list = Proxy.select().where(Proxy.valid == True)
        return [proxy for proxy in proxy_list]

    def fetch(self, id):
        proxy = random.choice(self.proxy_list)
        proxies = {
            "http": 'http://%s:%s' % (proxy.ip, proxy.port)
        }
        headers={
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
        }

        url = 'http://www.xiami.com/artist/%s' % id
        res = requests.get(url, headers=headers, proxies=proxies)
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(res.text), parser)

        # play_count & share_count & comment_count
        url = 'http://www.xiami.com/count/getplaycount?id=%s&type=artist' % id
        res = requests.get(url, headers=headers)
        play_count = res.json()['plays']

        fans_count = tree.xpath('//div[@class="music_counts"]//li[2]/text()')
        fans_count = int(fans_count[0])

        comment_count = tree.xpath('//div[@class="music_counts"]//li[3]/a/text()')
        comment_count = int(comment_count[0])

        name = tree.xpath('//*[@id="title"]/h1/text()')
        name = name[0]

        dd = {
            "play_count": play_count,
            "fans_count": fans_count,
            "comment_count": comment_count,
            "name": name,
            "create_time": datetime.now(),
            "update_time": datetime.now()
        }
        Artist.get_or_create(id=id, defaults=dd)
        logger.info('http://www.xiami.com/artist/%s', id)

def main(value):
    worker_pool = {}
    counter = AtomicInteger(value)
    for id in xrange(1, 2):
        p = FetchWorker(counter)
        p.start()
        worker_pool[p.ident] = p

    for p in worker_pool.values():
        p.join()

if __name__ == '__main__':
    value = 1
    main(value)




