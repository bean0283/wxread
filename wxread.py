# 小小檬阅读 
# 微信入口：https://rk0530232320-1318315264.cos.ap-nanjing.myqcloud.com/index.html?upuid=11675699
# 环境变量名read,
#微信抓包上面链接的cookie，复制cookie全部
# 定时 15 8-23 * * *
# 多账号换行，推荐换个人UA
# 每天开始手动阅读三篇
# 黑号不负责

import json
import os,sys 
import random
import re
import time
import requests
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir) 

default_ua = 'Mozilla/5.0 (Linux; Android 11; MEIZU 18s Build/RKQ1.210614.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5075 MMWEBSDK/20230202 MMWEBID/503 MicroMessenger/8.0.33.2320(0x28002151) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64'

read_ck = os.getenv('read')
#ck = read_ck.split('&')
ck = ["填写你的ck"]

site_url = 'https://m.cdcd.plus/tuijian'

message = ""
def struct_headers(referurl):
	headers = {
		'Host': 'm.cdcd.plus',
		'Connection': 'keep-alive',
		'Accept': 'application/json, text/plain, */*',
		'User-Agent': default_ua,
		'Accept-Language': 'zh-CN,zh',
		'Accept-Encoding': 'gzip, deflate',
		'Origin': referurl,
		'Referer': referurl,
		'Sec-Fetch-Site': 'cross-site',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Dest': 'empty',
		'X-Requested-With': 'XMLHttpRequest'
	}
	# print(headers)
	return headers


class UserInfo():
	message = ''
	ck = ''
	iu = ''
	referURL = ''
	jkey = ''
	uid = ''
	upuid = ''
	rootUrl = ''
	rest = ''


	def __init__(self, myck):
		self.ck = myck
		self.message = ''

	def get_userInfo(self):

		try:
			url = f'{self.rootUrl}/tuijian'
			temp_host = re.findall('http://(.*?)/', url)[0]
			headers = {
				'Host': temp_host,
				'Connection': 'keep-alive',
				'Accept': 'application/json, text/plain, */*',
				'User-Agent': default_ua,
				'Accept-Language': 'zh-CN,zh',
				'Accept-Encoding': 'gzip, deflate',
				'Cookie': self.ck
			}
			res = requests.get(url=url, headers=headers)

			json_obj = json.loads(res.text)
			status = json_obj['data']['infoView']['status']
			self.rest = json_obj['data']['infoView']['rest']
			self.upuid = json_obj['data']['user']['upuid']
			self.uid = json_obj['data']['user']['uid']
			if 'msg' in json_obj['data']['infoView']:
				print(json_obj['data']['infoView']['msg'],flush=True)
				self.message += json_obj['data']['infoView']['msg']
                
			return status
		except Exception:
			
			print(Exception)
			self.message += str(Exception)

	def get_new_id(self):
		try:
			url = 'https://m.cdcd.plus/entry/new_ld'
			headers = {
				'Host': 'm.cdcd.plus',
				'Connection': 'keep-alive',
				'User-Agent': default_ua,
				'Accept': '*/*',
				'Accept-Language': 'zh-CN,zh',
				'Accept-Encoding': 'gzip, deflate',
				'Sec-Fetch-Site': 'cross-site',
				'Sec-Fetch-Mode': 'cors',
				'Sec-Fetch-Dest': 'empty',
			}
			res = requests.get(url=url, headers=headers)
			#print(res)
			json_obj = json.loads(res.text)
			self.rootUrl = re.findall('(.*?)/new', json_obj['jump'])[0]
		except Exception:
			print(Exception,flush=True)
			self.message += str(Exception)


	def get_read_url(self):

		try:
			url = f'{self.rootUrl}/new/get_read_url'
			temp_host = re.findall('http://(.*?)/', url)[0]
			headers = {
				'Host': temp_host,
				'Connection': 'keep-alive',
				'Accept': 'application/json, text/plain, */*',
				'Referer': f'{self.rootUrl}/new?upuid={self.upuid}',
				'User-Agent': default_ua,
				'Accept-Language': 'zh-CN,zh',
				'Accept-Encoding': 'gzip, deflate',
				'Cookie': self.ck
			}
			res = requests.get(url, headers=headers)

			json_obj = json.loads(res.text)
			temp_url = json_obj['jump']
			print(temp_url)

			self.referURL = re.findall('(.*?)/read', temp_url)[0]
			self.iu = temp_url[temp_url.rfind('iu=') + 3:]
			print(self.referURL)
			print(self.iu)

		except Exception:
			print(Exception,flush=True)
			self.message += str(Exception)


	def goto_read(self, r):
		try:
			# r = random.random()
			url = site_url + f'/do_read?iu={self.iu}&for&zs&pageshow&r={r}'
			headers = struct_headers(self.referURL)
			res = requests.get(url=url, headers=headers)
			json_obj = json.loads(res.text)
			self.jkey = json_obj['jkey']

			if 'url' in json_obj:
				return json_obj['url']  # 返回文章地址
			else:
				exit(-1)
		except Exception:
			print(Exception)
			self.message += "阅读失败"

	def finish_read(self, r):
		try:
			url = site_url + f'/do_read?iu={self.iu}&for&zs&pageshow&r={r}&jkey={self.jkey}'
			headers = struct_headers(self.referURL)
			res = requests.get(url=url, headers=headers)
			json_obj = json.loads(res.text)
			msg = json_obj['success_msg']
			self.jkey = json_obj['jkey']
			if '250' in msg and 'url' in json_obj:
				print(msg,flush=True)
				self.message += msg
				self.message += "\n"
				return json_obj['url']  # 返回文章地址
			else:
				print('阅读受限，停止阅读')
				self.message += '阅读受限，停止阅读'
				exit(-1)
		except Exception:
			print(Exception)
			self.message += str(Exception)


	def find_withdraw(self):
		try:
			url = f'{self.rootUrl}/withdrawal'
			temp_host = re.findall('http://(.*?)/', url)[0]
			headers = {
				'Host': temp_host,
				'Connection': 'keep-alive',
				'Accept': 'application/json, text/plain, */*',
				'Referer': f'{self.rootUrl}/new?upuid={self.upuid}',
				'User-Agent': default_ua,
				'Accept-Language': 'zh-CN,zh',
				'Accept-Encoding': 'gzip, deflate',
				'Cookie': self.ck
			}
			res = requests.get(url=url, headers=headers)
			json_obj = json.loads(res.text)

			if 'score' in json_obj['data']['user']:
				score = json_obj['data']['user']['score']
				score = float(score)
				print('当前:%.3f元' % (score * 0.01),flush=True)
				self.message += '当前:%.3f元' % (score * 0.01)
				return int(score)
			return 0
		except Exception:
			print(Exception.args)
			self.message += Exception.args

	def withdraw(self, withdrawNum):
		try:
			url = f'{self.rootUrl}/withdrawal/doWithdraw'
			temp_host = re.findall('http://(.*?)/', url)[0]
			headers = {
				'Host': temp_host,
				'Connection': 'keep-alive',
				'Accept': 'application/json, text/plain, */*',
				'Referer': f'{self.rootUrl}/new?upuid={self.upuid}',
				'User-Agent': default_ua,
				'Accept-Language': 'zh-CN,zh',
				'Accept-Encoding': 'gzip, deflate',
				'Cookie': self.ck,
				'Content-Type': 'application/x-www-form-urlencoded'
			}
			data = f'amount={withdrawNum}'
			res = requests.post(url=url, headers=headers, data=data)

			json_obj = json.loads(res.text)
			code = json_obj['code']
			if code == 0:
				print(f'已提现{withdrawNum * 0.01}',flush=True)
				self.message += f'已提现{withdrawNum * 0.01}'
				self.message += "\n"
			else:
				print('提现失败',flush=True)
				self.message += '提现失败'

		except Exception:
			print(Exception.args)
			self.message += Exception.args

	def retmsg(self):
		return self.message      
  
# formatTime = time.strftime("%m%d%H%M", time.localtime())
print('=============开始运行==============')
print('当前共{userLen}个账号'.format(userLen=len(ck)))
message+= '当前共{userLen}个账号'.format(userLen=len(ck))
message += "\n"
for index, userInfo in enumerate(ck):
	print('===============账号{i}==============='.format(i=index + 1))
	message += '===============账号{i}==============='.format(i=index + 1)
	cur_user = UserInfo(ck[index])
	cur_user.get_new_id()
	print(cur_user.rootUrl)
	if cur_user.get_userInfo() != 1:
		continue
	cur_user.get_read_url()
	if int(cur_user.rest != 0):
		for i in range(int(cur_user.rest)):
			r = round(random.random(), 16)
			time.sleep(random.uniform(1, 2))
			if i == 0:
				# 第一次获取到文章
				article_url = cur_user.goto_read(r)
				article_url = article_url[:article_url.rfind('#wechat')]
				res = requests.get(article_url)
				time.sleep(8 + random.uniform(0, 2))  # 等待
			# 第一次阅读完成，返回第二次文章链接
			article_url = cur_user.finish_read(r)
			if article_url is None:
				break
			article_url = article_url[:article_url.rfind('#wechat')]
			res = requests.get(article_url)
			time.sleep(8 + random.uniform(0, 2))  # 等待
	score = cur_user.find_withdraw()
	if int(score) >= 30:
		cur_user.withdraw(score)
	message += cur_user.retmsg()
	message += '\n'
	

