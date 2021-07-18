# -*- coding:utf-8 -*-
"""
Desc:
    把数据写入数据库
"""
import os
import pymysql
import common.opertime as ot
import common.operdirandfiler as odf
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MusicRec.settings")
# os.environ['DJANGO_SETTINGS_MODULE'] = 'MusicRec.setttings'
django.setup()
"""
 上边import 解决错误：
 django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS, but settings are not 
 django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
"""
from MusicRec.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWD, DB_NAME
from playlist.models import PlayListToSongs, PlayListToTag, PlayList
from song.models import SongLysic, Song, SongTag
from user.models import User, UserTag
from sing.models import Sing, SingTag


class ToMySQL:
    def __init__(self):
        self.db = self.connect()
        self.curosr = self.db.cursor()
        self.error_song_file = 'data/error_songs.txt'
        self.error_lysic_file = 'data/error_lysic.txt'
        self.error_sing_file = 'data/error_sings.txt'
        self.error_user_file = 'data/error_users.txt'
        self.error_playlist_file = 'data/error_playlist.txt'
        self.error_playlist_sing_file = 'data/error_playlist_sing.txt'
        self.error_playlist_tag_file = 'data/error_playlist_tag.txt'
        self.error_user_tag_file = 'data/error_user_tag.txt'

    # 连接到mysql数据库
    def connect(self):
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT,
                             charset='utf8')
        return db

    # 将歌曲信息写入数据库 ok
    """
        song_id = models.CharField(blank=False, max_length=64, verbose_name="歌曲ID", unique=True)
        song_name = models.CharField(blank=False, max_length=200, verbose_name="歌曲名字")
        song_pl_id = models.CharField(blank=False, max_length=64, verbose_name="专辑ID")
        song_publish_time = models.DateTimeField(blank=True, verbose_name="出版时间")
        song_sing_id = models.CharField(blank=False, max_length=200, verbose_name="歌手ID")
        song_total_comments = models.IntegerField(blank=True,verbose_name="歌曲总的评论数")
        song_hot_comments = models.IntegerField(blank=True,verbose_name="歌曲热门评论数")
        song_url = models.CharField(blank=True, max_length=1000, verbose_name="歌曲链接")
    """

    def song_mess_to_mysql(self):
        i = 0
        for line in open('../api/data/song_mess/songs_mess_all.txt', 'r', encoding='utf-8'):
            _list = line.split(' |+| ')
            if _list.__len__() == 9:
                [song_id, song_name, song_pl_id, song_publish_time, song_sing_id, song_total_comments,
                 song_hot_comments, size, song_url] = line.split(' |+| ')
                if song_publish_time is None or song_publish_time.lower() == 'null':
                    odf.write_to_file(self.error_song_file, line.replace('\n', ''))
                    continue
                s = Song(
                    song_id=song_id,
                    song_name=song_name,
                    song_pl_id=song_pl_id,
                    song_publish_time=ot.transform_time(abs(int(song_publish_time)) / 1000),
                    song_sing_id=song_sing_id,
                    song_total_comments=song_total_comments,
                    song_hot_comments=song_hot_comments,
                    song_url=song_url
                )
                try:
                    s.save()
                except Exception as e:
                    print(e)
                    print(song_id)
                    pass
            else:
                odf.write_to_file(self.error_song_file, line.replace('\n', ''))
                # print(line)
            i += 1
            print(i)
        print('Over!')

    # 歌词信息写入数据库 ok
    """
        song_id = models.CharField(blank=False, max_length=64, verbose_name="歌曲ID", unique=True)
        song_lysic = models.TextField(blank=True, verbose_name="歌词")
    """

    def song_lysic_to_mysql(self):
        i = 0
        for line in open('../api/data/song_mess/songs_lysics_all.txt', 'r', encoding='utf-8'):
            _list = line.strip().split('\t')
            songid = ''
            try:
                if _list.__len__() > 1:
                    songid = _list[0]
                    lysic = _list[1]
                    if lysic == 'null':
                        lysic = '暂无歌词提供！'
                    SongLysic(song_id=songid, song_lysic=lysic).save()
                else:
                    songid = _list[0]
                    lysic = '暂无提供歌词！'
                    SongLysic(song_id=songid, song_lysic=lysic).save()
                i += 1
                print(i)
            except Exception as e:
                print(e)
                print(songid)
                odf.write_to_file(self.error_lysic_file, line.replace('\n', ''))
        print('歌词信息写入数据库完成！')

    # 歌手信息写入数据库 ok
    """
        sing_id = models.CharField(blank=False, max_length=64, verbose_name="歌手ID", unique=True)
        sing_name = models.CharField(blank=False, max_length=100, verbose_name="歌手名字")
        sing_music_num = models.IntegerField(blank=False, verbose_name="音乐数目")
        sing_mv_num = models.IntegerField(blank=False, verbose_name="MV数目")
        sing_album_num = models.IntegerField(blank=False, verbose_name="专辑数目")
        sing_url = models.CharField(blank=True, max_length=1000, verbose_name="歌手图片")
    """

    def sing_mess_to_mysql(self):
        i = 0
        have_write_sing = list()
        for line in open('../api/data/sing_mess/sings_mess_all.txt', 'r', encoding='utf-8').readlines():
            _list = line.strip().split(',')
            if _list[0] in have_write_sing:
                continue
            if _list.__len__() == 6:
                sing_id, sing_name, sing_music_num, sing_mv_num, sing_album_num, sing_url = line.strip().split(',')
                s = Sing(
                    sing_id=sing_id,
                    sing_name=sing_name,
                    sing_music_num=sing_music_num,
                    sing_mv_num=sing_mv_num,
                    sing_album_num=sing_album_num,
                    sing_url=sing_url
                )
                try:
                    s.save()
                except Exception as e:
                    print(e)
                    print(sing_id)
                    pass
                have_write_sing.append(sing_id)
            else:
                print(_list)
                odf.write_to_file(self.error_sing_file, line.replace('\n', ''))
                # print(line)
            i += 1
            print(i)
        print('Over!')

    # 用户信息写入数据库 ok
    """
        u_id = models.CharField(blank=False, max_length=64, verbose_name="用户ID", unique=True)
        u_name = models.CharField(blank=False, max_length=150, verbose_name="用户昵称")
        u_birthday = models.DateField(blank=True, verbose_name="生日")
        u_gender = models.IntegerField(blank=True,verbose_name="用户性别")
        u_province = models.CharField(blank=True, max_length=20, verbose_name="用户省份")
        u_city = models.CharField(blank=True, max_length=20, verbose_name="用户城市")
        u_type = models.CharField(blank=True, max_length=10, verbose_name="用户类型")
        u_tags = models.CharField(blank=True, max_length=1000, verbose_name="用户标签")
        u_img_url = models.CharField(blank=True, max_length=1000, verbose_name="头像链接")
        u_auth_status = models.CharField(blank=True, max_length=10, verbose_name="用户状态")
        u_account_status = models.CharField(blank=True, max_length=10, verbose_name="账号状态")
        u_dj_status = models.CharField(blank=True, max_length=10, verbose_name="DJ状态")
        u_vip_type = models.CharField(blank=True, max_length=10, verbose_name="VIP状态")
        u_sign = models.TextField(blank=True, verbose_name="用户签名")
    """

    def user_mess_to_mysql(self):
        i = 0
        uid_list = list()
        for line in open('../api/data/user_mess/user_mess_all.txt', 'r', encoding='utf-8').readlines():
            if line.split(' |=| ').__len__() < 14:
                odf.write_to_file(self.error_user_file, line.replace('\n', ''))
                continue
            [u_id, u_name, u_birthday, u_gender, u_province, u_city, u_type, u_tags, u_img_url, u_auth_status,
             u_account_status, u_dj_status, u_vip_type, u_sign] = line.split(" |=| ")
            if u_birthday is None or u_birthday.lower() == 'null':
                odf.write_to_file(self.error_user_file, line.replace('\n', ''))
                continue
            elif u_id in uid_list:
                continue
            else:
                uid_list.append(u_id)
            try:
                user = User(
                    u_id=u_id,
                    u_name=u_name,
                    u_birthday=ot.transform_time(abs(float(int(u_birthday) / 1000))),
                    u_gender=int(u_gender),
                    u_province=u_province,
                    u_city=u_city,
                    u_type=u_type,
                    u_tags=u_tags.replace("[", "").replace("]", ""),
                    u_img_url=u_img_url,
                    u_auth_status=u_auth_status,
                    u_account_status=u_account_status,
                    u_dj_status=u_dj_status,
                    u_vip_type=u_vip_type,
                    u_sign='我就是我是颜色不一样的花火！' if u_sign == "\n" else u_sign
                )
                user.save()
            except Exception as e:
                user = User(
                    u_id=u_id,
                    u_name=u_name,
                    u_birthday=ot.transform_time(abs(float(int(u_birthday) / 1000))),
                    u_gender=int(u_gender),
                    u_province=u_province,
                    u_city=u_city,
                    u_type=u_type,
                    u_tags=u_tags.replace("[", "").replace("]", ""),
                    u_img_url=u_img_url,
                    u_auth_status=u_auth_status,
                    u_account_status=u_account_status,
                    u_dj_status=u_dj_status,
                    u_vip_type=u_vip_type,
                    u_sign='纵有诗论满腹，却道不尽这魏巍河山！'
                )
                user.save()
                print('Error:{},{}'.format(u_id, e))
            i += 1
            # print(i)
        print('Over!')

    # 歌单信息写入数据库 ok
    """
        pl_id = models.CharField(blank=False, max_length=64, verbose_name="ID", unique=True)
        pl_creator = models.ForeignKey(User, related_name="创建者信息", on_delete=False)
        pl_name = models.CharField(blank=False, max_length=64, verbose_name="歌单名字")
        pl_create_time = models.DateTimeField(blank=True, verbose_name="创建时间")
        pl_update_time = models.DateTimeField(blank=True, verbose_name="更新时间")
        pl_songs_num = models.IntegerField(blank=True,verbose_name="包含音乐数")
        pl_listen_num = models.IntegerField(blank=True,verbose_name="播放次数")
        pl_share_num = models.IntegerField(blank=True,verbose_name="分享次数")
        pl_comment_num = models.IntegerField(blank=True,verbose_name="评论次数")
        pl_follow_num = models.IntegerField(blank=True,verbose_name="收藏次数")
        pl_tags = models.CharField(blank=True, max_length=1000, verbose_name="歌单标签")
        pl_img_url = models.CharField(blank=True, max_length=1000, verbose_name="歌单封面")
        pl_desc = models.TextField(blank=True, verbose_name="歌单描述")
    """

    def playlist_mess_to_mysql(self):
        i = 0
        for line in open('../api/data/playlist_mess/pl_mess_all.txt', 'r', encoding='utf-8').readlines():
            if line.split(' |=| ').__len__() < 13:
                odf.write_to_file(self.error_playlist_file, line.replace('\n', ''))
                i += 1
                print(i)
                continue
            [pl_id, pl_creator, pl_name, pl_create_time, pl_update_time, pl_songs_num, pl_listen_num, pl_share_num,
             pl_comment_num, pl_follow_num, pl_tags, pl_img_url, pl_desc] = line.split(" |=| ")
            if pl_create_time is None or pl_create_time.lower() == 'null':
                odf.write_to_file(self.error_playlist_file, line.replace('\n', ''))
                i += 1
                print(i)
                continue
            try:
                user = User.objects.filter(u_id=pl_creator)[0]
                pl = PlayList(
                    pl_id=pl_id,
                    pl_creator=user,
                    pl_name=pl_name,
                    pl_create_time=ot.transform_time(abs(int(pl_create_time)) / 1000),
                    pl_update_time=ot.transform_time(abs(int(pl_update_time)) / 1000),
                    pl_songs_num=int(pl_songs_num),
                    pl_listen_num=int(pl_listen_num),
                    pl_share_num=int(pl_share_num),
                    pl_comment_num=int(pl_comment_num),
                    pl_follow_num=int(pl_follow_num),
                    pl_tags=str(pl_tags).replace("[", "").replace("]", "").replace("\'", ""),
                    pl_img_url=pl_img_url,
                    pl_desc=pl_desc
                )
                pl.save()
            except Exception as e:
                print(e)
                odf.write_to_file(self.error_playlist_file, line.replace('\n', ''))
            i += 1
            print(i)
        print('Over!')

    # 歌单和歌曲的id对应信息写入数据库 ok
    """
        pl_id = models.ForeignKey(PlayList, related_name="歌单ID", on_delete=False)
        song_id = models.ForeignKey(Song, related_name="歌曲ID", on_delete=False)
    """

    def playlist_sing_mess_to_mysql(self):
        i = 0
        for line in open('../api/data/playlist_mess/pl_sing_id.txt', 'r', encoding='utf-8'):
            pid, sids = line.strip().split('\t')
            for sid in str(sids).split(','):
                try:
                    pls = PlayListToSongs(pl_id=pid, song_id=sid)
                    pls.save()
                except Exception as e:
                    print(e, pid, sid)
                    odf.write_to_file(self.error_playlist_sing_file, pid + ',' + sid)
            i += 1
            print(i)
        print('歌单和歌曲ID对应信息写入完毕！')

    # 歌单和歌单tag写入数据库 ok
    def playlist_tag_mess_to_mysql(self):
        i = 0
        for line in open('../api/data/playlist_mess/pl_mess_all.txt', 'r', encoding='utf-8'):
            try:
                _list = line.split(' |=| ')
                if _list.__len__() > 10:
                    pl_id = _list[0]
                    tags = _list[10].replace('[', '').replace(']', '')
                    if tags.split(',').__len__() > 1:
                        for tag in tags.split(','):
                            PlayListToTag(pl_id=pl_id, tag=tag.replace("\'", "").replace(" ", "")).save()
                    else:
                        PlayListToTag(pl_id=pl_id, tag=tags.replace("\'", "").replace(" ", "")).save()

                else:
                    odf.write_to_file(self.error_playlist_tag_file, line.replace('\n', ''))
            except Exception as e:
                print(e)
                odf.write_to_file(self.error_playlist_tag_file, line.replace('\n', ''))
            i += 1
            print(i)
        print('Over!')

    # 歌手和歌手标签， 写入数据库
    def sing_tag_mess_to_mysql(self):
        # 1.歌手->歌曲
        sing_song_dict = dict()
        if os.path.exists('data/sing_song.json'):
            sing_song_dict = json.load(open('data/sing_song.json', 'r', encoding='utf-8'))
        else:
            for one in Song.objects.all().values('song_id', 'song_sing_id'):
                if '#' in one['song_sing_id']:
                    for sing in one['song_sing_id'].split('#'):
                        sing_song_dict[sing] = one['song_id']
                else:
                    sing_song_dict[one['song_sing_id']] = one['song_id']
            json.dump(sing_song_dict, open('data/sing_song.json', 'w', encoding='utf-8'))
        print(sing_song_dict)

        # 2.歌曲->歌单->标签
        song_playlist_tag_dict = dict()

        if os.path.exists('data/song_tag.json'):
            song_playlist_tag_dict = json.load(open('data/song_tag.json', 'r', encoding='utf-8'))
        else:
            for one in PlayListToSongs.objects.all():
                pl_tags = PlayList.objects.filter(pl_id=one.pl_id).values('pl_tags')
                if len(pl_tags) == 0:
                    continue
                if one.song_id in song_playlist_tag_dict.keys():
                    song_playlist_tag_dict[one.song_id] += ',' + pl_tags[0]['pl_tags']
                else:
                    song_playlist_tag_dict[one.song_id] = pl_tags[0]["pl_tags"]
            json.dump(song_playlist_tag_dict, open('data/song_tag.json', 'w', encoding='utf-8'))

        print(song_playlist_tag_dict)

        # 将歌曲 -> 标签信息写入数据库,直接写入数据库数据太多，写入文件，利用工具导入
        i = 0
        for song in song_playlist_tag_dict.keys():
            # print(song)
            song_have_write = list()
            for tag in song_playlist_tag_dict[song].split(","):
                tag = tag.replace(" ", "")
                if tag not in song_have_write:
                    SongTag(song_id=song, tag=tag).save()
                    song_have_write.append(tag)
                    i += 1
                    print('%s-歌曲ID：%s' % (i, song))

        fw = open("data/song_tag.txt", "a", encoding="utf-8")
        for song in song_playlist_tag_dict.keys():
            # print(song)
            song_have_write = list()
            for tag in song_playlist_tag_dict[song].split(","):
                tag = tag.replace(" ", "")
                if tag not in song_have_write:
                    fw.write(song + "," + tag + "\n")
                    song_have_write.append(tag)
        fw.close()
        print("Over !")

        # 将歌手 -> 标签信息写入数据库
        i = 0
        for sing in sing_song_dict.keys():
            # print(sing)
            song_id = sing_song_dict[sing]
            sing_have_write = list()
            if song_id not in song_playlist_tag_dict:
                continue
            for tag in song_playlist_tag_dict[song_id].split(","):
                tag = tag.replace(' ', '')
                if tag not in sing_have_write:
                    SingTag(sing_id=sing, tag=tag).save()
                    sing_have_write.append(tag)
                    i += 1
                    print('%s-歌手ID：%s' % (i, sing))

        print("Over !")

        fw1 = open('data/sing_tag.txt', 'a', encoding='utf-8')
        for sing in sing_song_dict.keys():
            # print(sing)
            song_id = sing_song_dict[sing]
            sing_have_write = list()
            if song_id not in song_playlist_tag_dict:
                continue
            for tag in song_playlist_tag_dict[song_id].split(','):
                tag = tag.replace(' ', '')
                if tag not in sing_have_write:
                    fw1.write(sing + ',' + tag + '\n')
                    sing_have_write.append(tag)
        fw1.close()
        print('Over!')

    # 将用户->标签写入数据库
    def user_tag_mess_to_mysql(self):
        i = 0
        for one in PlayList.objects.all():
            try:
                print(one)
                for tag in one.pl_tags.split(','):
                    UserTag(user_id=one.pl_creator.u_id, tag=tag.replace(' ', '')).save()
                    i += 1
                    print(i)
            except Exception as e:
                print(e)
                odf.write_to_file(self.error_user_tag_file, one)
        print('Over!')


if __name__ == '__main__':
    tomysql = ToMySQL()
    # 歌曲信息
    # tomysql.song_mess_to_mysql()
    # 歌词信息
    # tomysql.song_lysic_to_mysql()
    # 歌手信息
    # tomysql.sing_mess_to_mysql()
    # 用户信息
    # tomysql.user_mess_to_mysql()
    # 导入歌单信息
    # tomysql.playlist_mess_to_mysql()
    # 导入歌单和歌曲id的对应关系
    # tomysql.playlist_sing_mess_to_mysql()
    # 导入歌单和歌单标签对应关系
    # tomysql.playlist_tag_mess_to_mysql()
    # 歌手和歌手标签，歌曲与歌曲标签写入数据库
    tomysql.sing_tag_mess_to_mysql()
    # 导入用户和标签的对应关系
    # tomysql.user_tag_mess_to_mysql()
