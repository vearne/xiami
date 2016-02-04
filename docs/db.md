song（歌曲）

|字段|类型|说明|
| --------|-------|-----|
| id | id |主键  |
| album_name | varchar(50) | 专辑 |
| album_id | int | 专辑ID |
| artist_name | varchar(30) | 歌手名称 |
| artist_id | id | 歌手ID |
| play_count | int | 试听次数 |
| share_count | int | 分享次数 |
| comment_count | int | 评论次数 |


artist（歌手)

|字段|类型|说明|
| --------|-------|-----|
| id | id |主键  |
| name| varchar(30) | 名称 |
| play_count | int | 试听次数 |
| fans_count | int | 粉丝数 |
| comment_count | int | 分享次数 |

album（专辑)

|字段|类型|说明|
| --------|-------|-----|
| id | id |主键  |
| name| varchar(30) | 名称 |
| play_count | int | 试听次数 |
| collect_count | int | 收藏数 |
| comment_count | int | 分享次数 |
| score | float| 评分 |
| publish_time| date| 发布时间 |
| category| varchar(30)| 类别 |
| artist_id| int| 歌手ID |
| artist_name| varchar(30)| 歌手名称 |
|genre|varchar(30)|风格|
|company|varchar(30)|唱片公司|
