import os, json
import matplotlib.pyplot as plt
import numpy as np


class Demo:
    def __init__(self, file_path):
        self.data_path = file_path
        self.users = ['1086360']
        self.item = ['80']

    # 查看self.user中用户个人兴趣度变化趋势
    def show_personla(self):
        user_item_rate = dict()
        # 首次计算会将计算结果保存在user_item_rate.json文件中，减少下次计算时的时间消耗
        if os.path.exists('data/user_item_rate.json'):
            user_item_rate = json.load(open('data/user_item_rate.json', 'r'))
            print('user_item_rate load OK！')
        else:
            # 遍历文件夹下的每一个文件
            for file in os.listdir(self.data_path):
                one_path = '{}/{}'.format(self.data_path, file)
                print(one_path)
                for line in open(one_path, 'r').readlines():
                    if not line.endswith(':') and line.strip().split(',')[0] in self.users:
                        user_id, rate, date = line.strip().split(',')
                        user_item_rate.setdefault(user_id, {})
                        new_date = ''.join(date.split('-')[:2])
                        user_item_rate[user_id].setdefault(new_date, []).append(int(rate))

            # 计算每个月份对应的平均分
            for uid in user_item_rate.keys():
                for date in user_item_rate[uid].keys():
                    user_item_rate[uid][date] = round(sum(user_item_rate[uid][date]) / len(user_item_rate[uid][date]),
                                                      2)
                    json.dump(user_item_rate, open('data/user_item_rate.json', 'w'))
                    print('user_item_rate message save OK !')
        return user_item_rate

    # 作图展示
    def show_picture(self, _dict, label):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        new_dict = sorted(_dict.items(), key=lambda k: k[0], reverse=False)  # false：升序
        x = [one[0] for one in new_dict]
        y = [one[1] for one in new_dict]
        plt.plot(x, y, marker='o', label=label)
        plt.xticks(np.arange(len(x), step=2), rotation=90)
        plt.xlabel(u'时间-单位/月')
        plt.ylabel(u'平均打分/月')
        plt.title(u'平均评分随时间的变化')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    init_file_path = 'data/netflix/training_set'
    demo = Demo(init_file_path)
    useritemrate = demo.show_personla()
    print(useritemrate)
    demo.show_picture(useritemrate[demo.users[0]], 'uid=1086960')
