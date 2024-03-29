"""
Desc:
    获取提供的1066个歌单信息
"""
import traceback

import requests

import common.operdirandfiler as odf

from itertools import islice


# 获取每个歌单的信息类
class PlayList:
    def __init__(self):
        self.playlist_file = 'data/playlist_url/playlist_id_name_all.txt'
        # 获取出错的歌单id保存文件
        self.error_id_file = 'data/playlist_url/error_playlist_ids.txt'
        # 歌单创建者信息
        self.creator_mess = 'data/user_mess/'
        # 每个歌单的json信息
        self.playlist_mess = 'data/playlist_mess/'
        # 歌单包含的歌曲id信息
        self.trackid_mess = 'data/playlist_mess/'
        # 判断上述目录和文件是否存在，不存在就创建
        odf.mkfile(self.playlist_file)
        odf.mkfile(self.error_id_file)
        odf.mkdir(self.creator_mess)
        odf.mkdir(self.playlist_mess)
        odf.mkfile(self.trackid_mess)

        self.ids_list = self.get_ids()
        self.url = 'https://api.imjad.cn/cloudmusic/?type=playlist&id='
        # 获得的歌单信息出错的歌单id
        self.error_id = list()

    # 由歌单url，获取歌单id
    def get_ids(self):
        print('根据歌单链接获取歌单ID。。。')
        ids_list = list()
        fileopen = open(self.playlist_file, 'r', encoding='utf-8')
        for line in islice(fileopen, 1, None):
            try:
                pl_id = line.strip().split('\t')[0].split('id=')[1]
                ids_list.append(pl_id)
            except Exception as e:
                print(e)
                pass
        print('获取歌单ID完成。。。')
        return ids_list

    # 因为不可能一次性下载所有歌曲信息
    # 部分歌曲下载失败后，将歌单id写入了文件error_playlist_ids.txt，这个文件是把所有id都放到一行，中间用逗号隔开
    # 把里面的内容复制到另外的文件中，重新获取歌单id同时获取信息，这样循环，就能把所有的歌单的信息获取到
    def get_ids_error(self):
        print('获取失败的歌单ID')
        ids_list = list()
        fileopen = open('./data/playlist_url/playlist_get_fail.txt', 'r', encoding='utf-8')
        for line in islice(fileopen, 0, None):
            try:
                pl_id_arr = line.strip().split(',')
                for pl_id in pl_id_arr:
                    ids_list.append(pl_id)
            except Exception as e:
                print(e)
                pass
        print('解析错误歌单ID完成')
        return ids_list

    # 获取每个歌单的具体信息 url： https://api.imjad.cn/cloudmusic/?type=playlist&id=2340739428
    def get_every_playlist_mess(self):
        print('获取每个歌单的具体信息。。。')
        i = 0
        while self.ids_list.__len__() != 0:
            i += 1
            pl_id = self.ids_list.pop()
            # if pl_id != '2068079160':
            #     continue
            url = self.url + str(pl_id)
            try:
                print("%s - 歌单ID为：%s" % (i, pl_id))
                r = requests.get(url)
                # 解析信息
                self.get_format_playlist_mess(r.json())
            except Exception as e:
                # 将出错id写入记录一下，然后写入文件，出错时进行跳过
                print(e)
                traceback.print_exc()
                print("歌单ID为：%s 获取出错，进行记录" % pl_id)
                self.error_id.append(pl_id)
                pass
            # break
        odf.write_to_file(self.error_id_file, ",".join(self.error_id))
        print("歌单信息获取完毕，写入文件: %s" % self.playlist_file)

    # 每个歌单的内容进行格式化处理 写入文件
    # 需要获取的信息: 歌单信息、创建者信息、歌单音乐信息
    def get_format_playlist_mess(self, json_line):
        # 创建者信息 用户id，昵称，生日，性别，省份，城市，类型，标签，头像链接，用户状态，账号状态，djStatus,vipStatus，签名
        creator = json_line['playlist']['creator']
        c_list = (
            str(creator['userId']),
            str(creator["nickname"]),
            str(creator["birthday"]),
            str(creator["gender"]),
            str(creator["province"]),
            str(creator["city"]),
            str(creator["userType"]),
            str(creator["expertTags"]),
            str(creator["avatarUrl"]),
            str(creator["authStatus"]),
            str(creator["accountStatus"]),
            str(creator["djStatus"]),
            str(creator["vipType"]),
            str(creator["signature"]).replace('\n', '无签名')
        )
        odf.write_to_file(self.creator_mess + 'user_mess_all.txt', ' |=| '.join(c_list))
        # 歌单信息
        # 歌单ID，创建者ID，名字，创建时间，更新时间，包含音乐数，播放次数，分享次数，评论次数，收藏次数，标签，歌单封面，描述
        playlist = json_line["playlist"]
        p_list = [
            str(playlist["id"]),
            str(playlist["userId"]),
            str(playlist["name"]).replace("\n", ""),
            str(playlist["createTime"]),
            str(playlist["updateTime"]),
            str(playlist["trackCount"]),
            str(playlist["playCount"]),
            str(playlist["shareCount"]),
            str(playlist["commentCount"]),
            str(playlist["subscribedCount"]),
            str(playlist["tags"]),
            str(playlist["coverImgUrl"]),
            str(playlist["description"]).replace("\n", "无描述")
        ]
        odf.write_to_file(self.playlist_mess + "pl_mess_all.txt", " |=| ".join(p_list))

        # 歌单包含的歌曲信息
        t_list = list()
        trackids = json_line["playlist"]["trackIds"]
        for one in trackids:
            t_list.append(str(one["id"]))
        odf.write_to_file(self.trackid_mess + "pl_sing_id_1.txt", str(playlist["id"]) + "\t" + ",".join(t_list))


if __name__ == '__main__':
    print("开始获取歌单信息 ..")
    pl = PlayList()
    pl.get_every_playlist_mess()
    print("歌单信息获取完毕 ... Bye !")
