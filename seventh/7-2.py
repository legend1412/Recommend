# -*- coding:utf-8 -*-
import random
import math
import json
import os
from sklearn.model_selection import train_test_split


class UserCFRec:
    def __init__(self, datafile):
        self.alpha = 0.5
        self.beta = 0.8
        self.datafile = datafile
        self.train_data, self.test_data, self.max_data = self.load_data()
        self.users_sim = self.user_similarity_best()

    # 加载评分数据到data
    def load_data(self):
        print("加载数据...")
        data = list()
        max_data = 0
        for line in open(self.datafile):
            userid, itemid, record, timestamp = line.split("::")
            data.append((userid, itemid, int(record), int(timestamp)))
            if int(timestamp) > max_data:
                max_data = int(timestamp)
        # 调用sklearn中的train_test_split拆分训练集和测试集
        train_list, test_list = train_test_split(data, test_size=0.1, random_state=40)
        # 将train和test转换为字典格式方便调用
        train_dict = self.transform(train_list)
        test_dict = self.transform(test_list)
        return train_dict, test_dict, max_data

    # 将list转换为dict
    def transform(self, data):
        data_dict = dict()
        for user, item, record, timestamp in data:
            data_dict.setdefault(user, {}).setdefault(item, {})
            data_dict[user][item]['rate'] = record
            data_dict[user][item]['time'] = timestamp
        return data_dict

    # 计算用户之间的相似度，采用惩罚热门商品和优化算法复杂度的算法
    def user_similarity_best(self):
        print("开始计算用户之间的相似度...")
        if os.path.exists("data/user_sim.json"):
            print("用户相似度从文件加载...")
            user_sim = json.load(open("data/user_sim.json", "r"))
        else:
            # 得到每个item被哪些user评价过
            item_eval_by_users = dict()
            for u, items in self.train_data.items():
                for i in items.keys():
                    item_eval_by_users.setdefault(i, set())
                    if self.train_data[u][i]['rate'] > 0:
                        item_eval_by_users[i].add(u)

            # 构建倒排表
            count = dict()
            # 用户评价过多少个sku
            user_eval_item_count = dict()
            for i, users in item_eval_by_users.items():
                for u in users:
                    user_eval_item_count.setdefault(u, 0)
                    user_eval_item_count[u] += 1
                    count.setdefault(u, {})
                    for v in users:
                        count[u].setdefault(v, 0)
                        if u == v:
                            continue
                        count[u][v] += 1 / (1 + self.alpha * abs(
                            self.train_data[u][i]['time'] - self.train_data[v][i]['time']) / (
                                                    24 * 60 * 60) * 1 / math.log(1 + len(users)))

            # 构建相似度矩阵
            user_sim = dict()
            for u, related_users in count.items():
                user_sim.setdefault(u, {})
                for v, cuv in related_users.items():
                    if u == v:
                        continue
                    user_sim[u].setdefault(v, 0.0)
                    user_sim[u][v] = cuv / math.sqrt(user_eval_item_count[u] * user_eval_item_count[v])
            json.dump(user_sim, open("data/user_sim.json", "w"))
        return user_sim

    """
    为用户user进行物品推荐
    user:为用户user进行推荐
    k：选取k个近邻用户
    nitems：取nitems个物品
    """

    def recommend(self, user, k=8, nitems=40):
        rank = dict()
        interacted_items = self.train_data.get(user, {})
        for v, wuv in sorted(self.users_sim[user].items(), key=lambda x: x[1], reverse=True)[0:k]:
            for i, rvi in self.train_data[v].items():
                if i in interacted_items:
                    continue
                rank.setdefault(i, 0)
                rank[i] += wuv * rvi['rate'] * 1 / (1 + self.beta * (self.max_data - abs(rvi['time'])))
        return dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:nitems])

    """
    计算准确率
    k:近邻用户数
    nitems：推荐的item个数
    """

    def precision(self, k=8, nitems=10):
        print("开始计算准确率...")
        hit = 0
        precision = 0
        for user in self.train_data.keys():
            tu = self.test_data.get(user, {})
            rank = self.recommend(user, k=k, nitems=nitems)
            for item, rate in rank.items():
                if item in tu:
                    hit += 1
            precision += nitems
        return hit / (precision * 1.0)


if __name__ == '__main__':
    cf = UserCFRec("../fifth/data/ml-1m/ratings.dat")
    result_rec = cf.recommend("1")
    print("用户'1' 推荐结果为:{}".format(result_rec))
    result_pre = cf.precision()
    print("效果评估为:{}".format(result_pre))
