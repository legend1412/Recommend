import pandas as pd
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 用来正常显示负号
plt.rcParams["axes.unicode_minus"] = False
# 图片输出目录
book_images_dir = "images/3-2/"


# 用户对图书的评分
def get_rating(file_path):
    print("文件路径:{}".format(file_path))
    ratings = pd.read_table(file_path, header=0, sep=";", encoding="ISO-8859-1")
    print("前5条数据为:\n{}".format(ratings.head(5)))
    print("总的数据记录数为:\n{}".format(ratings.count()))
    print("用户对图书的评分范围:<{},{}>".format(ratings['Book-Rating'].min(), ratings['Book-Rating'].max()))
    rate_ser = ratings["Book-Rating"].groupby(ratings["Book-Rating"]).count()
    plt.bar(rate_ser.keys(), rate_ser.values, fc="r", tick_label=rate_ser.keys())
    for x, y in zip(rate_ser.keys(), rate_ser.values):
        plt.text(x, y + 1, "%.0f" % y, ha="center", va="bottom", fontsize=9)
    plt.xlabel("用户评分")
    plt.ylabel("评分对应的人数")
    plt.title("每种评分下对应的人数统计图")
    plt.savefig(book_images_dir + "ratings.png")
    plt.show()


# 用户信息
def get_users(file_path):
    print("文件路径:{}".format(file_path))
    users = pd.read_table(file_path, header=0, sep=";", encoding="ISO-8859-1")
    print("前5条数据为:\n{}".format(users.head(5)))
    print("总的数据记录条数为:\n{}".format(users.count()))
    print("年龄的最大最小值:<{},{}>".format(users["Age"].min(), users["Age"].max()))


if __name__ == '__main__':
    ratings_file_path = "data/bookcrossings/BX-Book-Ratings.csv"
    get_rating(ratings_file_path)
    users_file_path = "data/bookcrossings/BX-Users.csv"
    get_users(users_file_path)
