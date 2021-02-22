import operator
import math


class DecisionTree:
    def __init__(self):
        pass

    # 加载数据集
    def loaddata(self):
        # 天气：晴（2），阴（1），雨（0）
        # 温度：炎热（2），适中（1），寒冷（0）
        # 湿度：高（1），正常（0）
        # 风速：强（1），弱（0）
        # 举办活动（yes），不举办活动（no）
        init_data = [[2, 2, 1, 0, "yes"], [2, 2, 1, 1, "no"], [1, 2, 1, 0, "yes"], [0, 0, 0, 0, "yes"],
                     [0, 0, 0, 1, "no"],
                     [1, 0, 0, 1, "yes"], [2, 1, 1, 0, "no"], [2, 0, 0, 0, "yes"], [0, 1, 0, 0, "yes"],
                     [2, 1, 0, 1, "yes"],
                     [1, 2, 0, 0, "no"], [0, 1, 1, 1, "no"]]
        # 分类属性
        features = ["天气", "温度", "湿度", "风速"]
        return init_data, features

    # 计算给定数据集的香农熵，即不使用任何属性进行拆分
    def shannonent(self, data):
        numdata = len(data)
        labelcounts = {}
        for feature in data:
            one_label = feature[-1]  # 获得标签
            # 如果标签不在新定义的字典里，则创建该标签值
            labelcounts.setdefault(one_label, 0)
            # 该类标签下含有的数据个数
            labelcounts[one_label] += 1
        shannon_ent = 0.0
        for key in labelcounts:
            # 同类标签出现的概率
            prob = float(labelcounts[key]) / numdata
            # 以2为底，求对数
            shannon_ent -= prob * math.log2(prob)
        return shannon_ent

    # 选择最好的划分属性标签：针对原始数据集，遍历每个属性，计算根据每个属性划分数据集后对应的香农熵Ei，然后计算每个属性对应的信息增益Gi，最后
    # 根据信息增益最大原则返回其对应的属性标签

    # 划分数据集，三个参数为带划分的数据集，划分数据集的特征，特征的返回值
    def splitdata(self, data, axis, value):
        retdata = []
        for feature in data:
            if feature[axis] == value:
                # 将拥有相同特征的数据集抽取出来
                reduced_feature = feature[:axis]
                reduced_feature.extend(feature[axis + 1:])
                retdata.append(reduced_feature)
        return retdata  # 返回一个列表

    # 选择最好的数据集划分方式
    def choose_best_feature_split(self, data):
        num_feature = len(data[0]) - 1
        base_entropy = self.shannonent(data)
        best_info_gain = 0.0
        best_feature = -1
        for i in range(num_feature):
            # 获取第i个特征所有的可能取值
            feature_list = [result[i] for result in data]
            # 从列表中创建集合，得到不重复的所有可能取值
            unique_feature_list = set(feature_list)
            new_entropy = 0.0
            for value in unique_feature_list:
                # 以i为数据集特征，value为返回值，划分数据集
                split_dataset = self.splitdata(data, i, value)
                # 数据集特征为i的数据集所占比例
                prob = len(split_dataset) / float(len(data))
                # 计算每种数据集的信息熵
                new_entropy += prob * self.shannonent(split_dataset)
            info_gain = base_entropy - new_entropy
            # 计算最好的信息增益，增益越大说明所占决策权越大
            if info_gain > best_info_gain:
                best_info_gain = info_gain
                best_feature = i
        return best_feature

    # 遍历整个数据集，递归构建决策树
    def majoritycnt(self, labelslist):
        labels_count = {}
        for vote in labelslist:
            if vote not in labels_count.keys():
                labels_count[vote] = 0
            labels_count[vote] += 1
        sorted_labels_count = sorted(labels_count.iteritems(), key=operator.itemgetter(1), reverse=True)  # 排序，True为升序
        print(sorted_labels_count)
        return sorted_labels_count[0][0]

    # 创建决策树
    def create_tree(self, data, features):
        # 使用“=”产生的新变量，实际熵两者是一样的，避免后面del()函数对原变量值产生影响
        features = list(features)
        labels_list = [line[-1] for line in data]
        # 类别完全相同则停止划分
        if labels_list.count(labels_list[0]) == len(labels_list):
            return labels_list[0]
        # 遍历完所有特征值时返回出现次数最多的
        if len(data[0]) == 1:
            return self.majoritycnt(labels_list)
        # 选择最好的数据集划分方式
        best_feature = self.choose_best_feature_split(data)
        best_feature_lable = features[best_feature]  # 得到对应的标签值
        my_tree = {best_feature_lable: {}}
        # 清空features[best_feature],在下一次使用时清零
        del (features[best_feature])
        feature_values = [example[best_feature] for example in data]
        unique_feature_values = set(feature_values)
        for value in unique_feature_values:
            sub_features = features[:]
            # 递归调用创建决策数函数
            my_tree[best_feature_lable][value] = self.create_tree(self.splitdata(data, best_feature, value),
                                                                  sub_features)
        return my_tree

    # 预测新数据特征装下是否举办活动
    def predict(self, tree, features, x):
        class_label = ""
        for key1 in tree.keys():
            second_dict = tree[key1]
            # key1是根节点代表的特征，feat_index是取根节点特征在特征列表中的索引，方便后面对输入样本逐变量判断
            feat_index = features.index(key1)
            # 这里每一个key值对应的是根节点特征的不同取值
            for key2 in second_dict.keys():
                # 找到输入样本在决策树中由根节点往下走的路径
                if x[feat_index] == key2:
                    # 该分支产生了一个内部节点，则在决策中继续用同样的操作查找路径
                    if type(second_dict[key2]).__name__ == "dict":
                        class_label = self.predict(second_dict[key2], features, x)
                    # 该分支产生的是叶节点，直接取值就得到类别
                    else:
                        class_label = second_dict[key2]
        return class_label


if __name__ == '__main__':
    dtree = DecisionTree()
    initdata, initfeatures = dtree.loaddata()
    mytree = dtree.create_tree(initdata, initfeatures)
    print(mytree)
    label = dtree.predict(mytree, initfeatures, [1, 1, 1, 0])
    print("新数据[1,1,1,0]对应的是否要举办活动为:{}".format(label))
