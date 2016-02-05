# coding:utf-8
from lxml import etree
from StringIO import StringIO
import requests
from db import Song
from datetime import datetime
from log import init_logger

logger = init_logger()

def fetch(id):
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
    }

    url = 'http://www.xiami.com/song/%s' % id
    res = requests.get(url, headers=headers)
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(res.text), parser)
    # album_name & album_id
    album_a = tree.xpath('//table[@id="albums_info"]//tr[1]/td[2]//a')
    album_name = album_a[0].text

    album_id = album_a[0].get('href')[7:]
    album_id = int(album_id)
    # artist_name & artist_id
    artist_a = tree.xpath('//table[@id="albums_info"]//tr[2]/td[2]//a')
    artist_name = artist_a[0].text
    artist_id = artist_a[0].get('href')[8:]
    artist_id = int(artist_id)

    # play_count & share_count & comment_count
    url = 'http://www.xiami.com/count/getplaycount?id=%s&type=song' % id
    res = requests.get(url, headers=headers)
    play_count = res.json()['plays']

    share_count = tree.xpath('//div[@class="music_counts"]//li[2]/text()')
    share_count = share_count[0]

    comment_count = tree.xpath('//div[@class="music_counts"]//li[3]/a/text()')
    comment_count = int(comment_count[0])

    name = tree.xpath('//*[@id="title"]/h1/text()')
    name = name[0]

    dd = {
        "album_name": album_name,
        "album_id": album_id,
        "artist_name": artist_name,
        "artist_id": artist_id,
        "play_count": play_count,
        "share_count": share_count,
        "comment_count": comment_count,
        "name": name,
        "create_time": datetime.now(),
        "update_time": datetime.now()
    }
    Song.get_or_create(id=id, defaults=dd)
    print id
#logger.info('http://www.xiami.com/song/%s', id)


def main():
    for id in range(1, 2000000000):
        fetch(id)


if __name__ == '__main__':
    main()




