'''
@Name           :count_data.py
@Description    :
@Time           :2022/03/07 16:39:53
@Author         :Zijie NING
@Version        :1.0

Count the number of pictures in each class.
'''


import os

count = [0, 0, 0, 0, 0, 0, 0]

path = "path"
dirs = os.listdir(path)
for i in dirs:
    if os.path.splitext(i)[1] == ".txt":
        f = open(path + "/" + i)
        # print(f)
        for line in f:
            i = int(line[0])
            print(line)
            count[i] += 1
        f.close()
print(count)
