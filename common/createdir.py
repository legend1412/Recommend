import os


#  创建目录
def mkdir(pathlist):
    folder = os.getcwd()
    for path in pathlist:
        folder = os.path.join(folder, path)

    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


# 先创建目录，再创建此目录下的文件
def mkfilefromdir(pathlist, filename):
    folder = mkdir(pathlist)
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        file = open(filepath, 'w')
        file.close()


# 创建文件,需要文件的绝对路径
def mkfile(filepath):
    if not os.path.exists(filepath):
        file = open(filepath, 'w')
        file.close()


if __name__ == '__main__':
    list1 = list()
    list1.append('data')
    list1.append('p')
    list1.append('a')
    mkfilefromdir(list1, 'a.txt')
