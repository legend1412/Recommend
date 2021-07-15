from sklearn import metrics

y_true = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
y_pred = [0, 0, 1, 1, 0, 1, 1, 0, 1, 1]

# MAE
print("MAE is {}".format((metrics.mean_absolute_error(y_true, y_pred))))
# MSE
print("MSE is {}".format((metrics.mean_squared_error(y_true, y_pred))))
# RMSE
print("RMSE is {}".format((metrics.mean_squared_error(y_true, y_pred) ** 0.5)))
