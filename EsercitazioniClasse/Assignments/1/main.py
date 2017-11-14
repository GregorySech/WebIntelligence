'''
Main script of the First Assignment
'''

from gensim import corpora
from gensim import utils
from gensim import similarities

import re
import matplotlib.pyplot as plt;
from gensim.models.tfidfmodel import TfidfModel

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import verge_retrival as v_r

#Parte A - Raccolta

print('Loading articles (read log!)')

# urls = v_r.news_urls_retriver()
# articles = v_r.news_articles_retriver(urls)

articles = v_r.articles_from_folder()
titles = [article.title for article in articles]


print('Loaded articles from folder!')
#Cleaning contents
contents = [' '.join(re.sub("[^0-9a-zA-Z ]+", ' ', article.title).split()) + ' '.join(re.sub("[^0-9a-zA-Z ]+", ' ', article.content).split()) for article in articles]
print('Content cleaned!')
#Parte B - Raccomandazione
#B - 1/2
blackset = set()
blacklist = []
with open('stopwords-en.txt', 'r', encoding='utf-8') as fin:
    for p in [re.sub("[^0-9a-zA-Z ]+", ' ', line).split() for line in fin]:
        for b in p:
            blacklist.append(b)
    blackset = set(blacklist)
    print('Black-set created!')

vector_contents = [[word for word in content.lower().split() if word not in blackset] for content in contents]

print('Lemmatizing...')
vector_contents = [utils.lemmatize(' '.join(content)) for content in vector_contents]
dictionary = corpora.Dictionary(vector_contents)
print('Dictionary Created!')


frequencies = dict(dictionary.doc2bow([item for contents in vector_contents for item in contents]))
top500 = sorted(frequencies, key=frequencies.get, reverse=True)[:500]
top500freq = [frequencies[item] for item in top500]

y_pos = np.arange(len(top500))

[print('{} => {}'.format(dictionary.get(id), frequencies[id])) for id in top500]

plt.plot(y_pos, top500freq)
plt.ylabel('Frequency')
plt.xlabel('Rank')
plt.title('Frequency over Rank (with stopwords)')

plt.show()

#B - 3

def user_profile(bows):
    user = {}
    for bow in bows:
        for (id, freq) in bow:
            if id not in user.keys():
                user[id] = freq
            else:
                user[id] += freq
    return [(id, freq/len(bows)) for (id, freq) in user.items()]


corpus = [dictionary.doc2bow(content) for content in vector_contents]

print('Generating User profile')
query = user_profile(corpus[:20])

tf_idf = TfidfModel(corpus=corpus, dictionary=dictionary)

index = similarities.MatrixSimilarity(tf_idf[corpus])

sims = index[tf_idf[query]]

similars = list(enumerate(sims))

similars.sort(key=lambda x: x[1], reverse=True)

rank = 1
print('TITLES OF THE FIRST 20')
pprint(titles[:20])

print('Raccomandations (50):')
for (k,v) in similars[:50]:
    print('{} => {}'.format(rank,titles[k]))
    rank+=1

