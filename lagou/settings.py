USER = ''
PWD = ''
DATABASE = ''
PORT = 27017
HOST = 'localhost'

MONGO_URL = "mongodb://{user}:{pwd}@{host}:{port}/{database}".format(
	user=USER, pwd=PWD, host=HOST, port=PORT, database=DATABASE)

HEADERS = {
	'Cookie': 'your cookie',
	'User-Agent': 'your user_agent',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.9',
}