import math


class UserCF:
    def __init__(self):
        self.user_score_dict = self.init_user_score()
        # self.users_sim = self.user_similarity()
        # self.users_sim = self.user_similarity_better()
        self.users_sim = self.user_similarity_best()

    # 初始化用户评分数据
    def init_user_score(self):
        user_score_dict = {"A": {"a": 3.0, "b": 4.0, "c": 0.0, "d": 3.5, "e": 0.0},
                           "B": {"a": 4.0, "b": 0.0, "c": 4.5, "d": 0.0, "e": 3.5},
                           "C": {"a": 0.0, "b": 3.5, "c": 0.0, "d": 0.0, "e": 3.0},
                           "D": {"a": 0.0, "b": 4.0, "c": 0.0, "d": 3.5, "e": 3.0}}
        return user_score_dict

    # 计算用户之间的相似度，采用的是遍历每一个用户进行计算
    def user_similarity(self):
        w = dict()
        for u in self.user_score_dict.keys():
            w.setdefault(u, {})
            for v in self.user_score_dict.keys():
                if u == v:
                    continue
                u_set = set([key for key in self.user_score_dict[u].keys() if self.user_score_dict[u][key] > 0])
                v_set = set([key for key in self.user_score_dict[v].keys() if self.user_score_dict[v][key] > 0])
                w[u][v] = float(len(u_set & v_set)) / math.sqrt(len(u_set) * len(v_set))
        return w

    # 预测用户对item的评分
    def pre_user_item_score(self, user_a, item):
        score = 0.0
        for user in self.users_sim[user_a].keys():
            if user != user_a:
                score += self.users_sim[user_a][user] * self.user_score_dict[user][item]

        return score

    # 为用户推荐物品
    def recommend(self, user_a):
        # 计算user_a未评分item的可能评分
        user_item_score_dict = dict()
        for item in self.user_score_dict[user_a].keys():
            if self.user_score_dict[user_a][item] <= 0:
                user_item_score_dict[item] = self.pre_user_item_score(user_a, item)

        return user_item_score_dict

    # 计算用户之间的相似度，采用优化算法时间复杂度的方法
    def user_similarity_better(self):
        # 得到每个item被哪些user评价过
        item_users = dict()
        for u, items in self.user_score_dict.items():
            for i in items.keys():
                item_users.setdefault(i, set())
                if self.user_score_dict[u][i] > 0:
                    item_users[i].add(u)

        # 构建倒排表
        c = dict()
        n = dict()
        for i, users in item_users.items():
            for u in users:
                n.setdefault(u, 0)
                n[u] += 1
                c.setdefault(u, {})
                for v in users:
                    c[u].setdefault(v, 0)
                    if u == v:
                        continue
                    c[u][v] += 1

        print(c)
        print(n)
        # 构建相似度矩阵
        w = dict()
        for u, related_users in c.items():
            w.setdefault(u, {})
            for v, cuv in related_users.items():
                if u == v:
                    continue
                w[u].setdefault(v, 0.0)
                w[u][v] = cuv / math.sqrt(n[u] * n[v])
        return w

    # 计算用户之间的相似度，采用惩罚热门商品和优化算法复杂度的算法
    def user_similarity_best(self):
        # 得到每个item被哪些user评价过
        item_users = dict()
        for u, items in self.user_score_dict.items():
            for i in items.keys():
                item_users.setdefault(i, set())
                if self.user_score_dict[u][i] > 0:
                    item_users[i].add(u)

        # 构建倒排表
        c = dict()
        n = dict()
        for i, users in item_users.items():
            for u in users:
                n.setdefault(u, 0)
                n[u] += 1
                c.setdefault(u, {})
                for v in users:
                    c[u].setdefault(v, 0)
                    if u == v:
                        continue
                    c[u][v] += 1 / math.log(1 + len(users))

        print(c)
        print(n)
        # 构建相似度矩阵
        w = dict()
        for u, related_users in c.items():
            w.setdefault(u, {})
            for v, cuv in related_users.items():
                if u == v:
                    continue
                w[u].setdefault(v, 0.0)
                w[u][v] = cuv / math.sqrt(n[u] * n[v])
        return w


if __name__ == '__main__':
    ub = UserCF()
    print(ub.recommend("C"))
