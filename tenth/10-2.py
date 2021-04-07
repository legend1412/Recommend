from sklearn.model_selection import KFold
import numpy as np


# 以生成器的方式产生每次需要的训练数据集和测试数据集
def show_kfold_test():
    x = np.random.randint(1, 10, 20)
    # n_splits k折交叉验证
    kf = KFold(n_splits=5)
    # 返回的数据的下标
    i = 1
    for train_index, test_index in kf.split(x):
        print('第{}次：'.format(i))
        print('train数据为:{}'.format(train_index))
        print('test数据为:{}'.format(test_index))
        i += 1


# 交叉验证
show_kfold_test()
