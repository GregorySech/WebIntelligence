import pprint

from gensim import corpora, models, similarities
#ESERCIZIO 1
# Estrarre i testi dei documenti, eliminando punteggiatura e le parole comuni
from gensim.similarities.docsim import Similarity, SparseMatrixSimilarity, MatrixSimilarity

TWEET_PATH = '/home/gregory/Documents/WebIntelligence/Archivi/venezia72_2015.txt/data'
STOPWORDS_PATH = '/home/gregory/Documents/WebIntelligence/Archivi/stopwords.txt'
WORD_BLACKLIST = []
with open(STOPWORDS_PATH, 'r', encoding='utf-8') as swin:
    for word in swin.readline().split():
        WORD_BLACKLIST.append(word)
WORD_BLACKLIST = set(WORD_BLACKLIST)

texts = []
with open(TWEET_PATH, 'r', encoding='utf-8') as fin:
    lines = []
    for x in range(100):
        lines.append(fin.readline())
    texts = [[word for word in document.lower().split() if word not in WORD_BLACKLIST] for document in lines]
	#print("{}".format(texts))
	

#ESERCIZIO 2
# Costruire il lessico (gensim.corpora.Dictionary), scartando le parole con frequenza 1

    lessico = corpora.Dictionary(texts)
    lessico.filter_n_most_frequent(1)
    print(lessico)

#ESERCIZIO 3
# Rappresentare i documenti come vettori (gensim.corpora.Dictionary.doc2bow)
    documents = [document.lower().split() for document in lines]
    vector_documents = [lessico.doc2bow(document) for document in documents]
    print(vector_documents)

#ESERCIZIO 4
# Calcolare la similarità tra (il vettore di) un documento qualsiasi e tutti gli altri (gensim.similarities.MatrixSimilarity)
    S = MatrixSimilarity(vector_documents)
    print("{}".format(S[lessico.doc2bow(documents[3])]))
#ESERCIZIO 5
    # Costruire una funzione che, dato in input (il vettore di) un documento qualsiasi, restituisca gli n=5 documenti della
    # collezione a lui più simili ordinati per punteggio di similarità in modo decrescente
    def mostSimilar(S, lessico, document, n = 5):
        similars = S[lessico.doc2bow(document)]
        return sorted(similars)[1:n]
    print("{}".format(mostSimilar(S, lessico, documents[1])))