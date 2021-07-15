import numpy as np
import pandas as pd
import random


class KMeans:
    def __init__(self):
        pass

    # 加载数据集
    def load_data(self, file):
        return pd.read_csv(file, header=0, sep=',')

    # 去除异常值，使用正态分布方法，同事保证最大异常值为5000，最小异常值为1
    def filter_anomaly_value(self, data):
        upper = np.mean(data['price']) + 3 * np.std(data['price'])
        lower = np.mean(data['price']) - 3 * np.std(data['price'])
        upper_limit = upper if upper > 5000 else 5000
        lower_limit = lower if lower > 1 else 1
        print('最大异常值为:{},最小异常值为:{}'.format(upper_limit, lower_limit))
        # 过滤掉大于最大异常值和小于最小异常值的
        new_data = data[(data['price'] < upper_limit) & (data['price'] > lower_limit)]
        return new_data, upper_limit, lower_limit

    # 初始化簇类中心
    def init_centers(self, values, k, cluster):
        random.seed(100)
        old_centers = list()
        for i in range(k):
            index = random.randint(0, len(values))
            cluster.setdefault(i, {})
            cluster[i]['center'] = values[index]
            cluster[i]['values'] = []

            old_centers.append(values[index])

        return old_centers, cluster

    # 计算任意两条数据之间的欧氏距离
    # noinspection PyMethodMayBeStatic
    def distance(self, price1, price2):
        return np.emath.sqrt(pow(price1 - price2, 2))

    # 聚类
    def k_means(self, data, k, maxiters):
        cluster = dict()  # 最终聚类结果
        old_centers, cluster = self.init_centers(data, k, cluster)
        print('初始的簇类中心为:{}'.format(old_centers))
        # 标志变量,若为true，则继续迭代
        cluster_changed = True
        i = 0  # 记录迭代次数，最大迭代
        while cluster_changed:
            for price in data:
                # 每条数据与最近簇类中心的距离，初始化为正去穷大
                min_distance = np.inf
                # 每条数据对应的索引，初始化为-1
                min_index = -1
                for key in cluster.keys():
                    # 计算每条数据到簇类中心的距离
                    dis = self.distance(price, cluster[key]['center'])
                    if dis < min_distance:
                        min_distance = dis
                        min_index = key

                cluster[min_index]['values'].append(price)

            new_centers = list()
            for key in cluster.keys():
                new_center = np.mean(cluster[key]['values'])
                cluster[key]['center'] = new_center
                new_centers.append(new_center)
            print('第{}次迭代后的簇类中心为:{}'.format(i, new_centers))
            if old_centers == new_centers or i > maxiters:
                cluster_changed = False
            else:
                old_centers = new_centers
                i += 1
                # 删除cluster中记录的簇类值
                for key in cluster.keys():
                    cluster[key]['values'] = []

        return cluster
