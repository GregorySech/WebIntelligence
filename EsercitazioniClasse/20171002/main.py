def prodotto_scalare_iterativo(a, b):
    result = 0
    if isinstance(a, list) and isinstance(b, list):
        if len(a) == len(b):
            for (n, m) in zip(a,b):
                result += n * m
            return result
        else:
            raise ValueError('Lists length do not match')
    else:
        raise TypeError('arguments must be lists')

def prodotto_scalare_lambdoso(a, b):
    if isinstance(a, list) and isinstance(b, list):
        if len(a) == len(b):
            #mol = lambda (m, n) : m*n
            #sum = lambda m, n: m + n

            return 0#reduce(sum, map(mol, zip(a, b)))

        else:
            raise ValueError('Lists length do not match')
    else:
        raise TypeError('arguments must be lists')


x = [1, 2, 3, 4, 5]
y = [10, 20, 30, 40, 50]

print('ITERATIVO : {}, FUNZIONALE : {}'.format(prodotto_scalare_iterativo(x, y), prodotto_scalare_lambdoso(x,y)))
print('-'*80)
class FileMagicCounter(object):
    '''
    Occurencies counter about words in a file.
    Info about rows are also stored.
    '''
    def __init__(self, file = None):
        self.rows = []
        self.occs = {}
        if(file is not None):
            self.update(file)
    
    def update(self, file):
        '''
        Updates for a file
        '''
        import io
        def __upd(dicti, word):
            if word not in dicti.keys():
                dicti[word] = 0
            dicti[word] += 1

        with io.open(file, 'r', encoding='utf-8') as fin:
            for line in fin:
                occ = {}
                for word in line.split():
                    __upd(occ, word)
                    __upd(self.occs, word)
                self.rows.append(occ)
    def get_lines_number(self):
        '''
        returns the number of rows the counter has read
        '''
        return len(self.rows)
    def get_words_number(self):
        '''
        returns the number of words the counter has read
        '''
        return len(self.occs.keys)
    def get_most_frequent_words(self, limit=None):
        '''
        returns the limit most frequent words, with limit = None
        it just sorts the dictionary
        '''
        sortedWords = [t for t,p in [(k, self.occs[k]) for k in sorted(self.occs, key = self.occs.get, reverse = True)]]
        if limit is None:
            return sortedWords
        else:
            return sortedWords[:limit]

fmc = FileMagicCounter(file='/home/gregory/Documenti/WebIntelligence/Archivi/venezia72_2015.txt/data')

print('-'*80)
i = 0

for word in fmc.get_most_frequent_words(limit = 100):
    print('{} -> {}'.format(i, word.encode('utf8')))
    i += 1
