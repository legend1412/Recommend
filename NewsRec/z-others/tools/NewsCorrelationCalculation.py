# -*- coding:utf-8 -*-
"""
代码11-3 每个类型下新闻的相似度计算
"""
import os
from NewsRec.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWD, DB_NAME
import pymysql


class Correlation:
    def __init__(self, file):
        self.db = self.connect()
        self.cursor = self.db.cursor()

        self.file = file
        self.news_tags = self.load_data()
        self.news_cor_list = self.get_correlation()

    # 连接mysql数据库
    def connect(self):
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT, charset='utf8')
        return db

    # 加载数据
    def load_data(self):
        print('开始加载文件数据:%s' % self.file)
        news_tags = dict()
        for line in open(self.file, 'r', encoding='utf-8').readlines():
            try:
                newid, newtags = line.strip().split('\t')
                news_tags[newid] = newtags
            except Exception as ex:
                print('读取分词数据过程中出现错误，错误行为：{}'.format(line))
                print("异常:" + str(ex))
                pass
        return news_tags

    # 计算相关度
    def get_correlation(self):
        news_cor_list = list()
        for newid1 in self.news_tags.keys():
            id1_tags = set(self.news_tags[newid1].split(","))
            for newid2 in self.news_tags.keys():
                id2_tags = set(self.news_tags[newid2].split(","))
                if newid1 != newid2:
                    # print(newid1 + "\t" + newid2 + "\t" + str(id1_tags & id2_tags))
                    cor = (len(id1_tags & id2_tags)) / len(id1_tags | id2_tags)
                    if cor > 0.0:
                        news_cor_list.append([newid1, newid2, format(cor, ".2f")])

        return news_cor_list

    # 将相似度数据写入数据库
    def wirte_to_mysql(self):
        for row in self.news_cor_list:
            sql_w = "insert into newsim(new_id_base,new_id_sim,new_correlation) values(%s,%s,%s)" % (row[0], row[1], row[2])
            try:
                self.cursor.execute(sql_w)
                self.db.commit()
            except Exception as ex:
                print("rollback", row)
                print("异常:" + str(ex))
                self.db.rollback()
        print("相似度数据写入数据库:newsrec.newsim")


if __name__ == '__main__':
    # 原始数据文件路径
    original_data_path = "../data/keywords/"
    files = os.listdir(original_data_path)
    for file in files:
        print("开始计算文件%s下的新闻相关度。" % file)
        cor = Correlation(original_data_path + file)
        cor.wirte_to_mysql()
    print("相关度计算完毕")
