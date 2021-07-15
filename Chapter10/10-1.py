from sklearn.model_selection import train_test_split
from sklearn import datasets
import pandas as pd


# 演示model_seletion中的train_test_split
def show_train_test_split(is_stratify):
    # 加载鸢尾花数据集
    x, y = datasets.load_iris(return_X_y=True)
    # 进行数据集拆分
    if is_stratify:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y, random_state=10)
    else:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=None, random_state=10)
    print('x_train的数据维度为:{}'.format(x_train.shape))
    print('x_test的数据维度为:{}'.format(x_test.shape))
    print('y_train的数据维度为:{}'.format(y_train.shape))
    print('y_test的数据维度为:{}'.format(y_test.shape))

    # 打印出训练数据集和测试数据集中各类目情况
    print('y_train中各类目对应的次数统计为:\n{}'.format(pd.value_counts(y_train)))
    print('y_test中各类目对应的次数统计为:\n{}'.format(pd.value_counts(y_test)))


# 调用
print("\n数据不分层")
show_train_test_split(is_stratify=False)  # 不分层
print("\n数据分层")
show_train_test_split(is_stratify=True)  # 分层
