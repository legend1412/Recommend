import pandas as pd
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 用来正常显示负号
plt.rcParams["axes.unicode_minus"] = False
# 图片输出目录
fs_images_dir = "images/3-4/"


# 评分记录数据查看
def get_ratings_mess(file_path):
    print("文件路径:{}".format(file_path))
    # drop 删除函数，这里删除第0行
    events = pd.read_table(file_path, header=0, sep="|").drop(0)
    print("原始events的key为:\n{}".format(events.keys()))
    # print(events.columns.values)
    print("数据的前5条为:\n{}".format(events.head(5)))
    #  去空格
    events.columns = events.rename(columns=lambda x: x.strip()).keys()
    events = events.replace(' ', '')
    print("去除标题空格后,events的key为:\n{}".format(events.keys()))
    print("去掉空格后,数据的前5条为:\n{}".format(events.head(5)))
    # 因为原始数据的原因，按照|分割后，字段前后多了空格
    rate_ser = events["rating"].groupby(events["rating"]).count()
    print("events的值有:\n{}".format(rate_ser))

    plt.axes(aspect=1)
    plt.pie(x=rate_ser.values, labels=rate_ser.keys(), autopct="%3.1f %%")
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.title("评分记录信息")
    plt.savefig(fs_images_dir + "ratings.png")
    plt.show()


if __name__ == '__main__':
    fs_file_path = "data/foursquare-2013/ratings.dat"
    get_ratings_mess(fs_file_path)
