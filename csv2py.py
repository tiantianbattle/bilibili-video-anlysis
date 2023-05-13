# coding：utf-8 -*-
# author 小红帽
# time: 2022/11/27 1:07

import pandas as pd
data = pd.read_csv('commit&time2.csv')
for line in data.values:
    print(str(line[0]))
#with open('评论2.txt','a+') as f:
#     for line in data.values:
#         f.write((str(line[1])))
