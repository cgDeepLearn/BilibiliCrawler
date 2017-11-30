import re
import os
import traceback
import requests
import pymysql


from bs4 import BeautifulSoup
from getuserinfo import *
from getvideoinfo import *

# comment
# http://api.bilibili.com/x/v2/reply?callback=jQuery17202870352235622704_1482889079904&jsonp=jsonp&pn=1&type=1&oid=170001&sort=0&_=1482889773903

# userinfo
# http://api.bilibili.com/cardrich?callback=jQuery17202870352235622704_1482889079913&mid=2325015&type=jsonp&_=1482891272353

# videoinfo
# https://api.bilibili.com/x/web-interface/archive/stat?aid=170001
# 数据库连接语句，请手动修改
try:
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                           passwd='root', db='bilibili', charset="utf8")
    cursor = conn.cursor()
except:
    print('\nError: database connection failed')


# 建表
try:
    cursor.execute('create table author_db(uid varchar(32) not null primary key, author text, sex text, sign text, fansNumber text, watchNumber text, registerTime text, birthday text, address text, icon text, videoNumber text)')
    conn.commit()
    cursor.execute('create table video_db(aid varchar(32) not null primary key, uid varchar(32), videoName text, watchNumber text,barrageNumber text, rank text, coinNumber text, favoriteNumber text, replyNumber text, icon text, link text)')
    conn.commit()
except:
    pass


def getHTMLText(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return None

# 返回BeautifulSOup对象


def getSoupObj(url):
    try:
        html = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except:
        return None

# 返回视频是否已经存在数据库


def isExistAvId(avId):
    global conn, cursor

    cursor.execute('select aid from video_db where aid = {}'.format(avId))
    result = cursor.fetchone()
    if result == None:
        return False
    else:
        return True

# 判断UP主是否已经存在数据库中


def isExistAuthor(uid):
    global conn, cursor

    cursor.execute('select uid from author_db where uid = {}'.format(uid))
    result = cursor.fetchone()
    if result == None:
        return False
    else:
        return True

# 处理UP主信息


def parserAuthorInfo(uid):
    global conn, cursor

    url = 'http://space.bilibili.com/{}/#!/'.format(uid)
    soup = getSoupObj(url)

    gu = GetUser(uid)
    gu.getUserInfo()

    sql = gu.getInsertSQLCode()
    cursor.execute(sql)
    conn.commit()

# 处理视频信息


def parserVideoInfo(url, avId):
    global conn, cursor

    if isExistAvId(avId):
        print('提示：数据库已经存在该视频')
        return None

    soup = getSoupObj(url + avId)
    if(soup == None):
        print('\n错误：获取Soup对象失败')
        return None

    infos = soup('div', {'class': 'viewbox'})
    if len(infos) == 0:
        cursor.execute('insert into video_db (aid) values ({})'.format(avId))
        conn.commit()
    elif len(infos) == 1:
        uid = soup('a', {'class', 'name'})[0].attrs['href'].split('/')[-1]

        # 如果数据库不存在该视频UP主，则加入该UP主
        if not isExistAuthor(uid):
            parserAuthorInfo(uid)

        gv = GetVideo(avId)
        gv.getVideoBaseInfo()
        gv.getVideoArchiveInfo()

        sql = gv.getInsertSQLCode()
        cursor.execute(sql)
        conn.commit()


def closeDB():
    global conn, cursor
    conn.close()
    cursor.close()

if __name__ == '__main__':

    url = 'http://www.bilibili.com/video/av'

    input('使用必看：使用本爬虫之前,请手动修改程序开头处的数据库连接语句,确认正确无误后,按Enter键继续')

    avId = input('\n提示:请输入AV号:')

    parserVideoInfo(url, avId)

    closeDB()
# os.system('pause')


# https://space.bilibili.com/ajax/member/getSubmitVideos?mid=7&pagesize=30&tid=0&page=1&keyword=&order=pubdate