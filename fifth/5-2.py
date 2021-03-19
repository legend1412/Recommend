import pandas as pd
import json


class DataProcessing:
    def __init__(self):
        pass

    def process(self):
        print('开始转换用户数据(users.dat)...')
        self.process_user_data()
        print('开始转换电影数据(movies.data)...')
        self.process_movies_data()
        print('开始转换用户对电影的评分数据(ratings.dat)...')
        self.process_ratings_data()
        print('Over!')

    def process_user_data(self, file='data/ml-1m/users.dat'):
        fp = pd.read_table(file, sep='::', engine='python', names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'])
        fp.to_csv('data/users.csv', index=False)

    def process_movies_data(self, file='data/ml-1m/movies.dat'):
        fp = pd.read_table(file, sep='::', engine='python', names=['MovieID', 'Title', 'Genres'])
        fp.to_csv('data/movies.csv', index=False)

    def process_ratings_data(self, file='data/ml-1m/ratings.dat'):
        fp = pd.read_table(file, sep='::', engine='python', names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
        fp.to_csv('data/ratings.csv', index=False)

    # 电影的特征信息矩阵
    def prepare_item_profile(self, file='data/movies.csv'):
        items = pd.read_csv(file)
        item_ids = set(items['MovieID'].values)
        self.item_dict = {}
        genres_all = list()
        # 将每个电影的类型放在item_dict中
        for item in item_ids:
            genres = items[items['MovieID'] == item]['Genres'].values[0].split('|')
            self.item_dict.setdefault(item, []).extend(genres)
            genres_all.extend(genres)
        self.genres_all = set(genres_all)
        # 将每个电影的特征信息矩阵存放在self.item_matrix中
        # 保存dict时，key只能为str，所以这里对item id做str()转换
        self.item_matrix = {}
        for item in self.item_dict.keys():
            self.item_matrix[str(item)] = [0] * len(set(self.genres_all))
            for genre in self.item_dict[item]:
                index = list(set(genres_all)).index(genre)
                self.item_matrix[str(item)][index] = 1
        json.dump(self.item_matrix, open('data/item_profile.json', 'w'))
        print('item信息计算完成,保存路径为:{}'.format('data/item_profile.json'))

    # 计算用户的偏好矩阵
    def prepare_user_profile(self, file='data/ratings.csv'):
        users = pd.read_csv(file)
        user_ids = set(users['UserID'].values)
        # 将users信息转换成dict
        users_rating_dict = {}
        for user in user_ids:
            users_rating_dict.setdefault(str(user), {})
        with open(file, 'r') as fr:
            for line in fr.readlines():
                if not line.startswith('UserID'):
                    (user, item, rate) = line.split(',')[:3]
                    users_rating_dict[user][item] = int(rate)

        # 获取用户对每个类型下的哪些电影进行了评分
        self.user_matrix = {}
        # 遍历每个用户
        for user in users_rating_dict.keys():
            print('user is {}'.format(user))
            score_list = users_rating_dict[user].values()
            # 用户的平均打分
            avg = sum(score_list) / len(score_list)
            self.user_matrix[user] = []
            # 遍历每个类型(保证item_profile和user_profile信息矩阵中每列表示的类型一致)
            for genre in self.genres_all:
                score_all = 0.0
                score_len = 0
                # 遍历每个item
                for item in users_rating_dict[user].keys():
                    # 判断类型是否在用户评分过的电影里
                    if genre in self.item_dict[int(item)]:
                        score_all += (users_rating_dict[user][item] - avg)
                        score_len += 1
                if score_len == 0:
                    self.user_matrix[user].append(0.0)
                else:
                    self.user_matrix[user].append(score_all / score_len)
        json.dump(self.user_matrix, open('data/user_profile.json', 'w'))
        print('user信息计算完成,保存路径为:{}'.format('data/user_profile.json'))


if __name__ == '__main__':
    dp = DataProcessing()
    dp.process()
    dp.prepare_item_profile()
    dp.prepare_user_profile()
