import json
import pandas as pd
import numpy as np
import math
import random


class CBRecommend:
    # 加载5-2中预处理的数据
    def __init__(self, k):
        # 给用户推荐item个数
        self.k = k
        self.item_profile = json.load(open('data/item_profile.json', 'r'))
        self.user_profile = json.load(open('data/user_profile.json', 'r'))

    # 获取用户未评分的item列表
    def get_none_score_item(self, user):
        items = pd.read_csv('data/ml-1m/movies.csv')['MovieID'].values
        ratings = pd.read_csv('data/ml-1m/ratings.csv')
        have_score_items = ratings[ratings['UserID'] == user]['MovieID'].values
        none_score_item = set(items) - set(have_score_items)
        return none_score_item

    # 获取用户对item的喜好程度
    def cos_ui(self, user, item):
        uia = sum(np.array(self.user_profile[str(user)]) * np.array(self.item_profile[str(item)]))
        ua = math.sqrt(sum([math.pow(one, 2) for one in self.user_profile[str(user)]]))
        ia = math.sqrt(sum([math.pow(one, 2) for one in self.item_profile[str(item)]]))
        return uia / (ua * ia)

    # 为用户进行电影推荐
    def recommend(self, user):
        user_result = {}
        item_list = self.get_none_score_item(user)
        for item in item_list:
            user_result[item] = self.cos_ui(user, item)
        if self.k is None:
            result = sorted(user_result.items(), key=lambda k: k[1], reverse=True)
        else:
            result = sorted(user_result.items(), key=lambda k: k[1], reverse=True)[:self.k]
        print('推荐结果:{}'.format(result))

    # 推荐系统的效果评估
    def evaluate(self):
        evas = []
        data = pd.read_csv('data/ml-1m/ratings.csv')
        # 随机选取20个用户进行效果评估
        for user in random.sample([one for one in range(1, 6041)], 20):
            have_score_items = data[data['UserID'] == user]['MovieID'].values
            items = pd.read_csv('data/ml-1m/movies.csv')['MovieID'].values
            user_result = {}
            for item in items:
                user_result[item] = self.cos_ui(user, item)
            results = sorted(user_result.items(), key=lambda k: k[1], reverse=True)[:len(have_score_items)]
            rec_items = []
            for one in results:
                rec_items.append(one[0])
            eva = len(set(rec_items) & set(have_score_items)) / len(have_score_items)
            evas.append(eva)
        return sum(evas) / len(evas)


if __name__ == '__main__':
    cb = CBRecommend(k=10)
    cb.recommend(1)
    print('推荐效果评估:{}'.format(cb.evaluate()))
