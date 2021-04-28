"""
计算歌手相似度
"""
import os
import json


class SingSim:
    def __init__(self):
        self.sing_tags = self.get_sing_tags()
        print(self.sing_tags)
        self.sim = self.get_sing_sim()
        print(self.sim)

    def get_sing_tags(self):
        sing_tags_dict = dict()
        for line in open('data/sing_tags.txt'):
            sing_id, tag = line.strip().split(',')
            sing_tags_dict.setdefault(sing_id, set())
            sing_tags_dict[sing_id].add(tag)

        return sing_tags_dict

    def get_sing_sim(self):
        sim = dict()
        if os.path.exists('data/sing_sim.json'):
            sim = json.load(open('data/sing_sim.json', 'r', encoding='utf-8'))
        else:
            i = 0
            for sing1 in self.sing_tags.keys():
                sim[sing1] = dict()
                for sing2 in self.sing_tags.keys():
                    if sing1 != sing2:
                        j_len = len(self.sing_tags[sing1] & self.sing_tags[sing2])
                        if j_len != 0:
                            result = j_len / len(self.sing_tags[sing1] | self.sing_tags[sing2])
                            if sim[sing1].__len__() < 20 or result > 0.8:
                                sim[sing1][sing2] = result
                            else:
                                # 找到最小值并删除
                                minkey = min(sim[sing1], key=sim[sing1].get)
                                del sim[sing1][minkey]
                i += 1
                print(str(i) + '\t' + sing1)
            json.dump(sim, open('data/sing_sim.json', 'w', encoding='utf-8'))
        print('歌曲相似度计算完毕!')
        return sim

    def transform(self):
        fw = open('data/sim_sim.txt', 'a', encoding='utf-8')
        for s1 in self.sim.keys():
            for s2 in self.sim[s1].keys():
                fw.write(s1 + ',' + s2 + ',' + str(self.sim[s1][s2]) + '\n')

        fw.close()
        print('Over!')


if __name__ == '__main__':
    sing = SingSim()
    sing.transform()
