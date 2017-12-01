# -*- coding: utf-8 -*-
"""
get  Bilibili Video Info
"""
import json
import random
import requests
from config import get_user_agents, get_urls, get_key
from logger import bilivideolog
from db import BiliVideoInfo, DBOperation
from .support import get_timestamp


class BiliVideo():
    """通过uid获取Bilibili Video Info"""
    field_keys = ('mid','aid','tid','cid','typename','arctype','title','pic','pages','created',
                    'view','danmaku','reply','favorite','coin','share',
                    'now_rank','his_rank','like','no_reprint','copyright')

    def __init__(self, aid):
        """
        aid: video id
        -----info format-----:
        ('mid','aid','tid','cid','typename','arctype','title','pic','pages','created') +
        ('view','danmaku','reply','favorite','coin','share',
        'now_rank','his_rank','like','no_reprint','copyright')
        """
        self.aid = aid
        self.info = None
    
    def getBasicInfo(self):
        url = get_urls('url_view')
        timestamp_ms = get_timestamp()
        appkey = get_key()
        UAS = get_user_agents()
        params = {'type':'json','appkey': appkey, 'id': str(self.aid), '_': '{}'.format(timestamp_ms)}
        headers = {'User-Agent': random.choice(UAS)}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
        except Exception as e:
            # print(e)
            msg = 'aid({}) get error'.format(self.aid)
            bilivideolog.error(msg)
            return None
        data = json.loads(res.text)
        if 'mid' in data:
            # ('mid','aid','tid','cid','typename','arctype','title','pic','pages','created')
            related_info = ( data['mid'], self.aid,  data['tid'],
                         data['cid'], data['typename'], data['arctype'],
                         data['title'], data['pic'],
                         data['pages'], data['created'])
            return related_info

        else:
            msg = 'aid({}) request code return error'.format(self.aid)
            bilivideolog.info(msg)
            return None
    

    def getAjaxInfo(self):
        """获取视频ajax信息"""
        url = get_urls('url_stat')
        timestamp_ms = get_timestamp()
        UAS = get_user_agents()
        params = {'aid': str(self.aid), '_': '{}'.format(timestamp_ms)}
        headers = {'User-Agent': random.choice(UAS)}

        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
        except Exception as e:
            # print(e)
            msg = 'aid({}) get error'.format(self.aid)
            bilivideolog.error(msg)
            return None
        text = json.loads(res.text)
        if text['code'] == 0:
            data = text['data']
            ajax_info = (data['view'], data['danmaku'],
                         data['reply'], data['favorite'], data['coin'],
                         data['share'], data['now_rank'], data['his_rank'],
                         data['like'], data['no_reprint'], data['copyright'])
            return ajax_info

        else:
            msg = 'aid({}) request code return error'.format(self.aid)
            bilivideolog.info(msg)
            return None
    
    @classmethod
    def getVideoInfo(cls, aid):
        """获取视频全部信息"""
        info_basic = cls(aid).getBasicInfo()
        info_ajax = cls(aid).getAjaxInfo()
        try:
            info = info_basic + info_ajax
        except Exception:
            info = None
        return info

    @classmethod
    def store_video(cls, aid, session=None, csvwriter=None):
        """session, csvwriter 二选一都没有直接打印"""
        info = cls.getVideoInfo(aid)
        if info:
            new_video = BiliVideoInfo(**dict(zip(cls.field_keys, info)))
            if session:
                DBOperation.add(new_video, session)
                return True
            elif csvwriter:
                csvwriter.writerow(info)
                return True
            else:
                print(info)
                return True
        else:
            return False


