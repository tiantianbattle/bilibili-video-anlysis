# coding：utf-8 -*-
# author 小红帽
# time: 2022/11/15 14:38
# -*- coding: utf-8 -*-



import json
import requests
from dm_pb2 import DmSegMobileReply
from google.protobuf.json_format import MessageToJson, Parse


b_web_cookie = 'buvid3=B777C3A2-D5C7-4854-8820-C51361CBDB7D184984infoc; LIVE_BUVID=AUTO1816255342865186; b_ut=5; i-wanna-go-back=2; _uuid=63855654-9C33-41A10-1F2B-81C64389E38248493infoc; fingerprint3=d4427f8b9ecfd41fb5f2a16779758bcd; buvid_fp_plain=undefined; nostalgia_conf=-1; CURRENT_BLACKGAP=0; hit-dyn-v2=1; blackside_state=0; b_nut=100; CURRENT_QUALITY=112; CURRENT_FNVAL=4048; fingerprint=d2c52f7217759297f2d4c4b15a4bcf73; DedeUserID=35170814; DedeUserID__ckMd5=53af129a863ddf15; hit-new-style-dyn=0; rpdid=|(u|kk~Y~kJl0J\'uYY)~Y|Juk; PVID=1; buvid4=A2922401-AEAF-8DA5-C36F-99E5D08794AD49830-022012418-WEPh3cauru8ifY9FwkVnF05iqj3PxjzxYmcthGmsHu+TP2Ew9JLqpQ==; buvid_fp=d2c52f7217759297f2d4c4b15a4bcf73; SESSDATA=a3f5ad75,1684993226,85fe2*b1; bili_jct=e85d50e8465fdcc999c5426b6a274f80; sid=5svfux4r; b_lsid=C3CB3B19_184B4FD9368; bp_video_offset_35170814=732933360330997800'


def get_date_list():
    url = "https://api.bilibili.com/x/v2/dm/history/index?type=1&oid=783037295&month=2022-07"
    headers = {
        'cookie': b_web_cookie
    }
    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), ensure_ascii=False, indent=4))


def dm_real_time():
    url_real_time = 'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid=783037295&pid=898762590&segment_index=1'
    resp = requests.get(url_real_time)

    DM = DmSegMobileReply()
    DM.ParseFromString(resp.content)
    data_dict = json.loads(MessageToJson(DM))
    # print(data_dict)
    list(map(lambda x=None: print(x['content']), data_dict.get('elems', [])))


def dm_history(date):
    url_history = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=783037295&date='+str(date)
    headers = {
        'cookie': b_web_cookie
    }
    resp = requests.get(url_history, headers=headers)
    DM = DmSegMobileReply()
    DM.ParseFromString(resp.content)
    data_dict = json.loads(MessageToJson(DM))
    data = data_dict.get('elems')
    #print(data_dict.get('elems')['content'])
    #res = list(map(lambda x=None: (x['content']), data_dict.get('elems', [])))
    #print(res)
    with open('弹幕0807.txt','a+',encoding='utf-8')as f:
        for danmu in data:
            try:
                f.write(danmu['content']+'\n')
            except:
                print('错误')
    print(date+'已完成')
if __name__ == '__main__':
    # dm_real_time()
    #get_date_list()
    date = ['2022-08-07','2022-08-08','2022-08-09','2022-08-10','2022-08-11','2022-08-12','2022-08-13']
    #date = ['2022-07-25', '2022-07-26', '2022-07-27', '2022-07-28', '2022-07-29', '2022-07-30', '2022-07-31']
    for i in date:
        dm_history(i)
    pass