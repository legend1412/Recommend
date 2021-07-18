"""
Desc:
    计算用户相似度
"""
import django
import json
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MusicRec.settings")
django.setup()

from user.models import UserTag


class UserSim:
    def __init__(self):
        self.user_tags = self.get_user_tags()
        print(self.user_tags)
        self.sim = self.get_user_sim()
        print(self.sim)

    def get_user_tags(self):
        user_tags_dict = dict()
        for one in UserTag.objects.all():
            user_tags_dict.setdefault(one.user_id, set())
            user_tags_dict[one.user_id].add(one.tag)
        return user_tags_dict

    # 计算用户相似度，由于全量用户存储数据量大且无用，所以这里只存储了每个用户的相近20个用户，并且要求相似度大于0.8
    def get_user_sim(self):
        sim = dict()
        if os.path.exists('data/user_sim.json'):
            sim = json.load(open('data/user_sim.json', 'r', encoding='utf-8'))
        else:
            i = 0
            for use1 in self.user_tags.keys():
                sim[use1] = dict()
                for use2 in self.user_tags.keys():
                    if use1 != use2:
                        j_len = len(self.user_tags[use1] & self.user_tags[use2])
                        if j_len != 0:
                            result = j_len / len(self.user_tags[use1] | self.user_tags[use2])
                            if sim[use1].__len__() < 20 or result > 0.8:
                                sim[use1][use2] = result
                            else:
                                # 找到最小值并删除
                                minkey = min(sim[use1], key=sim[use1].get)
                                del sim[use1][minkey]
                i += 1
                print(str(i) + '\t' + use1)
            json.dump(sim, open('data/user_sim.json', 'w', encoding='utf-8'))
        print('用户相似度计算完毕')
        return sim

    # 将计算出的相似度转成导入mysql的格式
    def transform(self):
        fw = open('data/user_sim.txt', 'a', encoding='utf-8')
        for u1 in self.sim.keys():
            for u2 in self.sim[u1].keys():
                fw.write(u1 + "," + u2 + "," + str(self.sim[u1][u2]) + '\n')

        fw.close()
        print('Over!')


if __name__ == '__main__':
    user = UserSim()
    user.transform()
