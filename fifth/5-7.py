# -*- coding:utf-8 -*-
import random
import math
import os
import json


class ItemCFRec:
    def __init__(self, datafile, ratio):
        # 原始数据路径文件
        self.datafile = datafile

    # 加载评分数据到data
    def load_date(self):
        print("加载数据...")

