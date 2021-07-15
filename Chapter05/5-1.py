from sklearn import preprocessing

# （1）对iphone5的离散型属性（颜色和内存）进行one-hot编码
onehot = preprocessing.OneHotEncoder()
# 训练数据，所有特征的可能组合
onehot.fit([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]])
print(onehot.transform([[0, 0]]).toarray())

# （2）对iphone5的离散型属性（颜色和内存）进行one-hot编码#
onehot.fit([[0, 0], [1, 1], [2, 2]])
print(onehot.transform([[0, 0]]).toarray())


# 对iphone 5的连续性属性（尺寸和价格）进行0-1归一化处理
def max_min_normalization(x, nmax, nmin):
    x = (x - nmin) / (nmax - nmin)
    return x


# 尺寸数组
sizes = [4, 4.7, 5.5]
# 价格数组
prices = [1358, 2788, 3656]
size_min, size_max = min(sizes), max(sizes)
price_min, price_max = min(prices), max(prices)
# 求iphone5，iphone6，iphone6sp的尺寸归一化
nor_price = []
for size in sizes:
    nor_price.append(round(max_min_normalization(size, size_max, size_min), 4))
print("尺寸归一化为:%s" % nor_price)

# 求iphone5，iphone6，iphone6sp的价格归一化
nor_price = []
for price in prices:
    nor_price.append(round(max_min_normalization(price, price_max, price_min), 4))
print("价格归一化为:%s" % nor_price)
