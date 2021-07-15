# -*- coding:utf-8 -*-
"""
代码11-4 获取NewsRec/settings.py中配置的前端展示的标签下的新闻
"""
import pymysql
from NewsRec.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWD, DB_NAME, ALLOW_TAGS
import os


class NewsTagsCor:
    def __init__(self, file_path):
        self.kw_path = file_path
        self.db = self.connect()
        self.cursor = self.db.cursor()
        self.result = self.get_news_tags()

    # 连接mysql数据库
    def connect(self):
        db = pymysql.Connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_NAME, port=DB_PORT, charset='utf8')
        return db

    # 获取每个标签下对应的文章
    def get_news_tags(self):
        result = dict()
        for file in os.listdir(self.kw_path):
            path = self.kw_path + file
            for line in open(path, encoding='utf-8').readlines():
                try:
                    newid, tags = line.strip().split("\t")
                except Exception as ex:
                    print("%s 下无对应标签" % newid)
                    print("异常:"+str(ex))
                for tag in tags.split(","):
                    if tag in ALLOW_TAGS:
                        sql = "select new_hot from newhot where new_id=%s" % newid
                        self.cursor.execute(sql)
                        hot_value = self.cursor.fetchone()
                        result.setdefault(tag, {})
                        result[tag][newid] = hot_value[0]
        return result

    # 对每个标签下的新闻进行排序，并写入mysql
    def write_to_mysql(self):
        for tag in self.result.keys():
            for newid in self.result[tag].keys():
                sql_w = "insert into newtag(new_tag,new_id,new_hot) values('%s','%s','%s')" % (
                tag, newid, self.result[tag][newid])
                try:
                    self.cursor.execute(sql_w)
                    self.db.commit()
                except Exception as ex:
                    print("异常:" + str(ex))
                    print("rollback", tag, newid, self.result[tag][newid])
                    self.db.rollback()


if __name__ == '__main__':
    print("开始寻找对应关键词下的新闻...")
    keyword_path = "../data/keywords/"
    ntc = NewsTagsCor(file_path=keyword_path)
    ntc.write_to_mysql()
    print("关键词下的新闻数据写入完毕，表为:newsrec.newtag")
