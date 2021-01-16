import numpy as np
import math


# 基于信息熵的数据离散化
class DiscreateByEntropy:
    """
    初始化数据
    """

    def __init__(self, group, threshold):
        self.max_group = group  # 最大分组数
        self.min_info_threshold = threshold  # 停止划分的最小熵
        self.result = dict()  # 保存划分结果

    # 准备数据
    def loaddata(self):
        data = np.array([[56, 1], [87, 1], [129, 0], [23, 0], [342, 1],
                         [641, 1], [63, 0], [2764, 1], [2323, 0], [453, 1],
                         [10, 1], [9, 0], [88, 1], [222, 0], [97, 0],
                         [2398, 1], [592, 1], [561, 1], [764, 0], [121, 1]])
        return data

    # 计算按照数据制定数据分组后的香农熵
    def calc_entropy(self, data):
        num_data = len(data)
        label_counts = {}
        for featues in data:
            # 获取标签。注:这个地方为啥用-1表示,Python数组的概念应该能找到答案
            one_label = featues[-1]
            # 如果标签不再新定义的字典里则创建该标签
            label_counts.setdefault(one_label, 0)
            # 该类标签下含有数据的个数
            label_counts[one_label] += 1
        shannonent = 0.0
        for key in label_counts:
            # 同类标签出现的概率
            prob = float(label_counts[key]) / num_data
            # 以2为底求对数
            shannonent -= prob * math.log2(prob)
        return shannonent

    # 按照调和信息熵最小化原则分割数据集
    def split_data(self, data):
        # inf为正无穷大
        min_entropy = np.inf
        # 记录最终分割索引
        index = -1
        # 按照第一列对数据进行排序
        sort_data = data[np.argsort(data[:, 0])]
        # 初始化最终分割数据后的熵
        last_e1, last_e2 = -1, -1
        # 返回数据结构，包含数据和对应的熵
        s1 = dict()
        s2 = dict()
        for i in range(len(sort_data)):
            # 分割数据集
            split_data1, split_data2 = sort_data[:i + 1], sort_data[i + 1:]
            entropy1, entropy2 = (self.calc_entropy(split_data1), self.calc_entropy(split_data2))
            # 计算信息熵
            entropy = entropy1 * len(split_data1) / len(sort_data) + \
                      entropy2 * len(split_data2) / len(sort_data)
            # 如果调和平均熵小于最小值
            if entropy < min_entropy:
                min_entropy = entropy
                index = i
                last_e1 = entropy1
                last_e2 = entropy2
        s1["entropy"] = last_e1
        s1["data"] = sort_data[:index + 1]
        s2["entropy"] = last_e2
        s2["data"] = sort_data[index + 1:]
        return s1, s2, min_entropy

    # 对数据进行分组
    def train_data(self, data):
        # 需要遍历的key
        need_split_key = [0]
        # 将整个数据作为一组
        self.result.setdefault(0, {})
        self.result[0]["entropy"] = np.inf
        self.result[0]["data"] = data
        group = 1
        for key in need_split_key:
            s1, s2, entropy = self.split_data(self.result[key]["data"])
            # 如果满足条件
            if entropy > self.min_info_threshold and group < self.max_group:
                self.result[key] = s1
                new_key = max(self.result.keys()) + 1
                self.result[new_key] = s2
                need_split_key.extend([key])
                need_split_key.extend([new_key])
                group += 1
            else:
                break


if __name__ == '__main__':
    dbe = DiscreateByEntropy(6, 0.5)
    dbe.train_data(dbe.loaddata())
    print("结果为:\n{}".format(dbe.result))
