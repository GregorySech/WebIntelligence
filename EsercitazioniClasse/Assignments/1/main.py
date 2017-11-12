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

test = v_r.news_urls_retriver(100)
articles = v_r.news_articles_retriver(test)

#Cleaning contents
contents = [' '.join(re.sub("[^0-9a-zA-Z ]+", ' ', article.content).split()) for article in articles]

#Parte B - Raccomandazione

#B - 1/2
blackset = set()
blacklist = []
with open('stopwords-en.txt', 'r', encoding='utf-8') as fin:
    for p in [re.sub("[^0-9a-zA-Z ]+", ' ', line).split() for line in fin]:
        for b in p:
            blacklist.append(b)
    blackset = set(blacklist)

vector_contents = [[word for word in content.lower().split() if word not in blackset] for content in contents]
vector_contents = [utils.lemmatize(' '.join(content)) for content in vector_contents]
dictionary = corpora.Dictionary(vector_contents)

frequencies = dict(dictionary.doc2bow([item for contents in vector_contents for item in contents]))
top500 = sorted(frequencies, key=frequencies.get, reverse=True)[:500]
top500freq = [frequencies[item] for item in top500]

y_pos = np.arange(len(top500))

for term in top500[:10]:
    print('{} Frequency: {}'.format(dictionary.get(term), frequencies[term]))

#plt.bar(y_pos, performance, align='center', alpha=0.5)
# plt.plot(y_pos, top500freq)
# plt.ylabel('Frequency')
# plt.xlabel('Rank')
# plt.title('Frequency over Rank (with stopwords)')
#
# plt.show()

#B - 3
corpus = [dictionary.doc2bow(content) for content in vector_contents]

tf_idf = TfidfModel(corpus=corpus, dictionary=dictionary)

print(tf_idf[corpus[1]])

index = similarities.SparseMatrixSimilarity(tf_idf[corpus], num_features=30)

print("prova")

print("prova")

pprint(list(enumerate(sims)))