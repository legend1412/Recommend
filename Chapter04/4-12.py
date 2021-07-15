class Apriori:
    def __init__(self, min_support, min_confidence):
        # 最小支持度
        self.min_support = min_support
        # 最小置信度
        self.min_confidenct = min_confidence
        self.data = self.load_data()

    # 加载数据集
    def load_data(self):
        return [[1, 5], [2, 3, 4], [2, 3, 4, 5], [2, 3]]

    # 生成项集C1，不包含项集中每个元素出现的次数
    def create_c1(self, data):
        c1 = list()  # c1为大小为1的项的集合
        for items in data:
            for item in items:
                if [item] not in c1:
                    c1.append([item])

        # map函数表示遍历c1中的每一个元素执行froenset
        # frozenset表示‘冰冻’的集合，即不可改变
        return list(map(frozenset, sorted(c1)))

    # 该函数用于从候选项集Ck生成Lk，Lk表示满足最低支持度的元素集合
    def scan_support_data(self, ck):
        # Data表示数据列表的列表[set([]),set([]),set([]),set([])]
        data = list(map(set, self.data))
        ck_count = {}
        # 统计ck项集中的每个元素出现的次数
        for items in data:
            for one in ck:
                # issubset:表示如果one中的每一个元素都在items中则返回true
                if one.issubset(items):
                    ck_count.setdefault(one, 0)
                    ck_count[one] += 1
        num_items = len(list(data))  # 数据条数
        lk = []  # 初始化符合支持度的项集
        support_data = {}  # 初始化所有符合条件的项集及对应的支持度
        for key in ck_count:
            # 计算每个项集的支持度, 如果满足条件则把该项集加入到lk列表中
            support = ck_count[key] * 1.0 / num_items
            if support >= self.min_support:
                lk.insert(0, key)
            # 构建支持的项集的字典
            support_data[key] = support
        return lk, support_data

    # generste_new_ck的输入参数为频繁项集列表lk与项集元素个数k，输出为ck
    def generate_new_ck(self, lk, k):
        next_lk = []
        len_lk = len(lk)
        # 若两个项集的长度为k-1，则必须前k-2项相同才可连接，即求并集，所有[:k-2]的实际作用为取列表的前k-1各元素
        for i in range(len_lk):
            for j in range(i + 1, len_lk):
                # 前k-2项相同时合并两个集合
                l1 = list(lk[i])[:k - 2]
                l2 = list(lk[j])[:k - 2]
                if sorted(l1) == sorted(l2):
                    next_lk.append(lk[i] | lk[j])

        return next_lk

    # 生成频繁项集
    def generate_lk(self):
        # 构建候选项集c1
        c1 = self.create_c1(self.data)
        l1, support_data = self.scan_support_data(c1)
        l = [l1]
        k = 2
        while len(l[k - 2]) > 0:
            # 组合项集lk中的元素，生成新的候选项集ck
            ck = self.generate_new_ck(l[k - 2], k)
            lk, sup_k = self.scan_support_data(ck)
            support_data.update(sup_k)
            l.append(lk)
            k += 1
        return l, support_data

    # 生成相关规则
    def generate_rules(self, l, suppor_data):
        rule_result = []  # 最终记录的相关规则结果
        for i in range(1, len(l)):
            for ck in l[i]:
                cks = [frozenset([item]) for item in ck]
                # 频繁项集中由三个及三个以上元素的集合
                self.rules_of_more(ck, cks, suppor_data, rule_result)
        return rule_result

    # 频繁项集中只有两个元素
    def rules_of_two(self, ck, cks, suppor_data, rule_result):
        prunedh = []
        for oneck in cks:
            # 计算置信度
            conf = suppor_data[ck] / suppor_data[ck - oneck]
            if conf >= self.min_confidenct:
                print(ck - oneck, "-->", 'Confidenct is :', conf)
                rule_result.append((ck - oneck, oneck, conf))
                prunedh.append(oneck)
        return prunedh

    # 频繁项集中由三个及三个以上元素的集合，递归生成相关规则
    def rules_of_more(self, ck, cks, suppor_data, rule_result):
        m = len(cks[0])
        while len(ck) > m:
            cks = self.rules_of_two(ck, cks, suppor_data, rule_result)
            if len(cks) > 1:
                cks = self.generate_new_ck(cks, m + 1)
                m += 1
            else:
                break


if __name__ == '__main__':
    apriori = Apriori(min_support=0.5, min_confidence=0.6)
    m_l, m_support_data = apriori.generate_lk()
    for one in m_l:
        print('项数为%s的频繁项集:' % (m_l.index(one) + 1), one)
    print('SupportData:', m_support_data)
    print('MinConfidence=0.6时:')
    m_rules = apriori.generate_rules(m_l, m_support_data)
