# -*- coding: utf-8 -*-
"""bilibili user api"""

import os
import json
import random
import time
import requests
from config import get_user_agents, get_urls
from logger import biliuserlog
from db import BiliUserInfo, BiliVideoList, DBOperation
from .support import get_timestamp


class BiliUser():
    """通过uid获取Bilibili User Info

    uid: user id
    -----info format-----:
    ("mid","name","approve","sex",--"face","DisplayRank","regtime","spacesta","birthday",
        "place",--"description","article","fans","attention",--"sign","level","verify","vip")
    face, description, sign 并未保存到数据库
    """
    field_keys = ("mid", "name", "approve", "sex", "displayrank", "regtime", "spacesta", "birthday",
                  "place", "article", "fans", "attention", "level", "verify", "vip")
    json_keys = ()

    @classmethod
    def getUserInfo(cls, uid):
        url = get_urls('url_user')
        timestamp_ms = get_timestamp()
        UAS = get_user_agents()
        headers = {'User-Agent': random.choice(UAS)}
        params = {'mid': str(uid), '_': '{}'.format(timestamp_ms)}

        try:
            res = requests.get(url, headers=headers, params=params)
            res.raise_for_status()
            text = json.loads(res.text)
        except Exception as e:
            msg = 'uid({}) get error'.format(uid)
            biliuserlog.error(msg)
            return None

        try:
            if text['code'] == 0:
                data = text['data']['card']

                info = (data['mid'], data['name'],
                        data['approve'], data['sex'],
                        data['DisplayRank'], data['regtime'],
                        data['spacesta'], data['birthday'],
                        data['place'],
                        data['article'], data['fans'],
                        data['attention'],
                        data['level_info']['current_level'],
                        data['official_verify']['type'],
                        data['vip']['vipStatus'])
                return info
            else:
                msg = 'uid({}) request code return error'.format(uid)
                biliuserlog.info(msg)
                return None
        except TypeError:
            msg = 'uid({}) text return None'.format(uid)
            biliuserlog.info(msg)
            return None

    @staticmethod
    def getVideoList(uid):
        url = get_urls('url_submit')
        timestamp_ms = get_timestamp()
        UAS = get_user_agents()
        headers = {'User-Agent': random.choice(UAS)}
        params = {'mid': str(uid), '_': '{}'.format(timestamp_ms)}
        video_num = 0
        video_pages = 0
        try:
            response = requests.get(url, headers=headers, params=params)
            text = json.loads(response.text)
            video_num = text['data']['count']
            video_pages = text['data']['pages']
        except Exception:
            msg = 'user({}) vnum text got error'.format(uid)
            biliuserlog.error(msg)
            return None
        # 没投过稿
        if video_num < 1:
            return None

        def get_aids(url, mid, pages):
            """返回所有aid的序列"""
            vlist = None
            for page in range(1, pages + 1):
                params = {"mid": '{}'.format(mid), "page": '{}'.format(page),
                          '_': '{}'.format(timestamp_ms)}
                try:
                    response = requests.get(
                        url, headers=headers, params=params)
                    text = json.loads(response.text)
                    vlist = text['data']['vlist']
                    for item in vlist:
                        yield(item['aid'])
                except Exception as e:
                    msg = 'uid({}) vlist get error and\n {}'.format(mid, e)
                    biliuserlog.error(msg)
                    return None

                time.sleep(0.1)  # 休息一下

        return get_aids(url, uid, video_pages)

    @classmethod
    def store_user(cls, mid, data, session=None, csvwriter=None):
        """
        mid,data 为生成的queue的里获取的数据，data参数多余为了兼容store_video
        session：
        None：csvwriter
        not None：:ORM"""
        info = cls.getUserInfo(mid)
        if info:
            new_user = BiliUserInfo(**dict(zip(cls.field_keys, info)))
            if session:
                DBOperation.add(new_user, session)
                return True
            elif csvwriter:
                csvwriter.writerow(info)
                return True
            else:
                print(info)
                return True
        else:
            return False
