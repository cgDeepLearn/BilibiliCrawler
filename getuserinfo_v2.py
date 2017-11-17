# -*- coding: utf8 -*-
"""
get bilibili user info v2
change url to api.bilibili
"""


# http://api.bilibili.com/cardrich?callback=jQuery17202870352235622704_1482889079913&mid=122541&type=jsonp&_=1482891272353


import json
import time
import random
import csv
import logging
import requests
from datetime import datetime


FMT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=FMT,
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log/userinfo_test.log',
                    filemode='a')

def LoadUserAgent(filename):
    """
    filename:string,path to user-agent file
    """
    ualist = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line:
                ualist.append(line.strip()[1:-1])
    random.shuffle(ualist)
    return ualist

UAS = LoadUserAgent('user_agents.txt')
proxies = {'http': 'http://119.29.158.87:80',
            'http': 'http://123.7.38.31:9999',
            'http': 'http://211.103.208.244:80',
            'http': 'http://27.219.38.130:81189',
            'http': 'http://61.135.217.7:80',
            'http': 'http://120.40.38.130:808',
            'http': 'http://221.211.221.34:80',
            'http': 'http://61.178.238.122:63000',
            'http': 'http://27.46.32.69:9797',
            'http': 'http://120.40.38.130:808'
            

}


def get_timestamp():
    # 返回毫秒数
    return int(round(datetime.now().timestamp() * 1000))


class BiliUser():
    """通过uid获取Bilibili User Info"""

    def __init__(self, uid):
        """
        uid: user id
        -----info format-----:
        (mid,name,approve,sex,face,DisplayRank,regtime,spacesta,birthday,
        place,description,article,fans,attention,sign,level,verify,vip)
        """
        self.uid = uid
        self.info = None

    def getUserInfo(self):
        url = 'http://api.bilibili.com/cardrich'
        timestamp_ms = get_timestamp()
        params = {'mid': str(self.uid), '_': '{}'.format(timestamp_ms)}
        headers = {'User-Agent': random.choice(UAS)}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
        except Exception as e:
            # print(e)
            msg = 'uid({}) get error'.format(self.uid)
            logging.error(msg)
            # logging.error(e)
            return None
        text = json.loads(res.text)
        if text['code'] == 0:
            data = text['data']['card']
            self.info = (data['mid'], data['name'],
                            data['approve'], data['sex'], data['face'],
                            data['DisplayRank'], data['regtime'],
                            data['spacesta'], data['birthday'],
                            data['place'], data['description'],
                            data['article'], data['fans'],
                            data['attention'], data['sign'],
                            data['level_info']['current_level'],
                            data['official_verify']['type'],
                            data['vip']['vipStatus'])
            return self.info
        
        else:
            msg = 'uid({}) request code return error'.format(self.uid)
            logging.info(msg)
            return None


if __name__ == '__main__':
    gu = BiliUser(1)
    gu.getUserInfo()
    print(gu.info)