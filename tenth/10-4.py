import numpy as np
from sklearn import metrics


# 计算AUC
def calc_auc():
    y = np.array([1, 1, 2, 2])
    pred = np.array([0.1, 0.4, 0.35, 0.8])
    # pos_label参数意义：这个pos_label的值被认为i是阳性的，而其他值被认为是阴性的，pred给的是阳性的概率
    fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=2)
    print(metrics.auc(fpr, tpr))
    y1 = np.array([1, 0, 1, 0, 0, 0])
    pred1 = np.array([0.9, 0.7, 0.8, 0.6, 0.5, 0.4])
    fpr1, tpr1, thresholds1 = metrics.roc_curve(y1, pred1, pos_label=1)
    print(metrics.auc(fpr1, tpr1))


calc_auc()
