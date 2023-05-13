# coding：utf-8 -*-
# author 小红帽
# time: 2022/11/13 23:10

#导入结巴讽刺模块
import jieba
#导入词云模块
import wordcloud
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Bar
import numpy as np



# 读取文件内容
with open('弹幕.txt','r' ,encoding='utf-8')as f:
    txt = f.read()

#去除无关数据
#txt = txt.replace('二舅','')
ls = jieba.lcut(txt)

#将文本数据转为字典
#dict()用于创建一个字典 counter()作用就是在一个数组内，遍历所有元素，将元素出现的次数记下来

dict = {}
for i in range(len(ls)):
    dict[i] = ls[i]
data = Counter(dict)
#选出词频最高的10个
c = Counter()
for i in ls:
    if len(i)>1 and i != '\r\n':
        c[i] +=1

high = c.most_common(10)

keyValue = []

for i in range(len(high)):
    keyValue.append(list(high[i]))

d = {k:v for [k,v] in keyValue}

#图表
# bar = Bar()
# key = list(d.keys())
# value = list(d.values())
# bar.add_xaxis(key)
# bar.add_yaxis('数量',value)
# bar.render('清洗后的评论.html')

content = ''.join(ls)
#读入存储wordcount的文件路径
wc=wordcloud.WordCloud(
    max_words=20,
    width=300,
    height=300,
    background_color='white',
    scale=15,
    font_path='msyh.ttc' #设置字体,

)

wc.generate(content)
wc.to_file('0725弹幕数据.png')