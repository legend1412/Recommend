from numpy import *

# 计算相似度

ponit_a = (1, 1)
ponit_b = (2, 2)

set_j_a = (1, 2, 3)
set_j_b = (2, 3, 4, 5)


# 欧氏距离
def EuclideanDistance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# 曼哈顿距离
def ManhattanDistance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# 切比雪夫距离
def ChebyshevDistance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


# 马氏距离

# 夹角余弦距离
def CosineSimilarity(a, b):
    cos = (a[0] * b[0]) + (a[1] * b[1]) / (sqrt(a[0] ** 2 + b[0] ** 2)) * (sqrt(a[1] ** 2 + b[1] ** 2))
    return cos


# 杰卡德相似系数
def JaccardSimilarity(a, b):
    set_a = set(a)
    set_b = set(b)
    dis = float(len(set_a & set_b)) / len(set_a | set_b)
    return dis


# 杰卡德距离
def JaccardSimilarityDistance(a, b):
    set_a = set(a)
    set_b = set(b)
    dis = float(len((set_a | set_b) - (set_a & set_b))) / len(set_a | set_b)
    return dis


print(str(ponit_a) + "和" + str(ponit_b) + "的欧氏距离为:", EuclideanDistance(ponit_a, ponit_b))
print(str(ponit_a) + "和" + str(ponit_b) + "的曼哈顿距离为:", ManhattanDistance(ponit_a, ponit_b))
print(str(ponit_a) + "和" + str(ponit_b) + "的切比雪夫距离为:", ChebyshevDistance(ponit_a, ponit_b))
print(str(ponit_a) + "和" + str(ponit_b) + "的夹角余弦距离为:", CosineSimilarity(ponit_a, ponit_b))
print(str(set_j_a) + "和" + str(set_j_b) + "的杰卡德相似系数为:", JaccardSimilarity(set_j_a, set_j_b))
print(str(set_j_a) + "和" + str(set_j_b) + "的杰卡德距离为:", JaccardSimilarityDistance(set_j_a, set_j_b))
