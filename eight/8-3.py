# -*- coding:utf-8 -*-
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import mean_squared_error
import pandas as pd


class ChurnPredWithLR:
    def __init__(self):
        self.file = 'data/new_churn.csv'
        self.data = self.load_data()
        self.train, self.test = self.split()

    # 加载数据
    def load_data(self):
        print("加载数据")
        data = pd.read_csv(self.file)
        labels = list(data.keys())
        # 构建labels和对应的value映射
        fdict = dict()
        for f in labels:
            if f not in ['customer_id', 'tenure', 'monthly_charges', 'total_charges', 'churn']:
                fdict[f] = sorted(list(data.get(f).unique()))
        # 写入文件
        fw = open('data/one_hot_churn.csv', 'w')
        fw.write('customer_id,')
        for i in range(1, 47):
            fw.write('f_%s,' % i)
        fw.write('churn\n')
        for line in data.values:
            list_line = list(line)
            # 存放一行one hot编码后的结果
            list_result = list()
            for i in range(0, list_line.__len__()):
                if labels[i] in ['customer_id', 'tenure', 'monthly_charges', 'total_charges', 'churn']:
                    list_result.append(list_line[i])
                else:
                    # 创建one hot数组，看该label下对应多少个不同的值
                    arr = [0] * fdict[labels[i]].__len__()
                    # 值的下标
                    ind = fdict[labels[i]].index(list_line[i])
                    # 让对应位置为1，其余位置为0
                    arr[ind] = 1
                    for one in arr:
                        list_result.append(one)
            fw.write(",".join([str(f) for f in list_result]) + "\n")
        fw.close()
        return pd.read_csv('data/one_hot_churn.csv')

    # 拆分数据集
    def split(self):
        print("拆分数据集")
        train, test = train_test_split(self.data, test_size=0.1, random_state=40)
        return train, test

    # 模型训练
    def train_model(self):
        print("模型训练")
        lable = "churn"
        customer_id = "customer_id"
        x_columns = [x for x in self.train.columns if x not in [lable, customer_id]]
        x_train = self.train[x_columns]
        y_train = self.train[lable]
        # 定义模型
        lr = LogisticRegression(penalty='l2', tol=1e-4, fit_intercept=True)
        lr.fit(x_train, y_train)
        return lr

    # 模型评估
    def evaluate(self, lr, type_evaluate):
        print("模型评估")
        lable = "churn"
        customer_id = "customer_id"
        x_columns = [x for x in self.test.columns if x not in [lable, customer_id]]
        x_test = self.test[x_columns]
        y_test = self.test[lable]
        new_y_pred = None

        if type_evaluate == 1:
            y_pred = lr.predict(x_test)
            new_y_pred = y_pred
        elif type_evaluate == 2:
            y_pred = lr.predict_proba(x_test)
            new_y_pred = list()
            for y in y_pred:
                new_y_pred.append(1 if y[1] > 0.5 else 0)
        mse = mean_squared_error(y_test, new_y_pred)
        print("LR-MSE:%.4f" % mse)
        accuracy = metrics.accuracy_score(y_test.values, new_y_pred)
        print("LR-Accuracy:%.4g" % accuracy)
        auc = metrics.roc_auc_score(y_test.values, new_y_pred)
        print("LR-AUC Score:%.4g" % auc)


if __name__ == '__main__':
    pred = ChurnPredWithLR()
    lr_result = pred.train_model()
    # type_evaluate=1:表示输出0,1,type_evaluate=2：表示输出概率
    pred.evaluate(lr_result, type_evaluate=1)
