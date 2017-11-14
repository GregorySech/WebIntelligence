from bs4 import BeautifulSoup
from pathlib import Path
import time
import os
import requests
import logging

#module name
__name__='verge_retrival'

#logging config
logging.basicConfig(filename='verge_retriver.log', level=logging.DEBUG, format='%(levelname)s:%(message)s')

##############################################################################
#                             Private Utilities                              #
##############################################################################

def _save_to_path(string_content, path = './dummy_save'):
    with open(file=path, mode='w', encoding='utf-8') as fout:
        print(string_content, file=fout)

def _page_retriver(url):

    headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '+
                   'AppleWebKit/537.36 (KHTML, like Gecko) '+
                   'Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    logging.debug('Page {} retrived with status code : {}'.format(url, response.status_code))
    return response.text

def _article_downloader(url, article_path):

    html = _page_retriver(url)
    article_content = _article_parser(html)
    _save_to_path(article_content.toJSON(), path=article_path)

    return article_content

def _article_parser(html_string):
    from lxml import html
    content = ''
    soup = BeautifulSoup(html_string, 'html.parser')
    title_tag = soup.find('h1', {'class':'c-page-title'})
    if title_tag is None:
        title = ''
        logging.critical('title could not be PARSED!')
    else:
        title = title_tag.getText()

    [bad.extract() for bad in soup.findAll('script')]

    for _content_tag in soup.find_all('div', 'c-entry-content'):
        tree = html.fromstring(_content_tag.__str__())
        extracted = tree.text_content()
        content += ' ' + extracted
    return Article(title, content)

##############################################################################
#                              Module Utilities                             #
##############################################################################

class Article(object):
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def toJSON(self):
        import json
        jart = {}
        jart["title"] = self.title
        jart["content"] = self.content
        return json.dumps(jart)

    def buildFromJSON(jsonString, encoding='utf-8'):
        import json
        jart = json.loads(jsonString, encoding=encoding)
        return Article(jart["title"], jart["content"])

def pages_downloader(urls):
    PAGES_DIR_PATH = './pages/{}'
    pages = []

    #If no directory will make it.
    os.makedirs(PAGES_DIR_PATH.format(''), exist_ok=True)

    for url in urls:
        retrived = _page_retriver(url)
        _save_to_path(retrived, PAGES_DIR_PATH.format(url.replace('/', '_')))
        pages.append(retrived)

    return pages


def news_urls_retriver(limit = 1000):
    '''
    Saves into out_dir_path the news from The Verge Archive
    :param limit: maximum number of news to save into the output directory.
    :return: list of news URLs
    '''
    NEWS_ARCHIVE_PATH = 'https://www.theverge.com/archives/{}'
    news = set()
    index = 1

    while(len(news) < limit):
        html = _page_retriver(NEWS_ARCHIVE_PATH.format(index))
        soup = BeautifulSoup(html, 'html.parser')
        for article in soup.find_all('li', 'p-basic-article-list__node'):
            news.add(article.find('div', 'body').find('h3').find('a')['href'])
            index += 1
            if len(news) >= limit:
                break
        time.sleep(1)

    return [x for x in news]


def news_articles_retriver(urls, force_download=False):
    NEWS_DIR_PATH = './news/{}'
    os.makedirs(NEWS_DIR_PATH.format(''), exist_ok=True)
    articles = []
    downloaded = 0
    for url in urls:
        article_path = NEWS_DIR_PATH.format(url.replace('/', '_'))
        article_file = Path(article_path)
        if not force_download:
            try:
                article_abs_path = article_file.resolve()
            except FileNotFoundError:
                logging.debug('cache miss! file = {}'.format(article_file))
                article_content = _article_downloader(url, article_path)
                downloaded += 1
                articles.append(article_content)
                if downloaded % 4 == 0:
                    time.sleep(1)
            else:
                logging.debug('cache hit! file = {}'.format(article_file))
                articles.append(Article.buildFromJSON(article_abs_path.read_text(encoding='utf-8', errors='replace')))
        else:
            articles.append(_article_downloader(url, article_path))
            downloaded += 1
            if downloaded % 2 == 0:
                time.sleep(1)
    return articles

def articles_from_folder(folder='./news'):
    articles = []
    for file in os.listdir(folder):
        try:
            with open(os.path.join(folder, file), 'r', encoding='utf-8') as fin:
                article = Article.buildFromJSON(' '.join(fin.readlines()))
                if article is not None and (article.title is not None and article.content is not None):
                    articles.append(article)
        except Exception as e:
            logging.critical('Error in loading news from file:{}'.format(e))
    return articles


##############################################################################
#                                Testring Area                               #
##############################################################################

