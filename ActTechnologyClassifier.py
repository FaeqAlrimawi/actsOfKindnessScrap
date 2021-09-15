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

file_name = 'actsOfKindness.xlsx'
sheet_name = 'test'
description_column = 'Description'
classifier_column = 'Tech'

start_index = 100
end_index = 151
# df_train= pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column, classifier_column])[:170]
df_test= pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column, classifier_column])[start_index:end_index]

# movie_data = load_files(r"D:\txt_sentoken")
X, y = df_test[description_column], df_test[classifier_column]

# print(X)

documents = []

from nltk.stem import WordNetLemmatizer

stemmer = WordNetLemmatizer()

for sen in range(start_index, end_index):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(X[sen]))

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

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=500, min_df=5, max_df=1.0, stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(documents).toarray()

from sklearn.feature_extraction.text import TfidfTransformer
tfidfconverter = TfidfTransformer()
X = tfidfconverter.fit_transform(X).toarray()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidfconverter = TfidfVectorizer(max_features=500, min_df=5, max_df=1.0, stop_words=stopwords.words('english'))
X = tfidfconverter.fit_transform(documents).toarray()

# transform the dataset
# from imblearn.over_sampling import SMOTE
# oversample = SMOTE()
# X, y = oversample.fit_resample(X, y)

# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# # define scaler
# scaler = MinMaxScaler()
# # fit scaler on the training dataset
# scaler.fit(X_train)
# # transform both datasets
# X_train_scaled = scaler.transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
# classifier.fit(X_train, y_train)

# print(X_test)
model = pickle.load(open('classifier_model.pkl', 'rb'))

y_pred = model.predict(X)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# evaluate predictions
acc = accuracy_score(X, y_pred)

print("Accuracy: %.3f" % acc)

precision = precision_score(X, y_pred, average='binary', pos_label="yes")
print('Precision: %.3f' % precision)

# calculate recall
recall = recall_score(X, y_pred, average='binary', pos_label='yes')
print('Recall: %.3f' % recall)

# calculate score
score = f1_score(X, y_pred, average='binary', pos_label='yes')
print('F-Measure: %.3f' % score)

print("Actual Pred")
for act, pred in zip(X, y_pred):
    if act == pred:
        print(act, pred)
    else:
        print(act, pred, "not equalllll")


# save the model
# dump(classifier, open('classifier_model.pkl', 'wb'))