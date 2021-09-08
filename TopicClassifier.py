from sklearn.datasets import fetch_20newsgroups

# pip install gensim
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(400)
import pandas as pd

# import nltk
# nltk.download('wordnet')


'''
Write a function to perform the pre processing steps on the entire dataset
'''

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


# Tokenize and lemmatize
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))

    return result


newsgroups_train = fetch_20newsgroups(subset='train', shuffle = True)
newsgroups_test = fetch_20newsgroups(subset='test', shuffle = True)

# print(list(newsgroups_train.target_names))

# past tense to present tense
# print(WordNetLemmatizer().lemmatize('went', pos = 'v'))

stemmer = SnowballStemmer("english")
# stemmer example
# stemmer = SnowballStemmer("english")
# original_words = ['caresses', 'flies', 'dies', 'mules', 'denied','died', 'agreed', 'owned',
#            'humbled', 'sized','meeting', 'stating', 'siezing', 'itemization','sensational',
#            'traditional', 'reference', 'colonizer','plotted']
# singles = [stemmer.stem(plural) for plural in original_words]
#
# pd.DataFrame(data={'original word':original_words, 'stemmed':singles })

'''
Preview a document after preprocessing
'''
# document_num = 50
# doc_sample = 'This disk has failed many times. I would like to get it replaced.'
#
# print("Original document: ")
# words = []
# for word in doc_sample.split(' '):
#     words.append(word)
# print(words)
# print("\n\nTokenized and lemmatized document: ")
# print(preprocess(doc_sample))

processed_docs = []

for doc in newsgroups_train.data:
    processed_docs.append(preprocess(doc))


'''
Create a dictionary from 'processed_docs' containing the number of times a word appears 
in the training set using gensim.corpora.Dictionary and call it 'dictionary'
'''
print("creating disctionary...")
dictionary = gensim.corpora.Dictionary(processed_docs)


'''
Checking dictionary created
'''
# count = 0
# for k, v in dictionary.iteritems():
#     print(k, v)
#     count += 1
#     if count > 10:
#         break


'''
OPTIONAL STEP
Remove very rare and very common words:

- words appearing less than 15 times
- words appearing in more than 10% of all documents
'''
dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n= 100000)


print("creating bag of words...")
'''
Create the Bag-of-words model for each document i.e for each document we create a dictionary reporting how many
words and how many times those words appear. Save this to 'bow_corpus'
'''
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]


# LDA mono-core -- fallback code in case LdaMulticore throws an error on your machine
lda_model = gensim.models.LdaModel(bow_corpus,
                                   num_topics = 10,
                                   id2word = dictionary,
                                   passes = 50)

# LDA multicore
print("creating the model...")
'''
Train your lda model using gensim.models.LdaMulticore and save it to 'lda_model'
'''
# TODO
# lda_model =  gensim.models.LdaMulticore(bow_corpus,
#                                    num_topics = 10,
#                                    id2word = dictionary,
#                                    passes = 50,
#                                    workers = 1)

for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic ))
    print("\n")

