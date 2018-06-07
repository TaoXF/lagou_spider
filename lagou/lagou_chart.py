import pygal
import pymongo
from settings import MONGO_URL


client = pymongo.MongoClient(MONGO_URL)
db = client.scrapy.lagou

# 顶层分类
chart = pygal.Bar()
chart.add('技术', db.find({'top_classify': '技术'}).count())
chart.add('产品', db.find({'top_classify': '产品'}).count())
chart.add('设计', db.find({'top_classify': '设计'}).count())
chart.add('运营', db.find({'top_classify': '运营'}).count())
chart.add('市场与销售', db.find({'top_classify': '市场与销售'}).count())
chart.add('职能', db.find({'top_classify': '职能'}).count())
chart.add('金融', db.find({'top_classify': '金融'}).count())
chart.render_to_file('top_classify.svg')

# 互联网分类
chart2 = pygal.Bar()
chart2.add('后端开发', db.find({'second_classify': '后端开发'}).count())
chart2.add('移动开发', db.find({'second_classify': '移动开发'}).count())
chart2.add('前端开发', db.find({'second_classify': '前端开发'}).count())
chart2.add('人工智能', db.find({'second_classify': '人工智能'}).count())
chart2.add('测试', db.find({'second_classify': '测试'}).count())
chart2.add('运维', db.find({'second_classify': '运维'}).count())
chart2.add('DBA', db.find({'second_classify': 'DBA'}).count())
chart2.add('高端职位', db.find({'top_classify': '技术', 'second_classify': '高端职位'}).count())
chart2.add('项目管理', db.find({'second_classify': '项目管理'}).count())
chart2.add('硬件开发', db.find({'second_classify': '硬件开发'}).count())
chart2.add('企业软件', db.find({'second_classify': '企业软件'}).count())
chart2.render_to_file('internet_classify.svg')
