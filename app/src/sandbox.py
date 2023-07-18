    import os
    import requests

    from trafilatura import fetch_url, extract, feeds
    from lxml import html
    from bs4 import BeautifulSoup

    # Custom imports
    from general_methods import gm
    from general_methods import web_gm as wgm
    from general_methods import files_gm as fgm


    def get_feeds(url):
        print(feeds.find_feed_urls(url))


    def get_body(filepath):
        my_doc = fgm.text_read(filepath)
        soup = BeautifulSoup(my_doc, "lxml")

        # body = soup.select_one("body")
        body = soup

        for s in body.select('script'):
            s.extract()

        for s in body.select('style'):
            s.extract()

        print(body.get_text(separator="\n"))
        fgm.text_rewrite("./result_body.txt", str(body))


    def trfl_extract(filepath):
        my_doc = fgm.text_read(filepath)
        mytree = html.fromstring(my_doc)
        result = extract(
            mytree,
            # include_links=True,
            # include_formatting=False,
            # include_tables=True,
            # no_fallback=True,
            # favor_recall=True,
            # include_comments=True,
            deduplicate=True
        )
        fgm.text_rewrite("result_trfl.txt", result)


    def trfl_request(url):
        downloaded = fetch_url(url)
        if downloaded is None:
            print(downloaded)

        result = extract(downloaded)
        fgm.text_rewrite("result_trfl_01.txt", result)


    def common_parse(url):
        response = requests.get(url).text
        fgm.text_rewrite("./result_common.txt", response)


    if __name__ == '__main__':
        url = 'https://rss.app/feed/Kjj5l7ZeCvz3rn4V'
        # url = 'https://rss.app/feed/8tPpg2g5IQ1YqHSB'

        url = 'https://www.aljazeera.com/news/2023/7/14/guatemala-prosecutor-denies-aiming-to-interfere-with-elections'
        url = 'https://apnews.com/article/flash-flooding-pennsylvania-deaths-c0b3fc0c9c3e40b4cd33c8dc0ad50c14'
        url = 'https://www.reuters.com/world/chinas-response-not-encouraging-g20-common-framework-debt-source-2023-07-16/'
        # common_parse(url)
        # os.system(f"node rss_news.js --url {url}")
        # get_body("result_common_rendered.txt")
        # trfl_extract("result_body.txt")
        trfl_request(url)
        