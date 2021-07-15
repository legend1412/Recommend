import numpy as np
from forth.kmeans import KMeans


class BisectingKMeans:
    # 计算对应的SSE值
    def calc_sse(self, data, mean):
        new_data = np.mat(data) - mean
        return (new_data * new_data.T).tolist()[0][0]

    # 二分-kmeans
    def bis_kmeans(self, data, k=7):
        cluster_sse_result = dict()  # 簇类对应的SSE值
        cluster_sse_result.setdefault(0, {})
        cluster_sse_result[0]['values'] = data
        cluster_sse_result[0]['sse'] = np.inf
        cluster_sse_result[0]['center'] = np.mean(data)

        while len(cluster_sse_result) < k:
            max_sse = -np.inf
            max_sse_key = 0
            # 找到最大的sse值对应数据，进行kmeans聚类
            for key in cluster_sse_result.keys():
                if cluster_sse_result[key]['sse'] > max_sse:
                    max_sse = cluster_sse_result[key]['sse']
                    max_sse_key = key
            # cluster_result {0:{'center':x,'values':[]},0:{'center':x,'values':[]}}
            cluster_result = km.k_means(cluster_sse_result[max_sse_key]['values'], k=2, maxiters=200)

            # 删除cluster_sse_result中的max_sse_key对应的值
            del cluster_sse_result[max_sse_key]
            # 将经过kmeans聚类后的结果赋值给cluster_sse_result
            cluster_sse_result.setdefault(max_sse_key, {})
            cluster_sse_result[max_sse_key]['center'] = cluster_result[0]['center']
            cluster_sse_result[max_sse_key]['values'] = cluster_result[0]['values']
            cluster_sse_result[max_sse_key]['sse'] = self.calc_sse(cluster_result[0]['values'],
                                                                   cluster_result[0]['center'])

            max_key = max(cluster_sse_result.keys()) + 1
            cluster_sse_result.setdefault(max_key, {})
            cluster_sse_result[max_key]['center'] = cluster_result[1]['center']
            cluster_sse_result[max_key]['values'] = cluster_result[1]['values']
            cluster_sse_result[max_key]['sse'] = self.calc_sse(cluster_result[1]['values'], cluster_result[1]['center'])

        return cluster_sse_result


if __name__ == '__main__':
    init_file = 'data/sku-price/skuid_price.csv'
    km = KMeans()
    bk = BisectingKMeans()
    m_data = km.load_data(init_file)
    m_new_data, m_upper_limit, m_lower_limit = km.filter_anomaly_value(m_data)
    cluster_sse = bk.bis_kmeans(m_new_data['price'].values, k=7)
    print(cluster_sse)
