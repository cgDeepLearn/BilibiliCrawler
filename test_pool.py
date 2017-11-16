import time
import csv
from multiprocessing.dummy import Pool as ThreadPool
from getuserinfo import GetUser


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
    gu = GetUser(mid)
    fans = gu.get_relation()
    # gu.getUserInfo()
    # print(mid, gu.info)
    # return gu.info
    return mid, fans


def main():
    NUMS = list(range(1, 200))
    pool = ThreadPool(10)
    try:
        results = pool.map(get_info, NUMS)
    except Exception as e:
        print(e)
        time.sleep(100)
        results = pool.map(get_info, NUMS)
    pool.close()
    pool.join()

    with open('test.csv', 'w', encoding='utf8', newline='') as f:
        for result in results:
            if result:
                csvwriter = csv.writer(f)
                csvwriter.writerow(result)
    

if __name__ == '__main__':
    #test()
    main()