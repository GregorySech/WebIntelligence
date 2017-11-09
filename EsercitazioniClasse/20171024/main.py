'''
Estrare informazione da HTML.

HTML è un linguaggio context-free -> può essere riconosciuto da un automa a pila ma non da una RE.
'''
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
from pathlib import Path
import time
URLSPATH = '/home/gregory/Documents/WebIntelligence/Archivi/ANSA_UrlList.txt'
FILESPATH = './scraps/{}'

def get_pages_from_url(urlpaths, outdir, limit=None):
    '''

    :param urlpaths: path to input file. For each line one url.
    :param outdir: path to the output directory where the files will be saved.
    :param limit: number of urls to download, if none all the urls will be used.
    :return: None
    '''
    def html_downloader(url, outdir):
        '''

        :param url: url of the single file to download
        :param outdir: path to the output directory where the file will be saved.
        :return: None
        '''
        fpath = outdir.format(url.replace('/', '_'))
        file = Path(fpath)
        try:
            abs_path = file.resolve()
        except FileNotFoundError:
            try:
                with urllib.request.urlopen(url) as response:
                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    with open(file=fpath, mode='w', encoding='utf-8') as fout:
                        print(soup.prettify(), file=fout)
                        print('{} FILE SAVED!'.format(fpath))
                    time.sleep(1)
            except urllib.error.HTTPError as e:
                print('HTTP ERROR! {}'.format(e.info()))
        else:
            print('FILE FOUND! {}'.format(fpath))
        return None

    with open(file = urlpaths, mode='r', encoding='utf-8') as urlin :

        if limit is None:
            for url in urlin:
                html_downloader(url, outdir)
        else:
            for i in range(limit):
                url = urlin.readline()
                html_downloader(url, outdir)

get_pages_from_url(URLSPATH, FILESPATH, 50)