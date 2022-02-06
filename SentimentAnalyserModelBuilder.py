
import re
import pandas as pd
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk import pos_tag
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

# Define a function to clean the text

file_name = 'actsOfKindness.xlsx'
sheet_name = 'train_sentiment'
description_column = 'Description'


# Creating a pandas dataframe from reviews.txt file
data = pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column])
# print(data.head())


def clean(text):
# Removes all special characters and numericals leaving the alphabets
    text = re.sub('[^A-Za-z]+', ' ', text)
    return text


# Cleaning the text in the review column
data['Cleaned Description'] = data[description_column].apply(clean)
# print(data.head())


# POS tagger dictionary
pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}
def token_stop_pos(text):
    tags = pos_tag(word_tokenize(text))
    newlist = []
    for word, tag in tags:
        if word.lower() not in set(stopwords.words('english')):
            newlist.append(tuple([word, pos_dict.get(tag[0])]))
    return newlist

data['POS tagged'] = data['Cleaned Description'].apply(token_stop_pos)
# print(data.head())

wordnet_lemmatizer = WordNetLemmatizer()
def lemmatize(pos_data):
    lemma_rew = " "
    for word, pos in pos_data:
        if not pos:
            lemma = word
            lemma_rew = lemma_rew + " " + lemma
        else:
            lemma = wordnet_lemmatizer.lemmatize(word, pos=pos)
            lemma_rew = lemma_rew + " " + lemma
    return lemma_rew

data['Lemma'] = data['POS tagged'].apply(lemmatize)
# print(data.head())


#### Sentiment Analysis with TextBlob
# function to calculate subjectivity
# def getSubjectivity(review):
#     return TextBlob(review).sentiment.subjectivity
#
#
# # function to calculate polarity
# def getPolarity(review):
#     return TextBlob(review).sentiment.polarity
#
# # function to analyze the reviews
# def analysis(score):
#     if score < 0:
#         return 'Negative'
#     elif score == 0:
#         return 'Neutral'
#     else:
#         return 'Positive'
#
# fin_data = pd.DataFrame(data[[description_column, 'Lemma']])
# # fin_data['Subjectivity'] = fin_data['Lemma'].apply(getSubjectivity)
# fin_data['Polarity'] = fin_data['Lemma'].apply(getPolarity)
# fin_data['Analysis'] = fin_data['Polarity'].apply(analysis)


#### Sentiment Analysis using Vader Sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

fin_data = pd.DataFrame(data[[description_column, 'Lemma']])

# function to calculate vader sentiment
def vadersentimentanalysis(review):
    vs = analyzer.polarity_scores(review)
    return vs['compound']


fin_data['Vader Sentiment'] = fin_data['Lemma'].apply(vadersentimentanalysis)


# function to analyse
def vader_analysis(compound):
    if compound >= 0.5:
        return 'Positive'
    elif compound <= -0.5 :
        return 'Negative'
    else:
        return 'Neutral'


fin_data['Vader Analysis'] = fin_data['Vader Sentiment'].apply(vader_analysis)
fin_data.head()

#### Sentiment Analysis using SentiWordnet
# nltk.download('sentiwordnet')
# from nltk.corpus import sentiwordnet as swn
#
#
# def sentiwordnetanalysis(pos_data):
#     sentiment = 0
#     tokens_count = 0
#     for word, pos in pos_data:
#         if not pos:
#             continue
#         lemma = wordnet_lemmatizer.lemmatize(word, pos=pos)
#         if not lemma:
#             continue
#         synsets = wordnet.synsets(lemma, pos=pos)
#         if not synsets:
#             continue
#         # Take the first sense, the most common
#         synset = synsets[0]
#         swn_synset = swn.senti_synset(synset.name())
#         sentiment += swn_synset.pos_score() - swn_synset.neg_score()
#         tokens_count += 1
#         # print(swn_synset.pos_score(),swn_synset.neg_score(),swn_synset.obj_score())
#         if not tokens_count:
#             return 0
#         if sentiment>0:
#             return "Positive"
#         if sentiment==0:
#             return "Neutral"
#         else:
#             return "Negative"

# fin_data = pd.DataFrame(data[[description_column, 'Lemma']])
# fin_data['SWN analysis'] = data['POS tagged'].apply(sentiwordnetanalysis)

print(fin_data)
fin_data.to_excel("sentiment_data.xlsx")