from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

y_true = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
y_pred = [0, 0, 1, 1, 0, 1, 1, 0, 1, 1]
# 混淆矩阵 行为label列为预测值
print("混淆矩阵")
print(confusion_matrix(y_true, y_pred))
# AUC
print("AUC is {}".format(metrics.roc_auc_score(y_true, y_pred)))
# 精确率
print("Precision is {}".format(metrics.precision_score(y_true, y_pred)))
# 召回率
print("Recall is {}".format(metrics.recall_score(y_true, y_pred)))
# F1值
print("F1 is {}".format(metrics.f1_score(y_true, y_pred)))
# 分类报告
print("分类报告")
print(classification_report(y_true, y_pred))
