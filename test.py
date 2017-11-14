"""
test func
"""


import pandas as pd
from getuserinfo import GetUser, get_uinfo
from getvideoinfo import GetVideo, get_vinfo

def simple(uid, vid):
    print("uid_info:\n", get_uinfo(uid))
    print("vid_info:\n", get_vinfo(vid))

if __name__ == '__main__':
    simple(74997410, 16262268)
