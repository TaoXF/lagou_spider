# lagou_spider

### 使用依赖
```
pip install requests
pip install pymongo
pip install beautifulsoup4
pip install pygal # 生成svg图片
```
### 使用方式
##### 完善settings.py 当中的基本配置
需要先登录 拉钩 复制下自己的cookie 补充到headers当中 \
需要配置mongodb 的基本信息

```
python3 lagou_spider.py
```
大约一小时左右就能抓取完毕

```
python3 lagou_chart.py
```
生成结果svg 图片

### 最终结果
#### 顶层分类
![顶层分类svg图片](https://github.com/TaoXF/lagou_spider/blob/master/lagou/top_classify.svg)

#### 互联网分类
![互联网分类svg图片](https://github.com/TaoXF/lagou_spider/blob/master/lagou/internet_classify.svg)
