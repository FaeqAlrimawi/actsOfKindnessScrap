import gensim
from gensim.models import LdaModel
from nltk import SnowballStemmer, WordNetLemmatizer
from sklearn.datasets import fetch_20newsgroups
import pandas as pd


file_name = 'actsOfKindness.xlsx'
sheet_name = 'train_data_AoK'
description_column = 'Description'

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


# newsgroups_train = fetch_20newsgroups(subset='train', shuffle=True)
# newsgroups_test = fetch_20newsgroups(subset='test', shuffle=True)

stemmer = SnowballStemmer("english")

# Load a potentially pretrained model from disk.
model_file_path = "lda.model"
lda = LdaModel.load(model_file_path)
lda_id2word =   LdaModel.load("lda.model.id2word")

for idx, topic in lda.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic ))


print("model loaded: ")
print(lda)

# processed_docs = []
#
# for doc in newsgroups_train.data:
#     processed_docs.append(preprocess(doc))

'''
Create a dictionary from 'processed_docs' containing the number of times a word appears 
in the training set using gensim.corpora.Dictionary and call it 'dictionary'
'''
print("creating dictionary...")
# dictionary = gensim.corpora.Dictionary(processed_docs)

'''
OPTIONAL STEP
Remove very rare and very common words:

- words appearing less than 15 times
- words appearing in more than 10% of all documents
'''
# dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n= 100000)

## test from the test data
# num = 201
# unseen_document = newsgroups_test.data[num]
# print(unseen_document)
#
# # Data preprocessing step for the unseen document
# bow_vector = dictionary.doc2bow(preprocess(unseen_document))
#
# vector = lda[bow_vector]
#
# for index, score in sorted(lda[bow_vector], key=lambda tup: -1 * tup[1]):
#     print("Score: {}\t Topic: {}".format(score, lda.print_topic(index, 5)))

# print(vector)

## test from the acts of kindness
acts_excel  =pd.read_excel(file_name, sheet_name=sheet_name)

cell_description_value = acts_excel[description_column][2]
print(cell_description_value)


# # Data preprocessing step for the unseen document
bow_vector = lda_id2word.doc2bow(preprocess(cell_description_value))
#

for index, score in sorted(lda[bow_vector], key=lambda tup: -1 * tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda.print_topic(index, 10)))