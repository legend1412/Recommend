import numpy as np
from sklearn import datasets


# 对鸢尾花数据集特征进行降维

class Pca:
    def __init__(self):
        pass

    # 加载鸢尾花数据集中的特征作为PCA的原始数据集并进行标准化
    def init_load_iris(self):
        data = datasets.load_iris()["data"]
        return data

    # 数据标准化
    def data_standard(self, data):
        # axis=0 按列取均值
        mean = np.mean(data, axis=0)
        return mean, data - mean

    # 计算协方差矩阵
    def calc_cov_matrix(self, data):
        # rowvar=false表示数据的每一列代表一个feature
        return np.cov(data, rowvar=False)

    # 计算协方差矩阵的特征值和特征向量
    def calc_fvalue_fvector(self, covmatrix):
        fvalue, fvector = np.linalg.eig(covmatrix)
        return fvalue, fvector

    # 得到特征向量矩阵
    def get_vector_matrix(self, fvalue, fvector, k):
        fvalue_sort = np.argsort(fvalue)
        fvalue_top_n = fvalue_sort[:-(k + 1):-1]
        return fvector[:, fvalue_top_n]

    # 得到降维后数据
    def get_result_data(self, data, vectormatrix):
        return np.dot(data, vectormatrix)


if __name__ == '__main__':
    # 创建PCA对象
    pca = Pca()
    # 加载iris数据集
    init_data = pca.init_load_iris()
    print("初始数据为:\n{}".format(init_data))
    # 归一化数据
    mean_vector, newdata = pca.data_standard(init_data)
    # 得到协方差矩阵:
    cov_matrix = pca.calc_cov_matrix(newdata)
    print("协方差矩阵为:\n{}".format(cov_matrix))
    # 得到特征值和特征向量
    value, vector = pca.calc_fvalue_fvector(cov_matrix)
    print("特征值为:\n{}".format(value))
    print("特征向量为:\n{}".format(vector))
    # 得到要降到k维的特征向量矩阵
    n = 2
    vector_matrix = pca.get_vector_matrix(value, vector, n)
    print(str(n) + "维特征向量矩阵为:\n{}".format(vector_matrix))
    # 计算结果
    result_data = pca.get_result_data(newdata, vector_matrix)
    print("最终降维结果为:\n{}".format(result_data))
    # 得到重构数据
    print("最终重构结果为:\n{}".format(np.mat(result_data) * vector_matrix.T + mean_vector))
