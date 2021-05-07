# -*- coding:utf-8 -*-
"""
Desc:
    训练模型
"""
import random
import pandas
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import mean_squared_error

class Mode:
    def __init__(self):
        self.data = self._load_data()
        self.train_data,self.test_data = self._split_data()
        self.gbdt = self._train_model()

    #加载数据
    def _load_data(self):
        if os.path.exists('data/train.txt'):
            print('训练模型苏数据环境准备完毕，路径为：data/train.txt')