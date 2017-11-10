'''
First Assignment part A module: Data Retrival.

a.1)    I've choosen www.theverge.com for my crawling. The Verge is a Tech-centric news site quite popular.
        It has an archive section of the site where I will retrive the URLs for the news. The archive
        URL is: https://www.theverge.com/archives.

        Each archive page has 10 news previews at date 2 November 2017.
'''

from bs4 import BeautifulSoup
from gensim import corpora
from gensim import utils
from pathlib import Path
import urllib.request
import urllib.error
import time


import matplotlib.pyplot as plt;
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
#                             Private Utilities                              #
##############################################################################

def _save_to_path(string_content, path = './dummy_save'):
    with open(file=path, mode='w', encoding='utf-8') as fout:
        print(string_content, file=fout)

def _article_downloader(url, article_path):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        article_content = _article_parser(html)
        _save_to_path(article_content.toJSON(), path=article_path)
    return article_content

def _article_parser(html_string):
    from lxml import html
    content = ''
    soup = BeautifulSoup(html_string, 'html.parser')
    title_tag = soup.find('h1', {'class':'c-page-title'})
    if title_tag is None:
        title = 'couldnotbeparsed'
        print('Title could not be parsed!')
    else:
        title = title_tag.getText()

    for _content_tag in soup.find_all('div', 'c-entry-content'):
        tree = html.fromstring(_content_tag.__str__())
        for bad in tree.xpath("//script"):
            bad.getparent().remove(bad)
        extracted = tree.text_content()
        content += ' ' + extracted.replace('\n', '').replace('\r','').replace('(', ' ').replace(')', ' ')
    return Article(title, content)

##############################################################################
#                              Module Functions                              #
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
                    if len(news) >= limit:
                        break
                time.sleep(1)
        except urllib.error.HTTPError as e:
            print('HTTP ERROR! {}'.format(e.info()))
            flag = True
    return [x for x in news]

def news_articles_retriver(urls, force_download=False):
    import os
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
                print('cache miss! file = {}'.format(article_file))
                article_content = _article_downloader(url, article_path)
                downloaded += 1
                articles.append(article_content)
                if downloaded % 2 == 0:
                    time.sleep(1)
            else:
                print('cache hit! file = {}'.format(article_file))
                articles.append(Article.buildFromJSON(article_abs_path.read_text(encoding='utf-8', errors='replace')))
        else:
            articles.append(_article_downloader(url, article_path))
            downloaded += 1
            if downloaded % 2 == 0:
                time.sleep(1)
    return articles

##############################################################################
#                                Testring Area                               #
##############################################################################

#Parte A - Raccolta

test = news_urls_retriver(100)
print('Retriver URLS : ')
print(test)
articles = news_articles_retriver(test)

print("Articles retrived!!!\nHere are the titles:")

for article in articles:
    print(article.title)

contents = [article.content for article in articles]

#Parte B - Raccomandazione

#B - 1
blacklist = set()
with open('stopwords-en.txt', 'r', encoding='utf-8') as fin:
    blacklist = set([word.replace('\n', '').replace('\r','') for word in fin.readlines()])

vector_contents = [[word for word in content.lower().split() if word not in blacklist] for content in contents]

dictionary = corpora.Dictionary(vector_contents)

occurencies = dictionary.doc2bow([item for contents in vector_contents for item in contents])

frequencies = dict(occurencies)
top500 = sorted(frequencies, key=frequencies.get, reverse=True)[:500]
top500freq = [frequencies[item] for item in top500]

for t in top500[:20]:
    print('{} -> {}'.format(dictionary.get(t), frequencies[t]))

print(blacklist)

y_pos = np.arange(len(top500))
performance = top500freq



plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.ylabel('Frequency')
plt.xlabel('Rank')
plt.title('Frequency over Rank (with stopwords)')

plt.show()



