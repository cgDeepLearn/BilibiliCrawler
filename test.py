"""
test func
"""


import pandas as pd
from getuserinfo import GetUser, get_uinfo
from getvideoinfo import GetVideo, get_vinfo

# df = pd.read_csv('biliup_info_10000.csv',names=['uid','author','gender','sign','fans','watch','regtime','birth','addr','icon','vnum'])
# dt = datetime.strptime(a, '%a %b %d %H:%M:%S %Y')
# df.drop(['icon'], axis=1)
# df['addr'].str.split(' ').str.get(0).value_counts() # 获取省份
# df['birth'].str.replace('0000-','') # 生日
#from dateutil.parser import parse
# df['regtime'].apply(parse) # 转为datetime,注意有0的数据，即注册时间未填写的
# df['regtime'].replace(['0'], np.nan).ffill().parse() # 前向插值再转换

def simple(uid, vid):
    print("uid_info:\n", get_uinfo(uid))
    print("vid_info:\n", get_vinfo(vid))

if __name__ == '__main__':
    simple(74997410, 16262268)
