import numpy as np


# 使用PCA方法对数据进行降维
class PcaTest:
    # 初始数据
    def __init__(self, data):
        self.data = np.array(data)

    # 对特征进行标准化采用的是每列特征值减去该列特征的平均值
    def standard(self, data):
        # axis=0 按列去均值
        mean_vector = np.mean(data, axis=0)
        return data - mean_vector

    # 对标准化后的特征数据进行协方差矩阵计算
    def get_cov_matrix(self, newdata):
        # rowvar=False表示数据的每一列代表一个feature
        return np.cov(newdata, rowvar=False)

    # 计算协方差矩阵的特征值和特征向量
    def get_fvalue_fvector(self, covmatrix):
        fvalue, fvector = np.linalg.eig(covmatrix)
        return fvalue, fvector

    # 根据指定的维数，求出方差最大的列对应的特征向量，进而转化为n*k的特征向量矩阵
    # 其中：n为数据长度，k为指定的维数
    def get_vector_martrix(self, fvalue, fvector, k):
        fvalue_sort = np.argsort(fvalue)
        fvalue_top_n = fvalue_sort[:-(k + 1):-1]
        return fvector[:, fvalue_top_n]

    # 求出降维后的数据
    def get_result(self, data, vectormatrix):
        return np.dot(data, vectormatrix)


if __name__ == '__main__':
    init_data = [[1, 2], [-2, -3.5], [3, 5], [-4, -7]]
    pca = PcaTest(init_data)
    print("初始数据如下:\n{}".format(pca.data))
    stan_data = pca.standard(pca.data)
    print("标准化后特征数据如下:\n{}".format(stan_data))
    cov_data = pca.get_cov_matrix(stan_data)
    print("标准化后数特征数据的协方差矩阵为:\n{}".format(cov_data))
    value, vector = pca.get_fvalue_fvector(cov_data)
    print("特征值为:\n{}".format(value))
    print("特征向量为:\n{}".format(vector))
    feature_vector_data = pca.get_vector_martrix(value, vector, 1)
    print("方差最大的列对应的特征向量:\n{}".format(feature_vector_data))
    result = pca.get_result(stan_data, feature_vector_data)
    print("降维后计算结果为:\n{}".format(result))
