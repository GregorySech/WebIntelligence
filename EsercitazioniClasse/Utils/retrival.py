'''
Utilities modules for the Course Web Intelligence.
AY: 2017-2018
'''

class Scraper:
    def __init__(self, cache_path=None, parser=None):
        if cache_path is None:
            self.cache_path = "./{}"
        else:
            self.cache_path = cache_path

        if parser is not None:
            self._parser = parser

    def _parser(self, url):
        '''
        Parses a URL, pattern command, it should be given by the user.
        :param url: URL to parse.
        :return: Parsed URL content.
        '''

    def _save_to_file(self, content, path="./{}"):
        with open(file=path, mode='w', encoding='utf-8') as fout:
            print(content, file=fout)


    def parseURL(self, url, ignore_cache=False):
        '''
        Returns the parsed object. Builted by the parser given to the class
        :param url: url of web page to download to parse.
        :param ignore_cache: if True it will not try to find cached versions of the url.
        :return: Parsed object
        '''
        if ignore_cache:
            pass
        else:
            pass



//*[@id="px"]/div[3]/div/div[5]/a

