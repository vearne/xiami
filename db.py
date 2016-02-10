# -*- coding: utf-8 -*-
from peewee import *

db = MySQLDatabase(host='127.0.0.1', user='xiami', passwd='xiami1234', database='xiami', charset='utf8mb4')

# ------------ external ---------------
class Song(Model):
    id = BigIntegerField(primary_key=True)
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

class Artist(Model):
    id = PrimaryKeyField()
    name = CharField(max_length=30)
    play_count = BigIntegerField()
    fans_count = IntegerField()
    comment_count = IntegerField()
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        database = db
        db_table = "artist"

class Proxy(Model):
    id = IntegerField()
    ip = CharField(max_length=30, unique=True)
    port = IntegerField()
    valid = BooleanField()

    class Meta:
        database = db
        db_table = "proxy"

if __name__ == '__main__':
    db.connect()

    # 建立表
    # Song.create_table()
    #Proxy.create_table()
    Artist.create_table()

