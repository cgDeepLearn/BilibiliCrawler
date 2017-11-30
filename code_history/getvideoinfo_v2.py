
# -*- coding: utf8 -*-
"""
get bilibili user info v2
change url to api.bilibili
get video info with uid or not
"""


import json
import random
import logging
from datetime import datetime
import requests


FMT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=FMT,
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log/videoinfo_test.log',
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

PROXIES = {'http': 'http://119.29.158.87:80',
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


class BiliVideo():
    """通过uid获取Bilibili User Info"""

    def __init__(self, aid, uid=None):
        """
        aid: video id
        -----info format-----:
        ('uid', aid','view','danmaku','reply','favorite','coin','share',
        'now_rank','his_rank','like','no_reprint','copyright')
        """
        if uid is None:
            self.uid = 0
        self.aid = aid
        self.info = None

    def getVideoInfo(self):
        url = 'http://api.bilibili.com/archive_stat/stat'
        timestamp_ms = get_timestamp()
        params = {'aid': str(self.aid), '_': '{}'.format(timestamp_ms)}
        headers = {'User-Agent': random.choice(UAS)}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
        except Exception as e:
            # print(e)
            msg = 'aid({}) get error'.format(self.aid)
            logging.error(msg)
            return None
        text = json.loads(res.text)
        if text['code'] == 0:
            data = text['data']
            self.info = (self.uid, self.aid, data['view'], data['danmaku'],
                         data['reply'], data['favorite'], data['coin'],
                         data['share'], data['now_rank'], data['his_rank'],
                         data['like'], data['no_reprint'], data['copyright'])
            return self.info

        else:
            msg = 'aid({}) request code return error'.format(self.aid)
            logging.info(msg)
            return None


if __name__ == '__main__':
    gv = BiliVideo(100)
    gv.getVideoInfo()
    print(gv.info)
