import time
import csv
import random
from multiprocessing.dummy import Pool as ThreadPool
from getuserinfo_v2 import BiliUser

def cal(num):
    try:
        print(num*num)
        time.sleep(1)
    except:
        pass
    return num

def test():
    NUMS = list(range(1,10))

    pool = ThreadPool(10)

    try:
        results = pool.map(cal, NUMS)
    except Exception as e:
        print(e)
        time.sleep(10)
        results = pool.map(cal, NUMS)

    pool.close()
    pool.join()
    print(results)

def get_info(mid):
    gu = BiliUser(mid)
    info = gu.getUserInfo()
    # gu.getUserInfo()
    # print(mid, gu.info)
    # return gu.info
    #time.sleep(1)
    return info


def go_get(start, end):
    NUMS = list(range(start, end))
    pool = ThreadPool(4)
    try:
        results = pool.map(get_info, NUMS)
    except Exception as e:
        print(e)
        time.sleep(100)
        results = pool.map(get_info, NUMS)
    pool.close()
    pool.join()

    with open('uinfo/uinfo_test.csv', 'a', encoding='utf8', newline='') as f:
        for result in results:
            if result:
                csvwriter = csv.writer(f)
                csvwriter.writerow(result)
    

if __name__ == '__main__':
    #test()
    start, end, step = 1, 10000, 100
    for loop in range(start, end, step):
        go_get(loop, loop + step)
        secs = round(random.uniform(15, 25), 2)  # 随机休息时间间隔
        time.sleep(secs)