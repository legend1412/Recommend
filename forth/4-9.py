from forth.kmeans import KMeans

if __name__ == '__main__':
    init_file = 'data/sku-price/skuid_price.csv'
    km = KMeans()
    m_data = km.load_data(init_file)
    m_new_data, m_upper_limit, m_lower_limit = km.filter_anomaly_value(m_data)
    m_cluster = km.k_means(m_new_data['price'].values, k=7, maxiters=200)
    print(m_cluster)
