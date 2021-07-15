from sklearn.model_selection import cross_validate
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier


# 使用CrossValidate演示交叉验证数据集的使用
def show_cross_validate():
    # 加载乳癌肿瘤数据集
    x, y = datasets.load_breast_cancer(return_X_y=True)
    # 定义KNN模型
    clf = KNeighborsClassifier()

    # 定义需要输出的评估指标
    scoring = ['accuracy', 'f1']
    # 打印每次交叉验证的准确率
    score = cross_validate(clf, x, y, scoring=scoring, cv=5, return_train_score=True)
    print(score)


show_cross_validate()
