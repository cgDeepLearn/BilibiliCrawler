"""
bilibili support
"""

from datetime import datetime


def get_timestamp():
    # 返回毫秒数
    return int(round(datetime.now().timestamp() * 1000))

