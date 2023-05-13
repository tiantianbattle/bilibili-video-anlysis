# coding：utf-8 -*-
# author 小红帽
# time: 2022/11/26 21:45

import numpy as np
import pandas as pd

text = []

fileHandler = open("评论&time.txt","r",encoding='utf-8')
while True:
    line  =  fileHandler.readline()
    if  not  line  :
        break
    line = line.strip().split('      ')
    text.append(line)
fileHandler.close()
df = pd.DataFrame(text)
df.to_csv("commit&time2.csv", index=False,header=None)
