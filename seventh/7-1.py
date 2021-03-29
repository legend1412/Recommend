import os
import json
import matplotlib.pyplot as plt
import numpy as np


class Demo:
    def __init__(self, file_path):
        self.data_path = file_path
        self.users = ['1086360']
        self.items = ['80']

    # 查看self.users中用户个人兴趣度变化趋势
    def show_personla(self):
        user_rate = dict()
        # 首次计算会将计算结果保存在user_rate.json文件中，减少下次计算时的时间消耗
        if os.path.exists('data/user_rate.json'):
            user_rate = json.load(open('data/user_rate.json', 'r'))
            print('user_rate load OK！')
        else:
            # 遍历文件夹下的每一个文件
            for file in os.listdir(self.data_path):
                one_path = '{}/{}'.format(self.data_path, file)
                print(one_path)
                for line in open(one_path, 'r').readlines():
                    if not line.endswith(':') and line.strip().split(',')[0] in self.users:
                        user_id, rate, date = line.strip().split(',')
                        user_rate.setdefault(user_id, {})
                        new_date = ''.join(date.split('-')[:2])
                        user_rate[user_id].setdefault(new_date, []).append(int(rate))

            # 计算每个月份对应的平均分
            for uid in user_rate.keys():
                for date in user_rate[uid].keys():
                    user_rate[uid][date] = round(sum(user_rate[uid][date]) / len(user_rate[uid][date]),
                                                 2)
                    json.dump(user_rate, open('data/user_rate.json', 'w'))
                    print('user_rate message save OK !')
        return user_rate

    # 查看self.items中物品流行度趋势
    def show_item(self):
        item_rate = dict()
        # 首次计算会将结果保存在item_rate.json文件中，减少下次计算时的时间消耗
        if os.path.exists('data/item_rate.json'):
            item_rate = json.load(open('data/item_rate.json', 'r'))
            print('item_rate load ok!')
        else:
            # 遍历文件夹下的每一个文件
            for file in os.listdir(self.data_path):
                one_path = "{}/{}".format(self.data_path, file)
                print(one_path)
                flag = False
                item_id = None
                for line in open(one_path, 'r').readlines():
                    if line.strip().endswith(":") and line.strip().split(":")[0] in self.items:
                        item_id = line.split(":")[0]
                        flag = True
                        continue
                    elif line.strip().endswith(":"):
                        flag = False
                        continue
                    if flag:
                        _, rate, date = line.strip().split(",")
                        item_rate.setdefault(item_id, {})
                        new_date = "".join(date.split("-")[:2])
                        item_rate[item_id].setdefault(new_date, []).append(int(rate))
            # 计算每个月份对应的平均分
            for item_id in item_rate.keys():
                for date in item_rate[item_id].keys():
                    item_rate[item_id][date] = round(sum(item_rate[item_id][date]) / len(item_rate[item_id][date]),
                                                     2)
            json.dump(item_rate, open('data/item_rate.json', 'w'))
            print('item_rate message save OK !')
        return item_rate

    # 作图展示
    def show_picture(self, _dict, label, title, save_file):
        print(self.data_path)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        new_dict = sorted(_dict.items(), key=lambda k: k[0], reverse=False)  # false：升序
        x = [one[0] for one in new_dict]
        y = [one[1] for one in new_dict]
        plt.plot(x, y, marker='o', label=label)
        plt.xticks(np.arange(len(x), step=2), rotation=90)
        plt.xlabel(u'时间-单位/月')
        plt.ylabel(u'平均打分/月')
        plt.title(u'{}'.format(title))
        plt.savefig("data/{}".format(save_file + ".png"))
        plt.legend()
        plt.show()


if __name__ == '__main__':
    init_file_path = 'data/netflix/training_set'
    demo = Demo(init_file_path)
    ur = demo.show_personla()
    print(ur)
    demo.show_picture(ur[demo.users[0]], 'user_id=1086960', '个人兴趣度平均评分随时间的变化', 'user_rate')
    ir = demo.show_item()
    print(ir)
    demo.show_picture(ir[demo.items[0]], 'item_id=2', '物品流程度平均评分随时间的变化', 'item_rate')
