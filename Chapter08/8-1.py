# -*-coding:utf-8-*-
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics
from sklearn.metrics import mean_squared_error


# 基于GBDT算法预估电信客户流失
class ChurnpPredWithGBDT:
    def __init__(self):
        self.file = 'data/telecom-churn/telecom-churn-prediction-data.csv'
        self.data = self.feature_transform
        self.train, self.test = self.split_data()

    # 空缺以0填充
    def isnone(self, value):
        if value == " " or value is None:
            return "0.0"
        else:
            return value

    # 特征转换
    @property
    def feature_transform(self):
        if not os.path.exists('data/new_churn.csv'):
            print('开始特征转换')
            # 定义特征转换字典
            feature_dict = {
                "gender": {"Male": "1", "Female": "0"},
                "Partner": {"Yes": "1", "No": "0"},
                "Dependents": {"Yes": "1", "No": "0"},
                "PhoneService": {"Yes": "1", "No": "0"},
                "MultipleLines": {"Yes": "1", "No": "0", "No phone service": "2"},
                "InternetService": {"DSL": "1", "Fiber optic": "2", "No": "0"},
                "OnlineSecurity": {"Yes": "1", "No": "0", "No internet service": "2"},
                "OnlineBackup": {"Yes": "1", "No": "0", "No internet service": "2"},
                "DeviceProtection": {"Yes": "1", "No": "0", "No internet service": "2"},
                "TechSupport": {"Yes": "1", "No": "0", "No internet service": "2"},
                "StreamingTV": {"Yes": "1", "No": "0", "No internet service": "2"},
                "StreamingMovies": {"Yes": "1", "No": "0", "No internet service": "2"},
                "Contract": {"Month-to-month": "0", "One year": "1", "Two year": "2"},
                "PaperlessBilling": {"Yes": "1", "No": "0"},
                "PaymentMethod": {"Electronic check": "0", "Mailed check": "1", "Bank transfer (automatic)": "2",
                                  "Credit card (automatic)": "3"},
                "Churn": {"Yes": "1", "No": "0"}
            }
            fw = open('data/new_churn.csv', 'w')
            fw.write(
                "customer_id, gender, senior_citizen, partner, dependents, tenure, phone_service, multiple_lines,"
                "internet_service, online_security, online_backup, device_protection, teach_support, streaming_tv,"
                "streaming_movies, contract, paperless_billing, payment_method, monthly_charges, total_charges,churn\n"
            )
            for line in open(self.file, 'r').readlines():
                if line.startswith('customerID'):
                    continue
                customer_id, gender, senior_citizen, partner, dependents, tenure, phone_service, multiple_lines, \
                    internet_service, online_security, online_backup, device_protection, teach_support, streaming_tv, \
                    streaming_movies, contract, paperless_billing, payment_method, monthly_charges, total_charges, \
                    churn = line.strip().split(",")
                _list = list()
                _list.append(customer_id)
                _list.append(self.isnone(feature_dict["gender"][gender]))
                _list.append(self.isnone(senior_citizen))
                _list.append(self.isnone(feature_dict["Partner"][partner]))
                _list.append(self.isnone(feature_dict["Dependents"][dependents]))
                _list.append(self.isnone(tenure))
                _list.append(self.isnone(feature_dict["PhoneService"][phone_service]))
                _list.append(self.isnone(feature_dict["MultipleLines"][multiple_lines]))
                _list.append(self.isnone(feature_dict["InternetService"][internet_service]))
                _list.append(self.isnone(feature_dict["OnlineSecurity"][online_security]))
                _list.append(self.isnone(feature_dict["OnlineBackup"][online_backup]))
                _list.append(self.isnone(feature_dict["DeviceProtection"][device_protection]))
                _list.append(self.isnone(feature_dict["TechSupport"][teach_support]))
                _list.append(self.isnone(feature_dict["StreamingTV"][streaming_tv]))
                _list.append(self.isnone(feature_dict["StreamingMovies"][streaming_movies]))
                _list.append(self.isnone(feature_dict["Contract"][contract]))
                _list.append(self.isnone(feature_dict["PaperlessBilling"][paperless_billing]))
                _list.append(self.isnone(feature_dict["PaymentMethod"][payment_method]))
                _list.append(self.isnone(monthly_charges))
                _list.append(self.isnone(total_charges))
                _list.append(self.isnone(feature_dict["Churn"][churn]))
                fw.write(",".join(_list))
                fw.write("\n")
            return pd.read_csv('data/new_churn.csv')
        else:
            return pd.read_csv('data/new_churn.csv')

    # 将数据集拆分为训练集和测试集
    def split_data(self):
        print("拆分数据集")
        train, test = train_test_split(self.data, test_size=0.1, random_state=40)
        return train, test

    # 调用sklearn进行模型训练
    def train_model(self):
        print('开始训练')
        lable = "churn"
        customer_id = "customer_id"
        x_columns = [x for x in self.train.columns if x not in [lable, customer_id]]
        x_train = self.train[x_columns]
        y_train = self.train[lable]
        gbdt = GradientBoostingClassifier(learning_rate=0.1, n_estimators=200, max_depth=5)
        gbdt.fit(x_train, y_train)
        return gbdt

    # 模型评估
    def evaluate(self, gbdt):
        print("模型评估")
        lable = "churn"
        customer_id = "customer_id"
        x_columns = [x for x in self.test.columns if x not in [lable, customer_id]]
        x_test = self.test[x_columns]
        y_test = self.test[lable]
        y_pred = gbdt.predict_proba(x_test)
        new_y_pred = list()
        for y in y_pred:
            # y[0]表示样本lable=0的概率，y[1]表示样本lable=1的概率
            new_y_pred.append(1 if y[1] > 0.5 else 0)
        mse = mean_squared_error(y_test, new_y_pred)
        print("GBDT-MSE:%.4f" % mse)
        accuracy = metrics.accuracy_score(y_test.values, new_y_pred)
        print("GBDT-Accuracy:%.4g" % accuracy)
        auc = metrics.roc_auc_score(y_test.values, new_y_pred)
        print("GBDT-AUC Score:%.4g" % auc)


if __name__ == '__main__':
    pred = ChurnpPredWithGBDT()
    gbdt_result = pred.train_model()
    pred.evaluate(gbdt_result)
