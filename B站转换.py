# coding：utf-8 -*-
# author 小红帽
# time: 2022/11/13 20:49

from xml.etree.ElementTree import parse


import requests
import json
import re


header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
def CIDget(bvid):
    url = 'https://api.bilibili.com/x/player/pagelist?bvid='+str(bvid)+'&jsonp=jsonp'
    response = requests.get(url,headers=header, timeout=2000)
    dirt = json.loads(response.text)
    cid = dirt['data'][0]['cid']
    nowDMget(cid)

def nowDMget(cid):
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='+str(cid)
    response = requests.get(url,headers=header, timeout=2000)
    response.encoding = 'utf-8'
    data = re.findall('<d p=".*?>(.*?)</d>',response.text)
    print(len(data))
    # for item in data:
    #     with open('danmu_1000.txt',mode='a',encoding='utf-8') as f:
    #         f.write(item+'\n')

CIDget('BV1MN4y177PB')