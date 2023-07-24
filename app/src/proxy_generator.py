# proxy_generator.py

import os
import json
import aiohttp
import asyncio
import aiofiles

from aiohttp_socks import ProxyConnector

# Custom imports
from general_methods import gm
from general_methods import web_gm as wgm
from general_methods import files_gm as fgm


class ProxyGenerator:

	def __init__(
		self, 
		test_url, 
		limit=500, 
		protocols=None, 
		save_path="./proxies.txt", 
		rewrite_key=True,
		remove_after=True, 
		timeout=20
	):
		"""
			:param limit: int
				TODO: page
			:param protocols: list of string 	| ['http', 'https', 'socks4', 'socks5']; all if None
			:param save_path: str 				| where to save result (good proxies)
			
		"""
		self.test_url = test_url
		self.limit = limit
		self.protocols = protocols
		self.save_path = save_path
		self.timeout = timeout
		self.rewrite_key = rewrite_key

		self.result_proxy_list = None

		# Result proxy list
		gm.PrintMode.info("Obtaining valid proxies")
		self.get_first_good_proxies()
		if len(self.result_proxy_list) > 0:
			if self.result_proxy_list[-1] in ['', " ", "\n", "\r", None]:
				self.result_proxy_list = self.result_proxy_list[:-1]

		# Remove temp file
		if remove_after:
			if os.path.exists(save_path):
				gm.PrintMode.info("Remove file:", save_path)
				os.remove(save_path)
		else:
			gm.PrintMode.info("Proxy list saved to:", save_path)

	def get_first_good_proxies(self, attempts=10):

		for page_index in range(1, attempts + 1):
			gm.PrintMode.info(f"Page: {str(page_index):>3}")

			# Good proxy list
			good_pl = self.get_proxies_one_page(page=page_index)

			if len(good_pl) < 5:
				continue
			else:
				self.result_proxy_list = good_pl
				break 

	def get_proxies_one_page(self, page):

		gm.PrintMode.info("Get raw proxies")
		raw_proxy_list = self.get_raw_proxy_list(page=page)
		proxy_list = self.parse_proxy_json(raw_proxy_list)

		gm.PrintMode.info(f"Test proxies")
		asyncio.run(self.proxy_test(proxy_list))

		return self.get_good_proxy_list()

	def get_raw_proxy_list(self, page=1):
		"""
			:param page: int
		"""
		url = f'https://proxylist.geonode.com/api/proxy-list'
		params = {
			'limit': self.limit,
			'page': page,
			'sort_by': "lastChecked",
			'sort_type': "desc",
		}
		if self.protocols is not None:
			params.update({"protocols": ",".join(self.protocols)})
		
		return json.loads(wgm.get_response_text(url, params=params))["data"]

	def parse_proxy_json(self, raw_proxy_list):

		proxy_list = []
		for proxy_item in raw_proxy_list:

			# socks5://user:password@127.0.0.1:1080
			port = proxy_item['port']
			ip = proxy_item['ip']
			protocol = proxy_item['protocols'][-1]

			proxy = f'{protocol}://{ip}:{port}'
			proxy_list.append(proxy)

		return proxy_list

	async def proxy_test_task(self, test_url, connector, proxy):

		try:
			async with aiohttp.ClientSession(connector=connector, timeout=self.timeout) as session:
				async with session.get(url=test_url, timeout=self.timeout) as response:
					if response.status < 400:
						gm.PrintMode.info(f'Succeed: {proxy}')

						async with aiofiles.open(self.save_path, mode='a') as f:
							await f.write(proxy + "\n")					

		except Exception as _ex:
			pass
			gm.PrintMode.error(_ex)

	async def proxy_test(self, proxy_list):

		if not os.path.exists(self.save_path) or self.rewrite_key:
			async with aiofiles.open(self.save_path, mode='w') as f:
				pass

		proxy_iterator = gm.UrlIterator(proxy_list, 175)
		for proxy_part, part_index in zip(proxy_iterator, range(1, proxy_iterator.parts + 1)):
			gm.PrintMode.info(f"part {str(part_index):>2}/{proxy_iterator.parts} "
							  f"({len(proxy_part)} proxies) on URL: {self.test_url}")
			tasks = []
			for proxy in proxy_part:
				connector = ProxyConnector.from_url(proxy)
				task = self.proxy_test_task(self.test_url, connector, proxy)
				tasks.append(task)

			await asyncio.gather(*tasks)

	def get_good_proxy_list(self):
		return fgm.text_read(self.save_path).split('\n')


	if __name__ == '__main__':

		test_url = 'https://rss.app/rss-feed'
		gen = ProxyGenerator(test_url, protocols=['socks4', 'socks5'])

		print(gen.result_proxy_list)