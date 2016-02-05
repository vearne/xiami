# -*- coding: utf-8 -*-
from peewee import *

db = MySQLDatabase(host='127.0.0.1', user='xiami', passwd='123456', database='xiami', charset='utf8mb4')

# ------------ external ---------------
class Song(Model):
    id = BigIntegerField()
    album_name = CharField()
    album_id = BigIntegerField()
    artist_name = CharField()
    artist_id = IntegerField()
    play_count = BigIntegerField()
    share_count = IntegerField()
    comment_count = IntegerField()
    name = CharField()
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        database = db
        db_table = "song"

if __name__ == '__main__':
    db.connect()

    # 建立表
    Song.create_table()
