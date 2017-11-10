'''
Utilities modules for the Course Web Intelligence.
AY: 2017-2018
'''


def _page_downloader(url, cache_folder='./cached/', ignore_cache=False):
    import os
    import urllib
    from pathlib import Path

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
                content = ' '.join(fin.readlines())
        return content

    os.makedirs(cache_folder, exist_ok=True)
    cache_path = cache_folder + '{}'.format(url.replace("/", "_"))
    if ignore_cache:
        content = _downloader(url)
    else:
        content = _cache(cache_path)
        if content is None:
            content = _downloader(url)

    return content


class Scraper:
    def __init__(self, cache_path=None, parser=None):
        if cache_path is None:
            self.cache_path = "./"
        else:
            self.cache_path = cache_path

        if parser is not None:
            self._parser = parser

    def _parser(self, content):
        '''
        Parses content, pattern command, it should be given by the user.
        :param url: URL to parse.
        :return: Parsed URL content.
        '''
        return None

    def _save_to_file(self, content, path="./{}"):
        with open(file=path, mode='w', encoding='utf-8') as fout:
            print(content, file=fout)


    def parseFromURL(self, url, ignore_cache=False):
        '''
        Returns the parsed object. Builted by the parser given to the class
        :param url: url of web page to download to parse.
        :param ignore_cache: if True it will not try to find cached versions of the url.
        :return: Parsed object
        '''

        page = _page_downloader(url, cache_folder=self.cache_path, ignore_cache=ignore_cache)
        return self._parser(page)



def baseParser(self, content):
    return content

scraper = Scraper(parser=baseParser)

scraper.parseFromURL(url='http://www.watchepisodeseries.com/mr-robot-season-3-episode-5-s03e05__16829904')