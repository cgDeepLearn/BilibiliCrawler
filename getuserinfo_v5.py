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
import sys
import csv
import requests

FMT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=FMT,
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log/userinfo_1000000.log',
                    filemode='w')


class GetUser():

    def __init__(self, uid):
        self.uid = uid
        self.info = None
        self.text = None
        self.videoNumber = 0
        self.fansNumber = 0
        self.headers = {'Accept': 'application/json, text/plain, */*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'Connection': 'keep-alive',
                        'Content-Length': '32',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Cookie': 'UM_distinctid=15b9449b43c1-04dfdd66b40759-51462d15-1fa400-15b9449b43d83; fts=1492841510; sid=j4j61vah; purl_token=bilibili_1492841536; buvid3=30EA0852-5019-462F-B54B-1FA471AC832F28080infoc; rpdid=iwskokplxkdopliqpoxpw; _cnt_pm=0; _cnt_notify=0; _qddaz=QD.cbvorb.47xm5.j1t4z5yc; pgv_pvi=9558976512; pgv_si=s2784223232; _dfcaptcha=02d046fd3cc2bfd2ce6724f8b2185887; CNZZDATA2724999=cnzz_eid%3D1176255236-1492841785-http%253A%252F%252Fspace.bilibili.com%252F%26ntime%3D1492857985',
                        'Host': 'space.bilibili.com',
                        'Origin': 'https://space.bilibili.com',
                        'Referer': 'https://space.bilibili.com/{}/'.format(self.uid),
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest'}

    # 获取用户信息
    def getUserInfo(self):
        url = 'https://space.bilibili.com/ajax/member/GetInfo'
        try:
            data = {'mid': '{}'.format(
                self.uid), '_': '1492863092419', 'csrf': ''}

            r = requests.post(url, headers=self.headers, data=data)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            self.text = json.loads(r.text)
            # print(self.text)
            self.get_main_info()  # 获取主要信息

        except:
            # logging.error('uid (%s) get error' % self.uid)
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
            registerTime = time.ctime(float(data['regtime']))
        except:
            registerTime = 0
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
            vlist = []
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
            if not u.getUserInfo():
                logging.error("uid(%s) info get error" % u.uid)
                continue
            vlist = u.get_video_list()
            logging.info('---- uid:%s---- vnum:%s -----' %
                         (u.uid, u.videoNumber))
            csvwriter1 = csv.writer(f1)
            userinfo = u.info
            csvwriter1.writerow(userinfo)
            csvwriter2 = csv.writer(f2)
            if vlist:
                try:
                    aids = list(vlist)
                except:
                    logging.error("%s get vlist errror" % u.uid)
                    continue
            else:
                if u.videoNumber:
                    logging.error("%s get vlist error" % u.uid)
                    continue
                aids = []
            csvwriter2.writerow([u.uid, u.videoNumber, aids])
            # time.sleep(1)

