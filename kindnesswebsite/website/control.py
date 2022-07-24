import pickle
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from bs4 import BeautifulSoup as bs
import requests
import re
import nltk
import trafilatura
import json
import numpy as np
from requests.models import MissingSchema

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


def scrapWebsite(websiteURL):
    page = requests.get(websiteURL)
    soup = bs(page.content, features="html.parser")
    text = soup.find_all(text=True)
    processWebsiteScrapText(text)
    return soup.getText()
    # text = extract_text_from_single_web_page(websiteURL)
    # print(text)


def processWebsiteScrapText(text):
    # returns the set of sentences in the given text
   
    # Remove unwanted tag elements:
    cleaned_text = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',]
    
    # Then we will loop over every item in the extract text and make sure that the beautifulsoup4 tag
    # is NOT in the blacklist
    for item in text:
        if item.parent.name not in blacklist:
            cleaned_text += '{} '.format(item)
            
      # Remove any tab separation and strip the text:
    cleaned_text = cleaned_text.replace('\t', '')
    # return cleaned_text.strip()
    cleaned_text.strip()
    
    sentences = nltk.sent_tokenize(cleaned_text)
    new_sents = []
    for sent in sentences:
        sent = ' '.join(sent.split())
        if sent:
            print(sent)
            new_sents.append(sent)
            
            
    # print(new_sents)
    
    
    
# def extract_text_from_single_web_page(url):
    
#     downloaded_url = trafilatura.fetch_url(url)
#     try:
#         a = trafilatura.extract(downloaded_url,  output_format="json", with_metadata=True, include_comments = False,
#                             date_extraction_params={'extensive_search': True, 'original_date': True})
#     except AttributeError:
#         a = trafilatura.extract(downloaded_url, json_output=True, with_metadata=True,
#                             date_extraction_params={'extensive_search': True, 'original_date': True})
#     if a:
#         json_output = json.loads(a)
#         return json_output['text']
#     else:
#         try:
#             resp = requests.get(url)
#             # We will only extract the text from successful requests:
#             if resp.status_code == 200:
#                 return beautifulsoup_extract_text_fallback(resp.content)
#             else:
#                 # This line will handle for any failures in both the Trafilature and BeautifulSoup4 functions:
#                 return np.nan
#         # Handling for any URLs that don't have the correct protocol
#         except MissingSchema:
#             return np.nan


# def beautifulsoup_extract_text_fallback(response_content):
    
#     '''
#     This is a fallback function, so that we can always return a value for text content.
#     Even for when both Trafilatura and BeautifulSoup are unable to extract the text from a 
#     single URL.
#     '''
    
#     # Create the beautifulsoup object:
#     soup = bs(response_content, 'html.parser')
    
#     # Finding the text:
#     text = soup.find_all(text=True)
    
#     # Remove unwanted tag elements:
#     cleaned_text = ''
#     blacklist = [
#         '[document]',
#         'noscript',
#         'header',
#         'html',
#         'meta',
#         'head', 
#         'input',
#         'script',
#         'style',]

#     # Then we will loop over every item in the extract text and make sure that the beautifulsoup4 tag
#     # is NOT in the blacklist
#     for item in text:
#         if item.parent.name not in blacklist:
#             cleaned_text += '{} '.format(item)
            
#     # Remove any tab separation and strip the text:
#     cleaned_text = cleaned_text.replace('\t', '')
#     return cleaned_text.strip()
    
    

    