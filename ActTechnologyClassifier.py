import numpy as np
import re
import nltk
from sklearn.datasets import load_files
from sklearn.ensemble import RandomForestClassifier

# nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords
import pandas as pd
from pickle import load

# load the model
classifier_model  = load(open('classifier_model.pkl', 'rb'))

file_name = 'actsOfKindness.xlsx'
description_column = 'Description'
classifier_column = 'UsesTechnology'

df_train= pd.read_excel(file_name, usecols=[description_column, classifier_column])[:101]
df_test= pd.read_excel(file_name, usecols=[description_column, classifier_column])[76:102]

# movie_data = load_files(r"D:\txt_sentoken")
X = df_test[description_column]

# print("print..." + X[0])

documents = []

from nltk.stem import WordNetLemmatizer

stemmer = WordNetLemmatizer()

for sen in range(76, 101):
    # print(sen)
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

# print(documents)
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X = vectorizer.fit_transform(documents).toarray()

from sklearn.feature_extraction.text import TfidfTransformer
tfidfconverter = TfidfTransformer()
X = tfidfconverter.fit_transform(X).toarray()

from sklearn.feature_extraction.text import TfidfVectorizer
tfidfconverter = TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X = tfidfconverter.fit_transform(documents).toarray()

# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
# classifier.fit(X_train, y_train)

y_pred = classifier_model.predict(X)


# print(X_test)
print(y_pred)
