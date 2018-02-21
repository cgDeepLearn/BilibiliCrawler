# BilibiliCrawler
- crawl bilibili user info and video info for data analysis。
- 爬取部分哔哩哔哩up主信息和up主投稿视频信息，用作数据处理与分析学习(不得用于商业和其他侵犯他人权益的用途)。
- 采取了一定的反反爬策略。
- Bilibili更改了用户页面的api, 用户抓取解析程序需要重构。

## 快速开始
1. 拉取项目, git clone https://github.com/cgDeepLearn/BilibiliCrawler.git
2. 进入项目主目录，安装虚拟环境crawlenv(请参考使用说明里的虚拟环境安装)。
3. 激活环境并在主目录运行crawl,爬取结果将保存在data目录csv文件中。
```python
source activate crawlenv
python initial.py file  # 初始化file模式
python crawl_user.py file 1 100  # file模式，1 100是开始、结束bilibili的uid
进入data目录查看抓取的数据，是不是很简单！
```

- 如果需要使用数据库保存和一些其他的设置，请看下面的使用说明

## 使用说明
### 1. 拉取项目,
```
git clone https://github.com/cgDeepLearn/BilibiliCrawler.git
```

### 2. 进入项目主目录， 安装虚拟环境
- 若已安装anaconda
```python
conda create -n crawlenv python=3.6
source activate crawlenv  # 激活虚拟环境
pip install -r requirements.txt
```
- 若使用virtualenv
```python
virtualenv crawlenv
source crawlenv/bin/activate  # 激活虚拟环境，windows下不用source
pip install -r requirements.txt  # 安装项目依赖
```

### 3. 修改配置文件
- 进入config目录，修改config.ini配置文件(默认使用的是postgresql数据库，如果你是使用的是postgresql，只需要将其中的参数替换成你的，下面其他的步骤可以忽略)
数据库配置选择其中一个你本地安装的即可，将参数更换成你的
如果你需要更自动化的数据库配置，请移步我的[DB_ORM](https://github.com/cgDeepLearn/DB_ORM)项目
```yaml
[db_mysql]
user = test
password = test
host = localhost
port = 3306
dbname = testdb

[db_postgresql]
user = test
password = test
host = localhost
port = 5432
dbname = testdb
```
- 然后修改conf.py中获取配置文件的函数
```python
def get_db_args():
    """
    获取数据库配置信息
    """
    return dict(CONFIG.items('db_postgresql'))  # 如果安装的是mysql,请将参数替换为db_mysql
```
- 进入db目录，修改basic.py的连接数据库的DSN
```python
# connect_str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(kwargs['user'], kwargs['password'], kwargs['host'], kwargs['port'], kwargs['dbname'])
# 若使用的是mysql，请将上面的connect_str替换成下面的
connect_str = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(kwargs['user'], kwargs['password'], kwargs['host'], kwargs['port'], kwargs['dbname'])
# sqlite3，mongo等请移步我的DB_ORM项目，其他一些数据库也将添加支持
```

### 4. 运行爬虫
- **在主目录激活虚拟环境， 初次运行请执行**
```python
python initial.py db # db模式，file模式请将db换成file
# file模式会将抓取结果保存在data目录
# db模式会将数据保存在设置好的数据库中
# 若再次以db模式运行将会drop所有表后再create，初次运行后请慎重再次使用!!!
# 如果修改添加了表，并不想清空数据，请运行 python create_all.py
```
- **开始抓取示例**
```python
python crawl_user.py db 1 10000 # crawl_user 抓取用户数据，db 保存在数据库中， 1 10000为抓取起止id
python crawl_video_ajax.py db 1 100 # crawl_video_ajax 抓取视频ajax信息保存到数据库中,
python crawl_user_video.py db 1 10000 #同时抓取user 和videoinfo
# 示例为uid从1到100的user如果有投稿视频则抓取其投稿视频的信息，
# 若想通过视频id逐个抓取请运行python crawl_video_by_aid.py db 1 1000
```

- **爬取速率控制**

程序内已进行了一些抓取速率的设置，但各机器cpu、mem不同抓取速率也不同，请酌情修改\
太快太慢请修改各crawl中的sleepsec参数,ip会被限制访问频率，overspeed会导致爬取数据不全，\
之后会添加运行参数speed(high, low),不用再手动配置速率

- **日志**

爬取日志在logs目录\
user, video分别为用户和视频的爬取日志\
storage为数据库日志
如需更换log格式，请修改logger模块

- **后台运行**

linux下运行python ......前面加上nohup，例如:
```python
nohup python crawl_user db 1 10000
```
程序输出保存文件，默认会包存在主目录额nohup.out文件中，添加 > fielname就会保存在设置的文件中:
```python
nohup python crawl_video_ajax.py db 1 1000 > video_ajaxup_1_1000.out  # 输出将保存在video_ajaxup_1_1000.out中
```

- **更多**
程序多线程使用的生产者消费者模式中产生了程序运行的状况的打印信息，类似如下
```python
produce 1_1
consumed 1_1
...
```
如想运行更快，请在程序各项设置好后注释掉其中的打印程序
```python
# utils/pcModels.py
print('[+] produce %s_%s' % (index, pitem))  # 请注释掉

print('[-] consumed %s_%s\n' % (index, data))  # 请注释掉
```

## 更多
项目是单机多线程，若想使用分布式爬取，请参考[Crawler-Celery](https://github.com/cgDeepLearn/BiliCrawler-Celery)
