# -*- coding:utf-8 -*-
import math
import os
import json
import random

train_file_path = "data/train.json"
test_file_path = "data/test.json"


class FirstRec:
    """
    初始化函数
    filePath:原始文件路径
    seed:产生随机数的种子
    k:选取的近邻用户个数
    n_items:为每个用户推荐的电影数
    """

    def __init__(self, file_path, seed, k, n_items):
        self.file_path = file_path
        self.users_1000 = self.__select__1000_users()
        self.seed = seed
        self.k = k
        self.n_items = n_items
        self.train, self.test = self._load_and_split_data()

    # 获取所有用户并随机选取1000个
    def __select__1000_users(self):
        print("随机选取1000个用户!")
        if os.path.exists(train_file_path) and os.path.exists(test_file_path):
            print("已存在相关记录，忽略选择")
            return list()
        else:
            users = set()
            # 获取所有用户
            for file in os.listdir(self.file_path):
                one_path = "{}/{}".format(self.file_path, file)
                print("{}".format(one_path))
                with open(one_path, "r") as fp:
                    for line in fp.readlines():
                        if line.strip().endswith(":"):
                            continue
                        userid, _, _ = line.split(",")
                        users.add(userid)
                # break
            users_1000 = random.sample(list(users), 1000)
            print(users_1000)
            return users_1000

    # 加载数据，并拆分为训练集和测试集
    def _load_and_split_data(self):
        train = dict()
        test = dict()
        if os.path.exists(train_file_path) and os.path.exists(test_file_path):
            print("从文件中加载训练集和测试集")
            train = json.load(open(train_file_path))
            test = json.load(open(test_file_path))
            print("从文件中加载数据完成")
        else:
            # 设置产生随机数的种子，保证每次实验产生的随机结果一致
            random.seed(self.seed)
            for file in os.listdir(self.file_path):
                one_path = "{}/{}".format(self.file_path, file)
                print("{}".format(one_path))
                with open(one_path, "r") as fp:
                    movieid = fp.readline().split(":")[0]
                    for line in fp.readlines():
                        if line.endswith(":"):
                            continue
                        userid, rate, _ = line.split(",")
                        # 判断用户是否在所选择的1000个用户中
                        if userid in self.users_1000:
                            if random.randint(1, 50) == 1:
                                test.setdefault(userid, {})[movieid] = int(rate)
                            else:
                                train.setdefault(userid, {})[movieid] = int(rate)
                # break
            print("加载数据到" + train_file_path + "和" + test_file_path)
            json.dump(train, open(train_file_path, "w"))
            json.dump(test, open(test_file_path, "w"))
            print("加载数据完成")
        return train, test

    """
    计算皮尔逊相关系数
     rating1:用户1的评分记录，形式如{"movieid1":rate1,"movieid2":rate2,...}
     rating2:用户2的评分记录，形式如{"movieid1":rate1,"movieid2":rate2,...}
    """

    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        num = 0
        for key in rating1.keys():
            if key in rating2.keys():
                num += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += math.pow(x, 2)
                sum_y2 += math.pow(y, 2)
        if num == 0:
            return 0
        # 皮尔逊相关系数分母
        denominator = math.sqrt(sum_x2 - math.pow(sum_x, 2) / num) \
                      * math.sqrt(sum_y2 - math.pow(sum_y, 2) / num)
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / num) / denominator

    """
    用户userid进行电影推荐
        userid：用户ID
    """

    def recommend(self, userid):
        neighboruser = dict()
        for user in self.train.keys():
            if userid != user:
                distance = self.pearson(self.train[userid], self.train[user])
                neighboruser[user] = distance
        # 字典排序
        newnu = sorted(neighboruser.items(), key=lambda k: k[1], reverse=True)

        movies = dict()
        for (sim_user, sim) in newnu[:self.k]:
            for movieid in self.train[sim_user].keys():
                movies.setdefault(movieid, 0)
                movies[movieid] += sim * self.train[sim_user][movieid]
        # 字典排序
        newmovies = sorted(movies.items(), key=lambda k: k[1], reverse=True)
        return newmovies

    """
    推荐系统效果评估函数
        num:随机抽取num个用户计算准确率
    """

    def evaluate(self, num=30):
        print("开始计算准确率")
        precisions = list()
        random.seed(10)
        for userid in random.sample(self.test.keys(), num):
            hit = 0
            result = self.recommend(userid)[:self.n_items]
            for (item, rate) in result:
                if item in self.test[userid]:
                    hit += 1
            precisions.append(hit / self.n_items)
        return sum(precisions) / precisions.__len__()


if __name__ == '__main__':
    init_file_path = "data/netflix/training_set"
    init_seed = 30
    init_k = 15
    init_n_items = 20
    f_rec = FirstRec(init_file_path, init_seed, init_k, init_n_items)
    # 计算用户198936和1653016的皮尔逊相关系数
    r = f_rec.pearson(f_rec.train["198936"], f_rec.train["1653016"])
    print("用户198936和1653016的皮尔逊相关系数为:{}".format(r))
    # 为用户进行电影推荐
    init_userid = "198936"
    rec_result = f_rec.recommend(init_userid)
    print("为用户" + init_userid + "推荐的电影为：" + str(rec_result))
    print("算法的推荐准确率为:{}".format(f_rec.evaluate()))
