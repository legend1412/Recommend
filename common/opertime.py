import datetime
import time

# unix时间戳
unix_ts = 1238536800000
# 时间戳转化为时间
tl = datetime.datetime.fromtimestamp(unix_ts / 1000)
# print(str(unix_ts) + "转换为时间是:{}".format(tl))


# 13位时间戳转换为时间
def transform_time(t1):
    try:
        dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t1))
    except Exception as e:
        print(t1)
        print('%s,%s' % (t1, e))
        dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(0))
    return dt
