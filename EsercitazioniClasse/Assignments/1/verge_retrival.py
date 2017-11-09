'''
First Assignment part A module: Data Retrival.

a.1)    I've choosen www.theverge.com for my crawling. The Verge is a Tech-centric news site quite popular.
        It has an archive section of the site where I will retrive the URLs for the news. The archive
        URL is: https://www.theverge.com/archives.

        Each archive page has 10 news previews at date 2 November 2017.
'''

from bs4 import BeautifulSoup
from pathlib import Path
import urllib.request
import urllib.error
import time

##############################################################################
#                             Private Utilities                              #
##############################################################################

def _save_to_path(string_content, path = './dummy_save'):
    with open(file=path, mode='w', encoding='utf-8') as fout:
        print(string_content, file=fout)

def _page_downloader(url, page_path, cache_folder='./cached/', ignore_cache=False):
    import os

    def _downloader(url):
        with urllib.request.urlopen(url) as response:
            return response.read()

    def _cache(cache_path):
        content = None
        try:
            Path(cache_path).resolve()
        except FileNotFoundError:
            return content;
        else:
            with open(cache_folder, mode='r', encoding='utf-8') as fin:


    os.makedirs(cache_folder, exist_ok=True)
    cache_path = cache_folder + '{}'.format(url.replace("/", "_"))

    if ignore_cache:


def _article_downloader(url, article_path):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        article_content = _article_parser(html)
        #print('Article Content Extracted : {}\n{}'.format(article_content, '###' * 80))
        _save_to_path(article_content, path=article_path)
    return article_content

def _article_parser(html_string):
    from lxml import html
    content = ''
    soup = BeautifulSoup(html_string, 'html.parser')
    for _content_tag in soup.find_all('div', 'c-entry-content'):
        tree = html.fromstring(_content_tag.__str__())
        for bad in tree.xpath("//script"):
            bad.getparent().remove(bad)
        extracted = tree.text_content()
        content += ' ' + extracted.replace('\n', '').replace('\r','')
    return content

##############################################################################
#                              Module Functions                              #
##############################################################################

def news_urls_retriver(limit = 1000):
    '''
    Saves into out_dir_path the news from The Verge Archive
    :param limit: maximum number of news to save into the output directory.
    :return: list of news URLs
    '''
    NEWS_ARCHIVE_PATH = 'https://www.theverge.com/archives/{}'
    news = set()
    flag = False
    index = 1
    while(len(news) < limit and not flag):
        try:
            with urllib.request.urlopen(NEWS_ARCHIVE_PATH.format(index)) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
                for article in soup.find_all('li', 'p-basic-article-list__node'):
                    news.add(article.find('div', 'body').find('h3').find('a')['href'])
                    index += 1
                time.sleep(1)
        except urllib.error.HTTPError as e:
            print('HTTP ERROR! {}'.format(e.info()))
            flag = True
    return [x for x in news][:limit]

def news_articles_retriver(urls, force_download=False):
    import os
    NEWS_DIR_PATH = './news/{}'
    os.makedirs(NEWS_DIR_PATH.format(''), exist_ok=True)
    articles = []
    for url in urls:
        article_path = NEWS_DIR_PATH.format(url.replace('/', '_'))
        article_file = Path(article_path)
        if not force_download:
            try:
                article_abs_path = article_file.resolve()
            except FileNotFoundError:
                    article_content = _article_downloader(url, article_path)
                    articles.append(article_content)
            else:
                with open(file=article_path, mode='r', encoding='utf-8') as fin:
                    articles.append(''.join(fin.readlines()))
        else:
            articles.append(_article_downloader(url, article_path))
    return articles

##############################################################################
#                                Testring Area                               #
##############################################################################

test = news_urls_retriver(100)
news_articles_retriver(test, force_download=True)

