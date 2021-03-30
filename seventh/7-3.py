# -*- coding:utf-8 -*-
import random
import math
import os
import json
from sklearn.model_selection import train_test_split


class NewItemCFRec:
    def __init__(self, datafile):
        self.alpha = 0.5
        self.beta = 0.8
        # 原始数据路径文件
        self.datafile = datafile
        # 测试集与训练集的比例
        self.train_data, self.test_data, self.max_data = self.load_data()
        self.item_sim = self.item_similarity_best()

    # 加载数据集并拆分为训练集和测试集
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
        # 将train和test转化为字典格式方法调用
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

    # 计算物品之间的相似度
    def item_similarity_best(self):
        print("开始计算物品之间的相似度...")
        if os.path.exists("data/item_sim.json"):
            print("物品相似度从文件加载...")
            item_sim = json.load(open("data/item_sim.json", "r"))
        else:
            item_sim = dict()
            item_eval_by_user_count = dict()  # 得到每个物品有多少用户产生过行为
            count = dict()  # 同现矩阵
            for user, items in self.train_data.items():
                print("user is {}".format(user))
                for i in items.keys():
                    item_eval_by_user_count.setdefault(i, 0)
                    if self.train_data[str(user)][i]['rate'] > 0.0:
                        item_eval_by_user_count[i] += 1
                    for j in items.keys():
                        count.setdefault(i, {}).setdefault(j, 0)
                        if self.train_data[str(user)][i]['rate'] > 0.0 and self.train_data[str(user)][j][
                            'rate'] > 0.0 and i != j:
                            count[i][j] += 1 * 1 / (1 + self.alpha * abs(
                                self.train_data[user][i]['time'] - self.train_data[user][i]['time']) / (24 * 60 * 60))
            # 同现矩阵=》相似度矩阵
            for i, retated_items in count.items():
                item_sim.setdefault(i, dict())
                for j, num in retated_items.items():
                    item_sim[i].setdefault(j, 0)
                    item_sim[i][j] = num / math.sqrt(item_eval_by_user_count[i] * item_eval_by_user_count[j])
        json.dump(item_sim, open("data/item_sim.json", "w"))
        return item_sim

    """
    为用户进行推荐
    user:用户
    k:k个临近物品
    nitems:总共返回n个物品
    """

    def recommend(self, user, k=8, nitems=40):
        # print("为用户推荐...")
        result = dict()
        u_items = self.train_data.get(user, {})
        for i, rate_time in u_items.items():
            for j, wj in sorted(self.item_sim[i].items(), key=lambda x: x[1], reverse=True)[0:k]:
                if j in u_items:
                    continue
                result.setdefault(j, 0)
                result[j] += rate_time['rate'] * wj * 1 / (1 + self.beta * (self.max_data - abs(rate_time['time'])))
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[0:nitems])

    # 计算准确率,由于测试集数据较大，这里选取10个用户进行测试，如果条件允许的话，可以使用全量用户进行测试
    def precision(self, k=8, nitems=10):
        print("开始计算准确率...")
        hit = 0
        precision = 0
        print(len(self.test_data.keys()))
        for user in random.sample(self.test_data.keys(), 10):
            print(user)
            u_items = self.test_data.get(user, {})
            result = self.recommend(user, k=k, nitems=nitems)
            for item, rate in result.items():
                if item in u_items:
                    hit += 1
            precision += nitems
        return hit / (precision * 1.0)


if __name__ == '__main__':
    ib = NewItemCFRec("../fifth/data/ml-1m/ratings.dat")
    print("用户1进行推荐结果如下:{}".format(ib.recommend("1")))
    print("准确率为:{}".format(ib.precision()))
