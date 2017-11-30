import configparser
import os
import random

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_PATH)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA_PATH = os.path.join(os.path.dirname(__file__), 'user_agents.txt')

def get_db_args():
    """
    获取数据库配置信息
    """
    return dict(CONFIG.items('db_postgresql'))

def get_user_agents(filename=UA_PATH):
    ualist = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line:
                ualist.append(line.strip()[1: -1])
    random.shuffle(ualist)
    return ualist

def get_proxies():
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
    return proxies

def get_urls(urlkey):
    return CONFIG.get('bili_url', urlkey)

def get_key():
    return CONFIG.get('bili_key', 'key')
