# BilibiliCrawler
- crawl bilibili user info and video info for data analysis
- 爬取哔哩哔哩up主信息和up主投稿视频信息，用作数据处理
- 采取了一定的反反爬策略

## 使用说明
1. git clone 拉取项目

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