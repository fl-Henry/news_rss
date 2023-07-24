# app.py
import os

from sys import exit as sx
from lxml import html
from bs4 import BeautifulSoup

# https://pypi.org/project/trafilatura/
from trafilatura import fetch_url, extract

# Custom imports
from proxy_generator import ProxyGenerator
from general_methods import files_gm as fgm
from general_methods import gm


dh = fgm.DirectoriesHandler()


def set_dirs():
	dh.dirs.update(
		{
			"db_data": dh.db_data,
			"temp": dh.temp,
		}
	)

	dh.dirs_to_remove.update(
		{
			"temp": dh.temp,
		}
	)

	print(dh)
	print()


def append_proxies(test_url, update=False):
	proxies_filepath = "./proxies.txt" 
	if not os.path.exists(proxies_filepath) or update:
		gen = ProxyGenerator(
			test_url, 
			protocols=['https', 'socks4', 'socks5'], 
			rewrite_key=True, 
			remove_after=False
		)
	else:
		saved_proxies = fgm.text_read(proxies_filepath).split('\n')
		if len(saved_proxies) < 5:
			gen = ProxyGenerator(
				test_url, 
				protocols=['https', 'socks4', 'socks5'], 
				rewrite_key=False, 
				remove_after=False
			)
		else:
			return saved_proxies


def get_feed_url_json():
	feed_url_filepath = "./feed_url_list.txt" 
	feed_url_list = fgm.text_read(feed_url_filepath).split("\n")
	feed_url_json = [
		{
			"base_url": x.split(" ")[0], 
			"feed_url": x.split(" ")[1], 
		}
		for x in feed_url_list if x not in gm.EMPTY
	]
	return feed_url_json
	

def get_feed_url(url):
	feed_url_json = get_feed_url_json()
	for feed_url_item in feed_url_json:
		if feed_url_item['base_url'] == url:
			return feed_url_item['feed_url']
	return None


def start_app():
	set_dirs()

	# Get Proxies
	test_url = 'https://rss.app/rss-feed'
	append_proxies(test_url)


	# Create RSS feed
	url = 'https://apnews.com/world-news'
	# os.system(f"node rss_news.js --url {url} --feed-url")

	# Get feed_url for url (news url)
	feed_url = get_feed_url(url)

	# Fetch news urls
	url = 'https://apnews.com/world-news'
	os.system(f"node rss_news.js --url {url} --new-feed")


def start_test():
	gm.PrintMode.debug("Test Mode")
	set_dirs()

	# Get Proxies
	test_url = 'https://ipfighter.com/'
	gen = ProxyGenerator(test_url, protocols=['socks4', 'socks5'], remove_after=False)

	# Create RSS feed
	gm.PrintMode.debug("node rss_news.js --test")
	os.system(f"node rss_news.js --test")


if __name__ == '__main__':
	start_app()
	# start_test()
