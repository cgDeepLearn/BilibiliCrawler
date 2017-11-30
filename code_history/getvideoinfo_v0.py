# -*-coding: utf-8 -*-
import json
import csv
import requests
from bs4 import BeautifulSoup

# 获取视频信息类
# http://api.bilibili.com/archive_stat/stat?aid=7


class GetVideo:

    def __init__(self, aid):
        self.aid = aid
        self.info = None

    # 获取视频基本信息
    def getVideoBaseInfo(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        url = 'https://www.bilibili.com/video/av{}/'.format(self.aid)
        try:
            r = requests.get(url, timeout=30, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, 'html.parser')
            tmp = soup('script', {'language': 'javascript'})[-1]
            t = str(tmp)
            t = t[t.find('aid'):t.find(', wb_summary')
                  ].replace("'", "").split(',')
            for i in t:
                i = i.strip().encode('utf-8').decode("unicode-escape")
                if not i.find('mid') == -1:
                    self.uid = i[4:]
                if not i.find('wb_title =') == -1:
                    self.videoName = i[i.find('"') + 1:i.rfind('"')]
                if not i.find('wb_img') == -1:
                    self.icon = i[i.find('=') + 1:]
                if not i.find('wb_full_url') == -1:
                    self.link = i[i.find('=') + 1:]
        except:
            return None

    # 获取视频详细信息
    def getVideoArchiveInfo(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        url = 'http://api.bilibili.com/archive_stat/stat?callback=jQuery17203163676409493352_1492874705738&aid={}'.format(
            self.aid)
        try:
            r = requests.get(url, timeout=30, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            t = json.loads(r.text)
            self.watchNumber = t['data']['view']
            self.barrageNumber = t['data']['danmaku'] # 弹幕数量
            self.rank = t['data']['his_rank']
            self.coinNumber = t['data']['coin']
            self.favoriteNumber = t['data']['favorite']
            self.replyNumber = t['data']['reply']
            self.info = (self.uid, self.aid, self.videoName, self.watchNumber, self.barrageNumber, self.rank, self.coinNumber, self.favoriteNumber, self.replyNumber)
            # 新加的推荐
        except:
            return None

    # 返回SQL插入语句
    def getInsertSQLCode(self):
        sql = "insert into video_db (aid, uid, videoName, watchNumber, barrageNumber, rank, coinNumber, favoriteNumber, replyNumber, icon, link) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            self.aid, self.uid, self.videoName, self.watchNumber, self.barrageNumber, self.rank, self.coinNumber, self.favoriteNumber, self.replyNumber, self.icon, self.link)
        return sql


def get_vinfo(aid):
    gv = GetVideo(aid)
    gv.getVideoBaseInfo()
    gv.getVideoArchiveInfo()
    return gv.info


if __name__ == '__main__':
    INDEX = input("please input vlist file index: ")
    with open('vlist/vlist_{}.csv'.format(INDEX), 'r', newline='') as f1, \
    open('vinfo_{}.csv'.format(INDEX), 'w', encoding='utf8', newline='') as f2:
        reader = csv.reader(f1)
        writer = csv.writer(f2)
        for row in reader:
            vlist = eval(row[2])
            for aid in vlist:
                # print(aid)
                vinfo = get_vinfo(aid)
                if vinfo is not None:
                    writer.writerow(vinfo)