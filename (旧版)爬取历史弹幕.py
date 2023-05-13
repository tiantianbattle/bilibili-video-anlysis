# coding：utf-8 -*-
# author 小红帽
# time: 2022/11/15 12:00

import re
import time
import requests
import pandas as pd

def get_cid(bvid):
    '''
    通过视频的bvid获得视频的cid
    输入：视频的bvid
    输出：视频的cid
    '''
    url = 'https://api.bilibili.com/x/player/pagelist?bvid=%s&jsonp=jsonp'%bvid
    res = requests.get(url)
    data = res.json()
    return data['data'][0]['cid']

def parse_dm(text):
    '''
    解析视频弹幕
    输入：视频弹幕的原数据
    输出：弹幕的解析结果
    '''
    result = [] # 用于存储解析结果
    data = re.findall('<d p="(.*?)">(.*?)</d>',text)
    for d in data:
        item = {} # 每条弹幕数据
        dm = d[0].split(',') # 弹幕的相关详细，如出现时间，用户等
        item['出现时间'] = float(dm[0])
        item['模式'] = int(dm[1])
        item['字号'] = int(dm[2])
        item['颜色'] = int(dm[3])
        item['评论时间'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(dm[4])))
        item['弹幕池'] = int(dm[5])
        item['用户ID'] = dm[6] # 并非真实用户ID，而是CRC32检验后的十六进制结果
        item['rowID'] = dm[7] # 弹幕在数据库中的ID，用于“历史弹幕”功能
        item['弹幕内容'] = d[1]
        result.append(item)
    return result

def get_history(bvid,date):
    '''
    获取视频历史弹幕
    输入：视频bvid,日期
    输出：视频某一日期开始的弹幕
    '''
    oid = get_cid(bvid)
    url = 'https://api.bilibili.com/x/v2/dm/history?type=1&oid=%d&date=%s'%(oid,date)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
               'Accept': '*/*',
               'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
               'Origin': 'https://www.bilibili.com',
               'Connection': 'keep-alive',
               'Referer': 'https://www.bilibili.com/video/BV1k54y1U79J',
               'TE': 'Trailers'}
    # 此接口需要登陆，因此需要cookies
    cookies = {}
    res = requests.get(url,headers=headers,cookies=cookies)
    res.encoding = 'utf-8'
    text = res.text
    dms = parse_dm(text) # 解析弹幕
    return dms

def get_dms(bvid):
    '''
    获取视频弹幕（此方法获取的弹幕数量更多）
    输入：视频的bvid
    输出：视频的弹幕
    '''
    print('视频解析中...')
    info = get_info(bvid)
    print('视频解析完成!')
    print('【视频标题】： %s\n【视频播放量】：%d\n【弹幕数量】：  %d\n【上传日期】：  %s'%(info[0],info[1],info[2],info[3]))
    dms = get_dm(bvid) # 存储弹幕
    if len(dms) >= info[2]: # 如果弹幕数量已抓满
        return dms
    else:
        dms = []
        date = time.strftime('%Y-%m-%d',time.localtime(time.time())) # 从今天开始
        while True:
            dm = get_history(bvid,date)
            dms.extend(dm)
            print('"%s"弹幕爬取完成!(%d条)'%(date,len(dm)))
            if len(dm) == 0: # 如果为空
                break
            end = dm[-1]['评论时间'].split()[0] # 取最后一条弹幕的日期
            if end == date: # 如果最后一条仍为当天，则往下推一天
                end = (datetime.datetime.strptime(end,'%Y-%m-%d')-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            if end == info[3]: # 如果已经到达上传那天
                break
            else:
                date = end
        dm = get_history(bvid,info[3]) # 避免忽略上传那天的部分数据
        dms.extend(dm)
        print('弹幕爬取完成!(共%d条)'%len(dms))
        print('数据去重中...')
        dms = del_repeat(dms,'rowID') # 按rowID给弹幕去重
        print('数据去重完成!(共%d条)'%len(dms))
        return dms

if __name__ == '__main__':
    dms = get_dms('BV1HJ411L7DP')
    dms = pd.DataFrame(dms)
    dms.to_csv('一路向北.csv',index=False)