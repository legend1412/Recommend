import matplotlib.pyplot as plt
import numpy as np


class UserShow:
    def __init__(self):
        self.file_user = '../third/data/bookcrossings/BX-Users.csv'
        self.file_book = '../third/data/bookcrossings/BX-Books.csv'
        self.file_rate = '../third/data/bookcrossings/BX-Book-Ratings.csv'
        self.user_mess = self.load_user_data()
        self.book_mess = self.load_book_mess()
        self.user_book = self.load_user_book()

    # 加载用户信息数据集
    def load_user_data(self):
        user_mess = dict()
        for line in open(self.file_user, 'r', encoding='ISO-8859-1'):
            if line.startswith("\"User-ID\""):
                continue
            # 行的列值以";分隔，有三列，过滤掉不符的数据
            # 因为location字段中存在;所以这里以";分隔数据
            if len(line.split("\";")) != 3:
                continue
            # 去除数据中的空格
            line = line.strip().replace(" ", "")
            # 去掉数据中的"
            userid, addr, age = [one.replace("\"", "") for one in line.split("\";")]
            # 这里假设年龄的合理范围时(1,120)
            if age == "NULL" or int(age) not in range(1, 120):
                continue
            # 这里将年龄处理成年龄段0-9=>0,10-19=>1,······
            # age_split=int(int(age)/10)
            user_mess.setdefault(userid, {})
            user_mess[userid]["age"] = int(age)
            # location分为三级，以逗号分隔，对应国、州、市
            if len(addr.split(",")) < 3:
                continue
            city, province, country = addr.split(",")[-3:]
            user_mess[userid]["country"] = country
            user_mess[userid]["province"] = province
            user_mess[userid]["city"] = city
        return user_mess

    # 加载图书编号和名字的对应关系
    def load_book_mess(self):
        book_mess = dict()
        for line in open(self.file_book, 'r', encoding='ISO-8859-1'):
            if line.startswith("\"ISBN\""):
                continue
            isbn, book_name = line.replace("\"", "").split(";")[:2]
            book_mess[isbn] = book_name
        return book_mess

    # 获取每个用户评分大于5的图书信息
    def load_user_book(self):
        user_book = dict()
        for line in open(self.file_rate, 'r', encoding='ISO-8859-1'):
            if line.startswith("\"User-ID\""):
                continue
            uid, isbn, rate = line.strip().replace("\"", "").split(";")
            user_book.setdefault(uid, list())
            if int(rate) > 5:
                user_book[uid].append(isbn)
        return user_book

    # 展示相应属性的用户统计分布
    def show(self, x, y, x_label, y_label='数目'):
        plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
        plt.rcParams['font.size'] = 12  # 字体大小
        plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

        # x:对应坐标轴中的x轴
        # y:对应坐标轴中的y轴
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        # 保证x轴数据按照传入的x顺序排列
        plt.xticks(np.arange(len(x)), x, rotation=90)
        # 在坐标轴上显示x值对应的y值
        for a, b in zip(np.arange(len(x)), y):
            plt.text(a, b, b, rotation=45)
        plt.bar(np.arange(len(x)), y)
        plt.savefig("data/" + x_label + ".png")
        plt.show()

    # 不同年龄端的用户人数统计
    def diff_age(self):
        age_user = dict()
        for key in self.user_mess.keys():
            age_split = int(int(self.user_mess[key]["age"]) / 10)
            age_user.setdefault(age_split, 0)
            age_user[age_split] += 1
        age_user_sort = sorted(age_user.items(), key=lambda k: k[0], reverse=False)
        x = [x[0] for x in age_user_sort]
        y = [x[1] for x in age_user_sort]
        print(age_user_sort)
        self.show(x, y, x_label="用户年龄段")

    # 不同州下的用户分布 top 20
    def diff_pro(self):
        pro_user = dict()
        for key in self.user_mess.keys():
            if "province" in self.user_mess[key].keys() and self.user_mess[key]["province"] != "n/a":
                pro_user.setdefault(self.user_mess[key]["province"], 0)
                pro_user[self.user_mess[key]["province"]] += 1
        pro_user_sort = sorted(pro_user.items(), key=lambda k: k[1], reverse=True)[:20]
        x = [x[0] for x in pro_user_sort]
        y = [x[1] for x in pro_user_sort]
        print(pro_user_sort)
        self.show(x, y, x_label="用户所处州")

    # 获取不同年龄人群的评分图书分布
    # 这里选择0~30岁和大于50岁的用户进行分析
    def diff_user_age(self):
        age_books = dict()
        age_books.setdefault(1, dict())
        age_books.setdefault(2, dict())
        for key in self.user_mess.keys():
            if "country" not in self.user_mess[key].keys():
                continue
            if key not in self.user_book.keys():
                continue
            if int(self.user_mess[key]["age"]) in range(0, 30):
                for book in self.user_book[key]:
                    if book not in self.book_mess.keys():
                        continue
                    age_books[1].setdefault(book, 0)
                    age_books[1][book] += 1
            if int(self.user_mess[key]["age"]) in range(50, 120):
                for book in self.user_book[key]:
                    if book not in self.book_mess.keys():
                        continue
                    age_books[2].setdefault(book, 0)
                    age_books[2][book] += 1
        print("年龄在30岁以下的用户偏好的共性图书（top 10）")
        for one in sorted(age_books[1].items(), key=lambda k: k[1], reverse=True)[:10]:
            print(self.book_mess[one[0]])
        print("年龄在50岁以上的用户偏好的共性图书（top 10）")
        for one in sorted(age_books[2].items(), key=lambda k: k[1], reverse=True)[:10]:
            print(self.book_mess[one[0]])


if __name__ == '__main__':
    ushow = UserShow()
    # ushow.diff_age()
    # ushow.diff_pro()
    # ushow.diff_user_age()
