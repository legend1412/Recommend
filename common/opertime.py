import datetime

# unix时间戳
unix_ts = 1238536800000
# 时间戳转化为时间
tl = datetime.datetime.fromtimestamp(unix_ts/1000)
print(str(unix_ts)+"转换为时间是:{}".format(tl))
