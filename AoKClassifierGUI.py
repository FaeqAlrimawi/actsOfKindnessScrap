import os
import pickle
import re
import PySimpleGUI as sg
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk import pos_tag
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


### for predicting sentiment
def clean(text):
# Removes all special characters and numericals leaving the alphabets
    text = re.sub('[^A-Za-z]+', ' ', text)
    return text


# POS tagger dictionary
pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}
def token_stop_pos(text):
    tags = pos_tag(word_tokenize(text))
    newlist = []
    for word, tag in tags:
        if word.lower() not in set(stopwords.words('english')):
            newlist.append(tuple([word, pos_dict.get(tag[0])]))
    return newlist


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


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
def vadersentimentanalysis(review):
    vs = analyzer.polarity_scores(review)
    # return vs['compound']
    return vs


def vader_analysis(compound):
    if compound > 0:
        return 'Positive'
    elif compound <= -0.5 :
        return 'Negative'
    else:
        return 'Neutral'


def get_sentiment(aok):
    ## sentiment analysis
    cleaned_text = clean(str(original_text))
    pos_text = token_stop_pos(cleaned_text)
    lemma_text = lemmatize(pos_text)
    # print("original text {}, pos {}, lemma {}".format(original_text, pos_text, lemma_text))
    sentiment_value = vadersentimentanalysis(lemma_text)
    return sentiment_value
    # return vader_analysis(sentiment_value)
    # print("sentiment: {}".format(sentiment_value))


## load model
model = pickle.load(open('AoK_classifier_model.pkl', 'rb'))

features_file = pickle.load(open("AoK_features.pkl", "rb"))

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
loaded_vec = CountVectorizer(decode_error="replace",vocabulary=features_file)


# ----- Full layout -----
import numpy as np

layout = [

    [
        sg.Text("Enter act:"),
        sg.InputText(size=(30, 1), enable_events=True, key="-ACT-"),
        sg.Button("Is an AoK?", key="-CHECK-")
    ],
    [
        sg.Text("", font='bold', key="-RESULT-"),
        sg.Text("", key="-RESULTExtra-")
    ],

    [
        sg.Text("", key="-Sentiment-")
    ]
]

sg.theme("DarkBlue3")
# sg.set_options(font=("Courier New", 13))

window = sg.Window("Acts of Kindness Predictor", layout, finalize=True)
window['-ACT-'].bind("<Return>", "_Enter")

while True:

    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:

        break

    elif event == "-CHECK-" or event == "-ACT-" + "_Enter":
        original_text = [values["-ACT-"]]
        converted_data = loaded_vec.fit_transform(original_text)
        transformer = TfidfTransformer()
        text = transformer.fit_transform(converted_data).toarray()
        y_pred = model.predict_proba(text)

        yes_result = y_pred[0][1]
        lower_threshold = 0.4
        upper_threshold = 0.6

        # get sentiment
        # print(get_sentiment(original_text))
        sentiment_analysis = get_sentiment(original_text)
        sentiment_judgment_value = vader_analysis(sentiment_analysis['compound'])
        sentiment_analysis_text = "Sentiment: {}. Details: Positive [{}], Neutral [{}], Negative [{}]".format(sentiment_judgment_value, sentiment_analysis['pos'],
                                                                                                                     sentiment_analysis['neu'], sentiment_analysis['neg'])
        # print(sentiment_analysis_text, "compound [{}]".format(sentiment_analysis['compound']))
        isAok = ""
        label_result = ""
        label_result_extra = ""

        if yes_result < lower_threshold:
            # print(lemmatize(pos_tag())))
            label_result = " Not Really! "
            label_result_extra = "(Confidence in [not AoK] " + "{:.1f}".format(y_pred[0][0]*100)+ "%)"

        elif lower_threshold <= yes_result <= upper_threshold:
            label_result = "Hmmm maybe?!"
            label_result_extra = "(Confidence in [an AoK] " + "{:.1f}".format(y_pred[0][1] * 100) + "%)"
        else:
            label_result += "Yep!"
            label_result_extra = "(Confidence in [an AoK] " + "{:.1f}".format(y_pred[0][1]*100)+ "%)"


        window["-RESULT-"].update(label_result)
        window["-RESULTExtra-"].update(label_result_extra)
        window["-Sentiment-"].update(sentiment_analysis_text)

window.close()