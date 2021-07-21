# -*- coding:utf-8 -*-
from playlist.models import PlayList
from song.models import Song
from sing.models import Sing
from user.models import UserPlayListRec, UserSingRec, UserSongRec, User


def rank_result(request):
    uname = request.GET.get('username')
    user = User.objects.filter(u_name=uname)
    if user.__len__() != 0:
        u_id = user[0].u_id
        result = dict()
        result['code'] = 1
        result['data'] = dict()
        result['data']['playlist'] = rank_play_list(u_id)
        result['data']['song'] = rank_song(u_id)
        result['data']['sing'] = rank_singer(u_id)
        return result


# 歌单排行榜
def rank_play_list(u_id):
    result_pl = list()
    play_list = UserPlayListRec.objects.filter(user=u_id).order_by('-sim')[12:]
    for pl in play_list:
        one = PlayList.objects.filter(pl_id=pl.related)
        if one.__len__() == 0:
            continue
        else:
            one = one[0]
        result_pl.append({
            'pl_id': one.pl_id,
            'pl_creator': one.pl_creator.u_name,
            'pl_create_time': one.pl_create_time,
            'pl_name': one.pl_name,
            'pl_img_url': one.pl_img_url,
            'score': '%.2f' % pl.sim
        })
    return result_pl


# 歌曲排行榜
def rank_song(u_id):
    result_song = list()
    songs = UserSongRec.objects.filter(user=u_id).order_by('-sim')[12:]
    # print(songs)
    for song in songs:
        one = Song.objects.filter(song_id=song.related)
        if one.__len__() == 0:
            continue
        else:
            one = one[0]
        s_id = one.song_sing_id.split('#')[0] if one.song_sing_id.__contains__('#') else one.song_sing_id
        if s_id == '0':
            continue
        else:
            s = Sing.objects.filter(sing_id=s_id)
            if s.__len__() == 0:
                continue
            else:
                singer = s[0]
                result_song.append({
                    'song_id': one.song_id,
                    'song_name': one.song_name,
                    'song_singer_name': singer.sing_name,
                    'song_publish_time': one.song_publish_time,
                    'score': '%.2f' % song.sim
                })
    # print(result_song)
    return result_song


# 歌手排行榜
def rank_singer(u_id):
    result_sing = list()
    sings = UserSingRec.objects.filter(user=u_id).order_by('-sim')[12:]
    for sing in sings:
        one = Sing.objects.filter(sing_id=sing.related)
        if one.__len__() == 0:
            continue
        else:
            one = one[0]
        result_sing.append({
            'sing_id': one.sing_id,
            'sing_name': one.sing_name,
            'sing_url': one.sing_url,
            'sing_music_num': one.sing_music_num,
            'sing_mv_num': one.sing_mv_num,
            'sing_album_num': one.sing_album_num,
            'score': '%.2f' % sing.sim
        })
    return result_sing
