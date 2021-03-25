import jieba
import math
import jieba.analyse


class TF_IDF:
    def __init__(self, file, stop_file):
        self.file = file
        self.stop_file = stop_file
        self.stop_words = self.get_stop_words()

    # 获取停用词列表
    def get_stop_words(self):
        swlist = list()
        for line in open(self.stop_file, 'r', encoding='utf-8').readlines():
            swlist.append(line.strip())
        print('加载停用词完成...')
        return swlist

    # 加载商品和其对应的短标题，使用jieba进行分词并去除停用词
    def load_data(self):
        dmap = dict()
        for line in open(self.file, 'r', encoding='utf-8').readlines():
            item_id, title = line.strip().split('\t')
            dmap.setdefault(item_id, [])
            for word in list(jieba.cut(str(title).replace(' ', ''), cut_all=False)):  # (1)
                if word not in self.stop_words:
                    dmap[item_id].append(word)
        print('加载商品和其对应的短标题，使用jieba进行分词并去除停用词...')
        return dmap

    # 获取一个短标题中的词频
    def get_freq_word(self, words):
        fred_word = dict()
        for word in words:
            fred_word.setdefault(word, 0)
            fred_word[word] += 1
        return fred_word

    # 统计单词在所有短标题中出现的次数
    def get_count_word_in_file(self, word, dmap):
        count = 0
        for key in dmap.keys():
            if word in dmap[key]:
                count += 1
        return count

    # 计算TF-IDF值
    def get_tf_idf(self, words, dmap):
        # 记录单词关键词和对应的tfidf值
        out_dic = dict()
        freq_word = self.get_freq_word(words)
        for word in words:
            # 计算tf值，即单个word在整句中出现的次数
            tf = freq_word[word] * 1.0 / len(words)
            # 计算idf值,即log(所有的标题数/(包含单个word的标题数+1))
            idf = math.log(len(dmap) / (self.get_count_word_in_file(word, dmap) + 1))
            tfidf = tf * idf
            out_dic[word] = tfidf
        # 给字典排序
        order_dic = sorted(out_dic.items(), key=lambda x: x[1], reverse=True)
        return order_dic


if __name__ == '__main__':
    # 数据集
    init_file = 'data/phone-title/id_title.txt'
    # 停用词文件
    init_stop_file = 'data/phone-title/stop_words.txt'
    tf_idf = TF_IDF(init_file, init_stop_file)
    # dmap中key是商品id，value为去除停用词后的词
    result_dmap = tf_idf.load_data()
    # print(result_dmap)
    for key_id in result_dmap.keys():
        tfidf_dic = tf_idf.get_tf_idf(result_dmap[key_id], result_dmap)
        print(key_id, tfidf_dic)
    words = "小米 红米6Pro 异形全面屏，后置1200万双摄，4000mAh超大电池"
    # withWeight用来设置打印权重
    print(jieba.analyse.extract_tags(words, topK=20, withWeight=True))
    print(jieba.analyse.textrank(words, topK=20, withWeight=True))
