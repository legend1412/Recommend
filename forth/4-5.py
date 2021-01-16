import numpy as np

np.seterr(divide='ignore', invalid='ignore')


# 利用KNN算法实现性别判定
class KNN:
    def __init__(self, k):
        self.k = k

    def createdata(self):
        features = np.array([[180, 76], [158, 43], [176, 78], [161, 49]])
        labels = ["男", "女", "男", "女"]
        return features, labels

    #  数据进行min-max标准化
    def normalization(self, data):
        maxs = np.max(data, axis=0)
        mins = np.min(data, axis=0)
        new_data = (data - mins) / (maxs - mins)
        return new_data, maxs, mins

    # 计算K最相邻
    def classify(self, one, data, labels):
        # 计算新样本与数据集中的每个样本质检的距离, 这里采用欧式距离计算
        differencedata = data - one
        squaredata = (differencedata ** 2).sum(axis=1)
        distance = squaredata ** 0.5
        sort_distance_index = distance.argsort()
        # 统计K最近邻的label
        label_cnt = dict()
        for i in range(self.k):
            label = labels[sort_distance_index[i]]
            label_cnt.setdefault(label, 0)
            label_cnt[label] += 1
        # 计算结果
        sort_label_cnt = sorted(label_cnt.items(), key=lambda x: x[1], reverse=True)
        print(sort_label_cnt)
        return sort_label_cnt[0][0]


if __name__ == '__main__':
    # 初始化类对象
    knn = KNN(3)
    # 创建数据集
    init_features, init_labels = knn.createdata()
    # 数据集标准化
    new_data_stan, max_data, min_data = knn.normalization(init_features)
    # 新数据标准化
    new_one = np.array([176, 76])
    new_one_stan = (new_one - min_data) / (max_data - min_data)
    # 计算新数据性别
    result = knn.classify(new_one_stan, new_data_stan, init_labels)
    print("数据{}的预测性别为:{}".format(new_one, result))
