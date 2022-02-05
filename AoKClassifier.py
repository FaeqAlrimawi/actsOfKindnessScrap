# This script predicts whether given acts are Aoks or Not
# the output is saved in a text file name: acts_preds.txt (same path as the project)
# the file contains two columns: one for the description (i.e. the act) and the prediction (Yes [AoK], No [non-AoK]
# the two columns are separated by $

import os

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
sheet_name = 'AoK_class_test'
description_column = 'Description'
# classifier_column = 'Tech'
# start_index = 0
# end_index = 200

# df_train= pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column, classifier_column])[:170]
df_test= pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column]) #[start_index:end_index]

# movie_data = load_files(r"D:\txt_sentoken")
X = df_test[description_column]

model = pickle.load(open('AoK_classifier_model.pkl', 'rb'))

features_file = pickle.load(open("AoK_features.pkl", "rb"))

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

loaded_vec = CountVectorizer(decode_error="replace",vocabulary=features_file)
converted_data = loaded_vec.fit_transform(np.array(X))
transformer = TfidfTransformer()
X = transformer.fit_transform(converted_data).toarray()

y_pred = model.predict(X)
# y_pred = model.predict_proba(X)


## save to cvs file
fileName = "acts_preds.txt"
f = open(fileName, 'w', encoding='utf-8')
f.write("Description$Tech-pred" + '\n')
f.close()
f = open(fileName, 'a', encoding='utf-8')

# print("Actual Pred")
for act, pred in zip(df_test[description_column], y_pred):
    print(pred, act)
    prediction_str = act+'$' + str(pred) + '\n'
    f.write(prediction_str)

f.close()

# print info
print('\n\nacts file info: {}, {}'.format(file_name, sheet_name))
print('# of acts predicted: ', len(X))
print('model info: ', model)
print("saved to: " + os.path.abspath(f.name))


