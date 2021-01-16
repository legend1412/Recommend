import pandas as pd
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 用来正常显示负号
plt.rcParams["axes.unicode_minus"] = False
# 图片输出目录
movies_images_dir = "images/3-1/"


# 用户评分记录统计

def get_rating(file_path):
    rates = pd.read_table(file_path, header=None, sep="::", names=["userid", "movieid", "rate", "timestamp"])
    print("userid的范围为:<{},{}>".format(min(rates["userid"]), max(rates["userid"])))
    print("movieid的范围为:<{},{}>".format(min(rates["movieid"]), max(rates["movieid"])))
    print("评分值的范围为:<{},{}>".format(min(rates["rate"]), max(rates["rate"])))
    print("数据总条数为:\n{}".format(rates.count()))
    print("数据前5条记录为:\n{}".format(rates.head(5)))
    df = rates["userid"].groupby(rates['userid'])
    print("用户评分记录最少条数为:{}".format(df.count().min()))
    scores = rates["rate"].groupby(rates["rate"]).count()
    # 图上添加数字
    for x, y in zip(scores.keys(), scores.values):
        plt.text(x, y + 2, "%.0f" % y, ha="center", va="bottom", fontsize=12)
    plt.bar(scores.keys(), scores.values, fc="r", tick_label=scores.keys())
    plt.xlabel("评分分数")
    plt.ylabel("对应的人数")
    plt.title("评分分数对应人数统计")
    plt.savefig(movies_images_dir + "ratings.png")
    plt.show()


# 电影的信息统计
def get_movies(file_path):
    movies = pd.read_table(file_path, header=None, sep="::", names=["movieid", "title", "genres"])
    print("movieid的范围为:<{},{}>".format(min(movies["movieid"]), max(movies["movieid"])))
    print("数据总条数为:\n{}".format(movies.count()))
    movies_dict = dict()
    for line in movies["genres"].values:
        for one in line.split("|"):
            movies_dict.setdefault(one, 0)
            movies_dict[one] += 1
    print("电影类型总数为:{}".format(len(movies_dict)))
    print("电影类型分别为:{}".format(movies_dict.keys()))
    print(movies_dict)

    newmd = sorted(movies_dict.items(), key=lambda x: x[1], reverse=True)
    # 设置标签
    labels = [newmd[i][0] for i in range(len(newmd))]
    values = [newmd[i][1] for i in range(len(newmd))]
    # 与labels对应，数值越大离中心区越远
    explode = [x * 0.01 for x in range(len(newmd))]
    # 设置X轴，Y轴比例
    plt.axes(aspect=1)
    # labeldistance表示标签离中心距离，pctdistance表示百分百数据离中心区距离
    # autopct 表示百分比模式，shadow表示阴影
    plt.pie(x=values, labels=labels, explode=explode, autopct="%3.1f %%",
            shadow=False, labeldistance=1.1, startangle=0,
            pctdistance=0.8, center=(-1, 0))
    # 控制位置：在bbox_to_anchor数组中，前者控制左右移动，后者控制上下移动
    # ncol 控制图例所列的列数，默认为1
    plt.legend(loc=7, bbox_to_anchor=(1.3, 1.0), ncol=3, fancybox=True, shadow=True, fontsize=6)
    plt.title("电影类型分布")
    plt.savefig(movies_images_dir + "movies.png")
    plt.show()


# 用户信息查看
def get_users(file_path):
    users = pd.read_table(file_path, header=None, sep="::",
                          names=["userid", "gender", "age", "occupation", "zip-code"])
    print("userid的范围为:<{},{}>".format(min(users["userid"]), max(users["userid"])))
    print("数据总条数为:\n{}".format(users.count()))

    # 用户性别分布
    users_gender = users["gender"].groupby(users["gender"]).count()
    print(users_gender)

    plt.axes(aspect=1)
    plt.pie(x=users_gender.values, labels=users_gender.keys(),
            autopct="%3.1f %%")
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.title("用户性别分布")
    plt.savefig(movies_images_dir + "user_gender.png")
    plt.show()

    users_age = users["age"].groupby(users["age"]).count()
    print(users_age)

    # 用户年龄分布
    plt.plot(users_age.keys(), users_age.values, label="用户年龄信息展示", linewidth=3, color='r',
             marker='o', markerfacecolor="blue", markersize=12)
    # 图上添加数字
    for x, y in zip(users_age.keys(), users_age.values):
        plt.text(x, y + 0, "%.0f" % y, ha="center", va="bottom", fontsize=12)
    plt.xlabel("用户年龄")
    plt.ylabel("年龄段对应的人数")
    plt.title("用户年龄段的人数统计")
    plt.savefig(movies_images_dir + "user_age.png")
    plt.show()


if __name__ == '__main__':
    ratings_file_path = "data/ml-1m/ratings.dat"
    get_rating(ratings_file_path)
    movies_file_path = "data/ml-1m/movies.dat"
    get_movies(movies_file_path)
    users_file_path = "data/ml-1m/users.dat"
    get_users(users_file_path)
