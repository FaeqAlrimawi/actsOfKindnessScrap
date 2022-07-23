import pickle
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from bs4 import BeautifulSoup as bs
import requests
import re


model = None

features_file = None

loaded_vec = None


def checkIfAoK(act):
    global model
    global features_file
    global loaded_vec
    
    if not model:
        model = pickle.load(open('./website/static/AoK_classifier_model.pkl', 'rb'))
      
    if not features_file:
       features_file = pickle.load(open("./website/static/AoK_features.pkl", "rb"))

    if not loaded_vec:
        loaded_vec = CountVectorizer(decode_error="replace",vocabulary=features_file)
 
            
    converted_data = loaded_vec.fit_transform([act])
    transformer = TfidfTransformer()
    text = transformer.fit_transform(converted_data).toarray()
    y_pred = model.predict_proba(text)
        
    prob = y_pred[0][1]*100
    
    # print("#### act:", act, " prob:", prob)
    
    return prob


def scrapWebiste(websiteURL):
    page = requests.get(websiteURL)
    soup = bs(page.content)
    
    return soup.getText()
    