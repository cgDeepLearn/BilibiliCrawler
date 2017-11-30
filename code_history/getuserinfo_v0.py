# -*-coding: utf-8 -*-
"""
get bilibili user info
date:2017/9/21
2017-3-31,id-->100000000
2017-11-13,id-->250000000

"""

import json
import time
import logging
import random
import sys
from datetime import datetime
import csv
import requests

FMT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=FMT,
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log/userinfo_test.log',
                    filemode='w')


def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return str(int(round(time.time() * 1000)))
    return current_milli_time()


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
proxies = {'https': 'https://60.255.186.169:8888',
           'https': 'https://14.221.164.10:9797',


           }


class GetUser():

    def __init__(self, uid):
        self.uid = uid
        self.info = None
        self.text = None
        self.videoNumber = 0
        self.fansNumber = 0
        self.useragent = random.choice(UAS)
        # print(self.useragent)
        # self.headers = {'Accept': 'application/json, text/plain, */*',
        #                 'Accept-Encoding': 'gzip, deflate',
        #                 'Accept-Language': 'zh-CN,zh;q=0.8',
        #                 'Connection': 'keep-alive',
        #                 'Content-Length': '32',
        #                 'Content-Type': 'application/x-www-form-urlencoded',
        #                 'Cookie': 'UM_distinctid=15b9449b43c1-04dfdd66b40759-51462d15-1fa400-15b9449b43d83; fts=1492841510; sid=j4j61vah; purl_token=bilibili_1492841536; buvid3=30EA0852-5019-462F-B54B-1FA471AC832F28080infoc; rpdid=iwskokplxkdopliqpoxpw; _cnt_pm=0; _cnt_notify=0; _qddaz=QD.cbvorb.47xm5.j1t4z5yc; pgv_pvi=9558976512; pgv_si=s2784223232; _dfcaptcha=02d046fd3cc2bfd2ce6724f8b2185887; CNZZDATA2724999=cnzz_eid%3D1176255236-1492841785-http%253A%252F%252Fspace.bilibili.com%252F%26ntime%3D1492857985',
        #                 'Host': 'space.bilibili.com',
        #                 'Origin': 'https://space.bilibili.com',
        #                 'Referer': 'https://space.bilibili.com/{}/'.format(self.uid),

        #                 'X-Requested-With': 'XMLHttpRequest'}
        self.headers = {'Referer': 'https://space.bilibili.com/' + str(self.uid) + '?from=search&seid=' + str(random.randint(10000, 50000)),
                        'User-Agent': self.useragent
                        }
        # print(self.headers)
    # 获取用户信息

    def getUserInfo(self):
        url = 'https://space.bilibili.com/ajax/member/GetInfo'
        try:
            # data = {'mid': '{}'.format(
            #   self.uid), '_': '1492863092419', 'csrf': ''}
            data = {'mid': str(self.uid), '_': datetime_to_timestamp_in_milliseconds(
                datetime.now())}
            # print(data)
            r = requests.post(url, headers=self.headers,
                              data=data, proxies=proxies)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            self.text = json.loads(r.text)
            # print(self.text)
            self.get_main_info()  # 获取主要信息

        except:
            logging.error('uid (%s) get error' % self.uid)
            return None

    def get_main_info(self):
        """
        基本信息
        """

        text = self.text
        data = text['data']
        author = data['name']
        sex = data['sex'] if data['sex'] else '无'
        # print(sex)
        sign = data['sign'] if 'sign' in data else '无'
        # print(sign)
        birthday = data['birthday'] if 'birthday' in data else '无'
        # print(birthday)
        address = data['place'] if 'place' in data else '无'
        # print(address)
        icon = data['face'] if 'face' in data else '无'
        # fans_num = text['data']['fans']
        watchNumber = data['playNum']
        try:
            dt = datetime.fromtimestamp(float(data['regtime']))
            # registerTime = time.ctime(float(data['regtime']))
            registerTime = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            registerTime = 'no'
        fansNumber = self.get_relation()  # get fansNumber
        videonum_info = self.get_video_num()
        if videonum_info is None:
            videoNumber, video_pages = 0, 0
        else:
            videoNumber, _ = videonum_info
        self.videoNumber = videoNumber
        self.info = (self.uid, author, sex, sign, fansNumber, watchNumber,
                     registerTime, birthday, address, icon, videoNumber)
        # print(self.info)

# uid,author,sex,sign,fansNumber,watchNumber,registerTime,birthday,address,icon,videoNum

    def get_relation(self):
        """
        粉丝数和up关注的人数
        """
        url = 'https://api.bilibili.com/x/relation/stat'
        params = {"vmid": '{}'.format(self.uid)}
        try:
            r = requests.get(url, params=params)
            text = json.loads(r.text)
            fansNumber = text['data']['follower']
            self.fansNumber = fansNumber
            return fansNumber
        except:
            return 0

    def is_up(self):
        videonum_info = self.get_video_num()
        if videonum_info is not None and videonum_info[0] > 1:
            return True
        return False

    def get_video_num(self):
        url = 'http://space.bilibili.com/ajax/member/getSubmitVideos'
        params = {"mid": '{}'.format(self.uid)}
        video_num = 0
        video_pages = 0

        try:
            response = requests.get(url, params=params)
            text = json.loads(response.text)
        except:
            return None

        video_num = text['data']['count']
        video_pages = text['data']['pages']
        return video_num, video_pages
# http://api.bilibili.com/cardrich?callback=jQuery17202870352235622704_1482889079913&mid=122541&type=jsonp&_=1482891272353

    def get_video_list(self):
        url = 'http://space.bilibili.com/ajax/member/getSubmitVideos'
        params = {"mid": '{}'.format(self.uid)}
        video_num = 0
        video_pages = 0

        try:
            response = requests.get(url, params=params)
            text = json.loads(response.text)
        except:
            return None

        video_num = text['data']['count']
        video_pages = text['data']['pages']
        self.videoNumber = video_num
        # print(self.videoNumber)
        if video_num < 1:  # 没投过稿件的pass
            return None

        def get_aids(url, mid, pages):
            """返回所有aid的序列"""
            vlist = None
            for page in range(1, pages + 1):
                params = {"mid": '{}'.format(mid), "page": '{}'.format(page)}
                response = requests.get(url, params=params)
                text = json.loads(response.text)
                if text is not None:
                    vlist = text['data']['vlist']
                else:
                    logging.error('uid %d vlist get error' % mid)
                    return None
                for item in vlist:
                    # print(item['aid'])
                    yield (item['aid'])

        return get_aids(url, self.uid, video_pages)
# uid, author, sex, sign, fansNumber, watchNumber,registerTime,birthday,address,icon,link

    def getInsertSQLCode(self):
        if not self.info:
            return None
        sql = "insert into user_db(uid, author, sex, sign, fansNumber,watchNumber,\
         registerTime, birthday, address, icon, videoNumber) values(\
         '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(*self.info)
        return sql


def get_uinfo(uid):
    gu = GetUser(uid)
    gu.getUserInfo()
    return gu.info


if __name__ == '__main__':
    # 输入抓取范围
    RANGE_START = int(input("please input start uid: "))
    RANGE_END = int(input("please input end uid: "))
    assert RANGE_START < RANGE_END
    # 分别存入upinfo文件和视频vlist文件
    with open('uinfo/biliup_info_{}.csv'.format(RANGE_END), 'w', encoding='utf8', newline='') as f1, open(
            'vlist/vlist_{}.csv'.format(RANGE_END), 'w', encoding='utf8', newline='') as f2:
        for index in range(RANGE_START, RANGE_END):
            if index % 1000 == 1:
                print("uid: ", index)
            u = GetUser(index)
            if u.get_relation() < 5000:  # 取粉丝数大于5000的up主:
                time.sleep(0.01)
                continue
            u.getUserInfo()
            vlist = u.get_video_list()
            logging.info('---- uid:%s---- vnum:%s -----' %
                         (u.uid, u.videoNumber))
            csvwriter1 = csv.writer(f1)
            userinfo = u.info
            csvwriter1.writerow(userinfo)
            csvwriter2 = csv.writer(f2)
            if vlist:
                aids = list(vlist)
            else:
                if u.videoNumber:
                    logging.error('uid %d vlist get error' % u.uid)
                    continue
                aids = []
            csvwriter2.writerow([u.uid, u.videoNumber, aids])
            # time.sleep(1)
