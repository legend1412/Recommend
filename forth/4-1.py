# -*-coding:utf-8-*-
import numpy as np
import math


# 实现数据标准化
class DataNorm:
    def __init__(self):
        self.arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.x_max = max(self.arr)  # 最大值
        self.x_min = min(self.arr)  # 最小值
        self.x_mean = sum(self.arr) / len(self.arr)  # 平均值
        self.x_std = np.std(self.arr)

    # Min-Max标准化
    def min_max(self):
        arr_ = list()
        for x in self.arr:
            # round(x,4) 对x保留4位小数
            arr_.append(round((x - self.x_min) / (self.x_max - self.x_min), 4))
        print("经过'Min-Max'标准化后的数据为:\n{}".format(arr_))

    # Z_Score标准化
    def z_score(self):
        arr_ = list()
        for x in self.arr:
            arr_.append(round((x - self.x_mean) / self.x_std, 4))
        print("经过'Z_Score'标准化后的数据为:\n{}".format(arr_))

    # 小数定标标准化(DecimalScaling)
    def decimal_scaling(self):
        arr_ = list()
        j = 1
        x_max = max([abs(one) for one in self.arr])
        while x_max / 10 >= 1.0:
            j += 1
            x_max = x_max / 10
        for x in self.arr:
            arr_.append(round(x / math.pow(10, j), 4))
        print("经过'小数定标(DecimalScaling)'标准化后的数据为:\n{}".format(arr_))

    # 均值归一化法
    def mean(self):
        arr_ = list()
        for x in self.arr:
            arr_.append(round((x - self.x_mean) / (self.x_max - self.x_min), 4))
        print("经过'均值归一化法'标准化后的数据为:\n{}".format(arr_))

    # 向量归一化
    def vector(self):
        arr_ = list()
        for x in self.arr:
            arr_.append(round(x / sum(self.arr), 4))
        print("经过'向量归一化'标准化后的数据为:\n{}".format(arr_))

    # 指数转换
    def exonential(self):
        arr_1 = list()
        for x in self.arr:
            arr_1.append(round(math.log10(x) / math.log10(self.x_max), 4))
        print("经过'指数转换法(log10)'标准化后的数据为:\n{}".format(arr_1))

        arr_2 = list()
        sum_e = sum([math.exp(one) for one in self.arr])
        for x in self.arr:
            arr_2.append(round(math.exp(x) / sum_e, 4))
        print("经过'指数转换法(Softman)'标准化后的数据为:\n{}".format(arr_2))

        arr_3 = list()
        for x in self.arr:
            arr_3.append(round(1 / (1 + math.exp(-x)), 4))
        print("经过'指数转换法(Sigmoid)'标准化后的数据为:\n{}".format(arr_3))


if __name__ == '__main__':
    dn = DataNorm()
    dn.min_max()
    dn.z_score()
    dn.decimal_scaling()
    dn.mean()
    dn.vector()
    dn.exonential()
