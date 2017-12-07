# BilibiliCrawler
- crawl bilibili user info and video info for data analysis
- 爬取哔哩哔哩up主信息和up主投稿视频信息，用作数据处理
- 采取了一定的反反爬策略

## 快速开始
1. 拉取项目, git clone https://github.com/cgDeepLearn/BilibiliCrawler.git
2. 进入项目主目录，安装虚拟环境crawlenv(请参考使用说明里的虚拟环境安装)
3. 激活环境并在主目录运行crawl,爬取结果将保存在data目录csv文件中
```python
source activate crawlenv
python crawl_user.py file 1 100  # file是数据保存方式，1 100是开始、结束bilibili的uid
```

## 使用说明
1. 拉取项目, git clone https://github.com/cgDeepLearn/BilibiliCrawler.git

2. 进入项目主目录， 安装虚拟环境
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

3. 修改配置文件
