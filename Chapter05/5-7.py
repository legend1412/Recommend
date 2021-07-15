# -*- coding:utf-8 -*-
import random
import math
import os
import json


class ItemCFRec:
    def __init__(self, datafile, ratio):
        # 原始数据路径文件
        self.datafile = datafile
        # 测试集与训练集的比例
        self.ratio = ratio
        self.data = self.load_data()
        self.train_data, self.test_data = self.split_data(3, 47)
        self.item_sim = self.item_similarity_best()

    # 加载评分数据到data
    def load_data(self):
        print("加载数据...")
        data = []
        for line in open(self.datafile):
            userid, itemid, record, _ = line.split("::")
            data.append((userid, itemid, int(record)))
        return data

    """
    拆分数据集为 训练集和测试集
    k:参数
    seed:生成随机数的种子
    m:随机数上限
    """

    def split_data(self, k, seed, m=9):
        print("训练集与测试集切分...")
        train, test = {}, {}
        random.seed(seed)
        for user, item, record in self.data:
            if random.randint(0, m) == k:
                test.setdefault(user, {})
                test[user][item] = record
            else:
                train.setdefault(user, {})
                train[user][item] = record
        return train, test

    # 计算物品之间的相似度
    def item_similarity_best(self):
        print("开始计算物品之间的相似度...")
        if os.path.exists("data/item_sim.json"):
            print("物品相似度从文件加载...")
            item_sim = json.load(open("data/item_sim.json", "r"))
        else:
            item_sim = dict()
            item_user_count = dict()  # 得到每个物品有多少用户产生过行为
            count = dict()  # 同现矩阵
            for user, item in self.train_data.items():
                print("user is {}".format(user))
                for i in item.keys():
                    item_user_count.setdefault(i, 0)
                    if self.train_data[str(user)][i] > 0.0:
                        item_user_count[i] += 1
                    for j in item.keys():
                        count.setdefault(i, {}).setdefault(j, 0)
                        if self.train_data[str(user)][i] > 0.0 and self.train_data[str(user)][j] > 0.0 and i != j:
                            count[i][j] += 1
            # 同现矩阵=》相似度矩阵
            for i, retated_items in count.items():
                item_sim.setdefault(i, dict())
                for j, cuv in retated_items.items():
                    item_sim[i].setdefault(j, 0)
                    item_sim[i][j] = cuv / math.sqrt(item_user_count[i] * item_user_count[j])
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
        for i, pi in u_items.items():
            for j, wj in sorted(self.item_sim[i].items(), key=lambda x: x[1], reverse=True)[0:k]:
                if j in u_items:
                    continue
                result.setdefault(j, 0)
                result[j] += pi * wj
        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[0:nitems])

    # 计算准确率
    def precision(self, k=8, nitems=10):
        print("开始计算准确率...")
        hit = 0
        precision = 0
        for user in self.test_data.keys():
            u_items = self.test_data.get(user, {})
            result = self.recommend(user, k=k, nitems=nitems)
            for item, rate in result.items():
                if item in u_items:
                    hit += 1
            precision += nitems
        return hit / (precision * 1.0)


if __name__ == '__main__':
    ib = ItemCFRec("data/ml-1m/ratings.dat", [1, 9])
    print("用户1进行推荐结果如下:{}".format(ib.recommend("1")))
    print("准确率为:{}".format(ib.precision()))
