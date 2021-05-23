import os


# 创建文件
def mkfile(filepath):
    filepath1 = os.path.join(os.getcwd(), filepath)
    if not os.path.exists(os.path.dirname(filepath1)):
        os.makedirs(os.path.dirname(filepath1))
    if not os.path.exists(filepath1):
        file = open(filepath1, 'w')
        file.close()


# 创建目录
def mkdir(dirs):
    if not os.path.exists(os.path.join(os.getcwd(), dirs)):
        os.makedirs(os.path.join(os.getcwd(), dirs))


# 写入文件
def write_to_file(filename, one):
    fw = open(filename, "a", encoding="utf8")
    fw.write(str(one) + "\n")
    fw.close()
