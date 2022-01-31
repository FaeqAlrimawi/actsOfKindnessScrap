# Generates a model to predict whether an AoK is technology-mediated or not
# it is also used to create a model to predict whether a given act (or a statement can be an AoK)
#generated model is saved where the project is


import os

import numpy
import numpy as np
import re
import nltk
from sklearn.datasets import load_files
from sklearn.ensemble import RandomForestClassifier

# nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords
import pandas as pd
from pickle import dump

from sklearn.preprocessing import MinMaxScaler

### last used to create a model predicting AoKs
file_name = 'actsOfKindness.xlsx'
sheet_name = 'AoK_class_train'
description_column = 'Description'
classifier_column = 'AoK'
# start_index = 0
# end_index = 129

df_train= pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column, classifier_column])
# df_predict = pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column, classifier_column])[151:208]

# movie_data = load_files(r"D:\txt_sentoken")
act_description, act_tech = df_train[description_column], df_train[classifier_column]

# print(X)

documents = []

from nltk.stem import WordNetLemmatizer

stemmer = WordNetLemmatizer()

for sen in range(0, len(act_description)):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(act_description[sen]))

    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)

    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)

    # Converting to Lowercase
    document = document.lower()

    # Lemmatization
    document = document.split()

    document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)

    documents.append(document)

# from sklearn.feature_extraction.text import CountVectorizer
# vectorizer = CountVectorizer(max_features=500, min_df=5, max_df=1.0, stop_words=stopwords.words('english'))
# X = vectorizer.fit_transform(documents).toarray()

# from sklearn.feature_extraction.text import TfidfTransformer
# tfidfconverter = TfidfTransformer()
# X = tfidfconverter.fit_transform(X).toarray()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidfconverter = TfidfVectorizer(max_features=1000, min_df=5, max_df=0.8, sublinear_tf=True, ngram_range=(1,2), stop_words=stopwords.words('english'))
features = tfidfconverter.fit_transform(documents)
print("features: ", features.shape)

# transform the dataset
from imblearn.over_sampling import SMOTE
oversample = SMOTE()
features, act_tech = oversample.fit_resample(features, act_tech)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(features, act_tech, test_size=0.2, random_state=0)

# # define scaler
# scaler = MinMaxScaler()
# # fit scaler on the training dataset
# scaler.fit(X_train)
# # transform both datasets
# X_train_scaled = scaler.transform(X_train)
# X_test_scaled = scaler.transform(X_test)

classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
classifier.fit(X_train, y_train)

# print(X_test)

y_pred = classifier.predict(X_test)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# info about model, train and test data
print('model: ', classifier)
print('acutal number of acts: ', len(df_train[description_column]))
print("# of training acts (with oversampling): ", len(X_train.toarray()))
print('# of test acts (with oversampling): ', len(y_test))

# evaluate predictions
acc = accuracy_score(y_test, y_pred)

print("Accuracy: %.3f" % acc)

precision = precision_score(y_test, y_pred, average='binary', pos_label="yes")
print('Precision: %.3f' % precision)

# calculate recall
recall = recall_score(y_test, y_pred, average='binary', pos_label='yes')
print('Recall: %.3f' % recall)

# calculate score
score = f1_score(y_test, y_pred, average='binary', pos_label='yes')
print('F-Measure: %.3f' % score)

# print("Actual Pred")
# for act, pred in zip(y_test, y_pred):
#     if act == pred:
#         print(act, pred)
#     else:
#         print(act, pred, "not equalllll")

## predict
# X_predict = df_predict[description_column]
# X_pred = tfidfconverter.transform(X_predict).toarray()
#
# y_pred = classifier.predict(X_pred)
#
# X_predict_array = np.array(X_predict)
#
# for i in range(len(X_predict_array)):
#     print(y_pred[i], X_predict_array[i])

# save the model and features
file_model = open('AoK_classifier_model.pkl', 'wb')
file_features = open('AoK_features.pkl', 'wb')
dump(classifier, file_model)
dump(tfidfconverter.vocabulary_, file_features)

print('\nmodel saved to: ', os.path.abspath(file_model.name))
print('features saved to: ', os.path.abspath(file_features.name))