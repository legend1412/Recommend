# -*- coding:utf-8 -*-
"""
Desc:
    数据预处理
"""
import pandas
import re
import random

class Prepare:
    def __init__(self):
        self.file = 'data/豆瓣图书.xlsx'
        self.data = self.load_data()
        self.trans_data=self.transform()

    def load_data(self):
        data = pandas.read_excel(self.file,sheet_name='Sheet1')
        return data
    def transform(self):
        trans_data = dict()
        for row in self.data.iterrows():
            print(row[1]['ID'])
            trans_data[row[1]['ID']]=list()
            trans_data[row[1]['ID']].append(row[1]['标题'].replace(',','&'))
            