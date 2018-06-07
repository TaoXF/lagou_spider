import time
import requests
import pymongo
import logging; logging.basicConfig(level=logging.INFO)

from pymongo import errors
from bs4 import BeautifulSoup
from settings import MONGO_URL, HEADERS


class LagouSpider(object):

	def __init__(self, mongo_url, headers):
		self.headers = headers
		self.client = pymongo.MongoClient(mongo_url)
		self.db = self.client.scrapy.lagou

	def start(self):
		# 请求首页
		# 启动调度方法

		index_url = 'https://www.lagou.com/'
		classify_list = self.index_pars(self.request_(index_url))
		self.scheduler(classify_list)

	def scheduler(self, classify_list):
		# 调度方法 复制控制请求间隔时间
		# 先请求第一页拿到总页数然后生成剩余页数的请求
		# 调用解析方法 拿到结果 最后调用保存方法
		# 当所有请求结束之后关闭数据库连接

		for classify in classify_list:
			total = self.first_page(classify)
			if total:
				time.sleep(1)
				for i in range(2, int(total)+1):
					url = classify.get('classify_href') + str(i) + '/?filterOption=3'
					soup = BeautifulSoup(self.request_(url), "lxml")
					self.save(self.pars(soup), classify)
					time.sleep(1)

		self.close_spider()

	def request_(self, url):
		# 发起请求的方法 返回页面内容

		logging.info('start request %s' %url)
		response = requests.get(url, headers=self.headers)
		logging.info('status_code is %s' %response.status_code)
		return response.text

	def first_page(self, classify):
		# 请求每个分类的第一页
		# 将数据解析保存之后 并返回总页数

		url = classify.get('classify_href')
		soup = BeautifulSoup(self.request_(url), "lxml")
		self.save(self.pars(soup), classify)

		total_page = soup.select('.totalNum')[0].text
		if int(total_page) > 1:
			return total_page

	def save(self, results, classify):
		# 整理需要保存的数据 并保存到数据库中

		count = 0
		items = []
		for result in results:
			count += 1
			items.append({
				'top_classify': classify.get('top_classify'),
				'second_classify': classify.get('second_classify'),
				'classify_title': classify.get('classify_title'),
				'position': result[0],
				'company': result[1],
				'other': result[2]
			})

			if count > 10:
				try:
					logging.info('inser_item')
					self.db.insert_many(items).inserted_ids
				except errors.BulkWriteError as e:
					logging.error('inser_error')
					logging.error(e)
				finally:
					count = 0
					items = []

	def close_spider(self):
		self.client.close()

	@staticmethod
	def pars(soup):
		# 接受一个soup 进行数据整理 并返回结果

		list_item = soup.select('.con_list_item')
		for item in list_item:
			position = {
				'position_link': item.select('.position_link')[0].attrs['href'],
				'position_title': item.select('.position_link > h3')[0].text,
				'address': item.select('.position_link > .add')[0].text,
				'money': item.select('.p_bot > .li_b_l > .money')[0].text,
				'require': item.select('.p_bot > .li_b_l')[0].text.split('\n')[2]
			}
			company = {
				'company_name': item.select('.company_name > a')[0].attrs['href'],
				'company_link': item.select('.company_name > a')[0].text,
				'industry': item.select('.company > .industry')[0].text.strip(),
			}
			other = {
				'tags': [tags.text for tags in item.select('.list_item_bot > .li_b_l > span')],
				'describe': item.select('.list_item_bot > .li_b_r')[0].text
			}
			yield (position, company, other)

	@staticmethod
	def index_pars(html):
		# 解析首页
		# 进行分类整理 最终返回分类信息

		soup = BeautifulSoup(html, "lxml")
		m_list = soup.select('.menu_box')
		for m in m_list:
			top_classify = m.select('.category-list > h2')[0].text.strip()
			dl_list = m.select('.menu_sub > dl')
			for dl in dl_list:
				second_classify = dl.select('dt > span')[0].text
				a_list = dl.select('dd > a')
				for a in a_list:
					classify_href = a.attrs['href']
					classify_title = a.text
					yield {
						'top_classify': top_classify,
						'second_classify': second_classify,
						'classify_title': classify_title,
						'classify_href': classify_href,
					}


if __name__ == '__main__':
	spider = LagouSpider(MONGO_URL, HEADERS)
	spider.start()

