"""
计算歌曲相似度
"""
import django
import json
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'MusicRec.settings'
django.setup()


class SongSim:
    def __init__(self):
        self.song_tags = self.get_song_tags()
        print(self.song_tags)
        self.sim = self.get_song_sim()
        print(self.sim)

    def get_song_tags(self):
        song_tags_dict = dict()
        for line in open('data/song_tag.txt', 'r', encoding='utf-8'):
            song_id, tag = line.strip().split(',')
            song_tags_dict.setdefault(song_id, set())
            song_tags_dict[song_id].add(tag)

        return song_tags_dict

    def get_song_sim(self):
        sim = dict()
        if os.path.exists('data/song_sim.json'):
            sim = json.load(open('data/song_sim.json', 'r', encoding='utf-8'))
        else:
            i = 0
            for song1 in self.song_tags.keys():
                sim[song1] = dict()
                for song2 in self.song_tags.keys():
                    if song1 != song2:
                        j_len = len(self.song_tags[song1] & self.song_tags[song2])
                        if j_len != 0:
                            result = j_len / len(self.song_tags[song1] | self.song_tags[song2])
                            if sim[song1].__len__() < 20 or result > 0.8:
                                sim[song1][song2] = result
                            else:
                                # 找到最小值，并删除
                                minkey = min(sim[song1], key=sim[song1].get)
                                del sim[song1][minkey]
                i += 1
                print(str(i) + '\t' + song1)
            json.dump(sim, open('data/song_sim.json', 'w', encoding='utf-8'))
        print('歌曲相似度计算完毕!')
        return sim

    def transform(self):
        fw = open('data/song_sim.txt', 'a', encoding='utf-8')
        for s1 in self.sim.keys():
            for s2 in self.sim[s1].keys():
                fw.write(s1 + ',' + s2 + ',' + str(self.sim[s1][s2]) + '\n')
        fw.close()
        print('Over!')


if __name__ == '__main__':
    song = SongSim()
    song.transform()
