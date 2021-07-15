import pandas as pd
import matplotlib.pyplot as plt

# 用来正常显示中文标签
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 用来正常显示负号
plt.rcParams["axes.unicode_minus"] = False
# 图片输出目录
events_images_dir = "images/3-5/"


# 用户行为数据查看
def get_user_event_mess(file_path):
    print("文件路径是:{}".format(file_path))
    events = pd.read_csv(file_path, header=0, encoding="utf-8")
    print("数据前5条:\n{}".format(events.head(5)))
    print("数据总条数为:\n{}".format(events.count()))
    event_ser = events["event"].groupby(events["event"]).count()
    print("Event的值有:\n{}".format(event_ser))

    plt.axes(aspect=1)
    plt.pie(x=event_ser.values, labels=event_ser.keys(), autopct="%3.1f %%")
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.savefig(events_images_dir + "events.png")
    plt.show()


if __name__ == '__main__':
    events_file_path = "data/retailrocket/events.csv"
    get_user_event_mess(events_file_path)
