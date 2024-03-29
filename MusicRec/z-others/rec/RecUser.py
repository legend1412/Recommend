"""
Desc:
    基于用户的协同过滤算法，计算用户相似度
"""
import math


class RecUser:
    def __init__(self):
        self.playlist_mess_file = '../api/data/playlist_mess/pl_mess_all.txt'
        self.user_tags_count_dict = dict()  # 用户对标签的次数统计
        self.load_data()

        self.w = self.user_similarity_best()

    # 加载数据
    def load_data(self):
        for line in open(self.playlist_mess_file, 'r', encoding='utf-8'):
            pl_mess_list = line.strip().split(' |=| ')
            playlist_id, user_id, tags = (
                pl_mess_list[0],
                pl_mess_list[1],
                str(pl_mess_list[10]).replace('[', '').replace(']', '').replace("'", '').replace(' ', '')
            )
            # print(playlist_id,user_id,tags)
            self.user_tags_count_dict.setdefault(user_id, {})
            for tag in tags.split(','):
                self.user_tags_count_dict[user_id].setdefault(tag, 0)
                self.user_tags_count_dict[user_id][tag] += 1
        print('用户打标签统计完成!')

    # 计算用户之间的相似度
    def user_similarity_best(self):
        """
        计算用户之间的相似度，采用惩罚热门商品和优化算法复杂度的算法
        :return: dict
        """
        # 得到每个item被哪些user评价过
        tags_users = dict()
        for user_id, tags in self.user_tags_count_dict.items():
            for tag in tags.keys():
                tags_users.setdefault(tag, set())
                if self.user_tags_count_dict[user_id][tag] > 0:
                    tags_users[tag].add(user_id)

        # 构建倒排表
        c = dict()
        n = dict()
        for tags, users in tags_users.items():
            for u in users:
                n.setdefault(u, 0)
                n[u] += 1
                c.setdefault(u, {})
                for v in users:
                    c[u].setdefault(v, 0)
                    if u == v:
                        continue
                    c[u][v] += 1 / math.log(1 + len(users))

                    # 构建相似度矩阵
        w = dict()
        for u, relate_users in c.items():
            w.setdefault(u, {})
            for v, cuv in relate_users.items():
                if u == v:
                    continue
                w[u].setdefault(v, 0.0)
                w[u][v] = cuv / math.sqrt(n[u] * n[v])
        return w

    # 保存每个用户最相似的20个用户在文件中
    def write_to_file(self):
        fw = open('data/user_user_prefer.txt', 'a', encoding='utf-8')
        for user_id in self.w.keys():
            sorted_result = sorted(self.w[user_id].items(), key=lambda one: one[1], reverse=True)
            for one in sorted_result[:20]:
                fw.write(user_id + ',' + one[0] + ',' + str(one[1]) + '\n')
        fw.close()
        print('保存到文件完成!')


if __name__ == '__main__':
    rec_user = RecUser()
    rec_user.write_to_file()
