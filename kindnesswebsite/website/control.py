import pickle
from sre_constants import FAILURE, SUCCESS
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from bs4 import BeautifulSoup as bs
import requests
import re
import nltk
from sqlalchemy import true
import trafilatura
import json
import numpy as np
from requests.models import MissingSchema
from .models import AoK
from . import db
from flask_login import current_user
import urllib.robotparser as urobot
from urllib.parse import urlparse


model = None

features_file = None

loaded_vec = None


def addAoK(aok):
    if len(aok)<1:
        return False
    
    else:
        new_aok = AoK(act=aok, user_id=current_user.id)
        db.session.add(new_aok)
        db.session.commit()
        return True
    
    
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
    # text = soup.find_all("<li>")
    sents = soup.find_all(text=True)
    sents = processWebsiteScrapText(sents)
    return sents
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
            # print(sent)
            new_sents.append(sent)
            
    return new_sents        
    # print(new_sents)
    


def getSiteMap(url):
    rp = urobot.RobotFileParser()
    baseURL = getBaseURL(url)
    
    rp.set_url(baseURL + "/robots.txt")
    rp.read()
    return rp.site_maps()
    
    
def canScrap(url):
    rp = urobot.RobotFileParser()
    
    baseURL = getBaseURL(url)
     
    robotsURL = baseURL + "/robots.txt"
      
    rp.set_url(robotsURL)
    
    rp.read()
    
    parsedURL = urlparse(url)
    
    path = parsedURL.path  
   
   ## almost always this returrns false
    print("######## ", url, " ", rp.can_fetch("*", url))
    return rp.can_fetch("*", url)
      
        
    
def getBaseURL(url):
    parsedURL = urlparse(url)
    
    base = parsedURL.scheme + "://"+ parsedURL.netloc
    
    return base

def getRobotsURL(url):
    
    return getBaseURL(url) + "/robots.txt"
    
    