import pandas as pd
import math


class RecBaseTag:
    # 由于从文件读取的为字符串，统一格式为整数，方便后续计算
    def __init__(self):
        # 用户听过艺术家的次数文件
        self.user_rate_file = 'data/lastfm-2k/user_artists.dat'
        # 用户打标信息
        self.user_tag_file = 'data/lastfm-2k/user_taggedartists.dat'

        # 获取所有的艺术家ID
        self.artists_all = list(pd.read_table('data/lastfm-2k/artists.dat', delimiter='\t')['id'].values)
        # 用户对艺术家的评分
        self.user_rate_dict = self.get_user_rate()
        # 艺术家与标签的相关度
        self.artists_tag_dict = self.get_artists_tags()
        # 用户对每个标签打标的次数统计和每个标签被所有用户打标的次数统计
        self.user_tag_dict, self.tag_user_dict = self.get_user_tag_num()
        # 用户最终对每个标签的喜好程度
        self.user_tag_pre = self.get_user_tag_pre()

    # 用户对艺术家的评分
    def get_user_rate(self):
        user_rate_dict = dict()
        fr = open(self.user_rate_file, 'r', encoding='utf-8')
        for line in fr.readlines():
            if not line.startswith('userID'):
                userID, artistID, weight = line.split('\t')
                user_rate_dict.setdefault(int(userID), {})
                # 对听歌次数进行适当比例的缩放，避免计算结果过大
                user_rate_dict[int(userID)][int(artistID)] = float(weight) / 10000
        return user_rate_dict

    # 获取艺术家对应的标签基因，这里的相关度全部为1
    # 由于艺术家和tag过多，存储到一个矩阵中维度太大，这里优化存储结构
    # 如果艺术家有对应的标签则记录，相关度为1，否则不为1
    def get_artists_tags(self):
        artists_tags_dict = dict()
        for line in open(self.user_tag_file, 'r', encoding='utf-8'):
            if not line.startswith('userID'):
                artistID, tagID = line.split('\t')[1:3]
                artists_tags_dict.setdefault(int(artistID), {})
                artists_tags_dict[int(artistID)][int(tagID)] = 1
        return artists_tags_dict

    # 获取每个用户打标的标签和每个标签被所有用户打标的次数
    def get_user_tag_num(self):
        user_tag_dict = dict()
        tag_user_dict = dict()
        for line in open(self.user_tag_file, 'r', encoding='utf-8'):
            if not line.startswith('userID'):
                userID, artistID, tagID = line.strip().split('\t')[:3]
                # 统计每个标签被打标的次数
                if int(tagID) in tag_user_dict.keys():
                    tag_user_dict[int(tagID)] += 1
                else:
                    tag_user_dict[int(tagID)] = 1
                # 统计每个用户对每个标签的打标次数
                user_tag_dict.setdefault(int(userID), {})
                if int(tagID) in user_tag_dict[int(userID)].keys():
                    user_tag_dict[int(userID)][int(tagID)] += 1
                else:
                    user_tag_dict[int(userID)][int(tagID)] = 1
        return user_tag_dict, tag_user_dict

    # 获取用户对标签的最终兴趣度
    def get_user_tag_pre(self):
        user_tag_pre = dict()
        user_tag_count = dict()
        # num为用户打标的总条数
        num = len(open(self.user_tag_file, 'r', encoding='utf-8').readlines())
        for line in open(self.user_tag_file, 'r', encoding='utf-8').readlines():
            if not line.startswith('userID'):
                userID, artistID, tagID = line.split('\t')[:3]
                user_tag_pre.setdefault(int(userID), {})
                user_tag_count.setdefault(int(userID), {})
                rate_ui = (self.user_rate_dict[int(userID)][int(artistID)]
                           if int(artistID) in self.user_rate_dict[int(userID)].keys()
                           else 0)
                if int(tagID) not in user_tag_pre[int(userID)].keys():
                    user_tag_pre[int(userID)][int(tagID)] = (
                            rate_ui * self.artists_tag_dict[int(artistID)][int(tagID)]
                    )
                    user_tag_count[int(userID)][int(tagID)] = 1
                else:
                    user_tag_pre[int(userID)][int(tagID)] += (
                            rate_ui * self.artists_tag_dict[int(artistID)][int(tagID)]
                    )
                    user_tag_count[int(userID)][int(tagID)] += 1

        for userID in user_tag_pre.keys():
            for tagID in user_tag_pre[userID].keys():
                tf_ut = self.user_tag_dict[int(userID)][int(tagID)] / sum(self.user_tag_dict[int(userID)].values())
                idf_ut = math.log(num * 1.0 / (self.tag_user_dict[int(tagID)] + 1))
                user_tag_pre[userID][tagID] = (
                        user_tag_pre[userID][tagID] / user_tag_count[userID][tagID] * tf_ut * idf_ut)
        return user_tag_pre

    # 对用户进行艺术家推荐
    def recommend_for_user(self, user, k, flag=True):
        user_artist_pre_dict = dict()
        # 得到用户没有打标过的艺术家
        for artist in self.artists_all:
            if int(artist) in self.artists_tag_dict.keys():
                # 计算用户对艺术家的喜好程度
                for tag in self.user_tag_pre[int(user)].keys():
                    rate_ut = self.user_tag_pre[int(user)][int(tag)]
                    rel_it = (0
                              if tag not in self.artists_tag_dict[int(artist)].keys()
                              else self.artists_tag_dict[int(artist)][tag])
                    if artist in user_artist_pre_dict.keys():
                        user_artist_pre_dict[int(artist)] += rate_ut * rel_it
                    else:
                        user_artist_pre_dict[int(artist)] = rate_ut * rel_it

        new_user_artist_pre_dict = dict()
        if flag:
            # 对推荐结果进行过滤，过滤掉用户已经听过的
            for artist in user_artist_pre_dict.keys():
                if artist not in self.user_rate_dict[int(user)].keys():
                    new_user_artist_pre_dict[artist] = user_artist_pre_dict[int(artist)]
            return sorted(new_user_artist_pre_dict.items(), key=lambda x: x[1], reverse=True)[:k]
        else:
            # 表示用来进行效果评估
            return sorted(user_artist_pre_dict.items(), key=lambda x: x[1], reverse=True)[:k]

    # 效果评估 重合度
    def evaluate(self, user):
        k = len(self.user_rate_dict[int(user)])
        rec_result = self.recommend_for_user(user, k=k, flag=False)
        count = 0
        for (artist, pre) in rec_result:
            if artist in self.user_rate_dict[int(user)]:
                count += 1
        return count * 1.0 / k


if __name__ == '__main__':
    rbt = RecBaseTag()
    print(rbt.recommend_for_user('2', k=20))
    print(rbt.evaluate('2'))
