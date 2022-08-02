from genericpath import exists
from multiprocessing.dummy import active_children
import pickle
from sre_constants import FAILURE, SUCCESS
from xmlrpc.client import Boolean
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from bs4 import BeautifulSoup as bs
import requests
import re
import nltk
from sqlalchemy import true, exists
import trafilatura
import json
import numpy as np
from requests.models import MissingSchema
from .models import Aok
from . import db
from flask_login import current_user
import urllib.robotparser as urobot
from urllib.parse import urlparse
import urllib.request
import ssl


model = None

features_file = None

loaded_vec = None


def addAoK(aok):
    if len(aok)<1:
        return False
    
    else:
        new_aok = Aok(act=aok, user_id=current_user.id)
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
    


def getSiteMaps(url):
    rp = urobot.RobotFileParser()
    baseURL = getBaseURL(url)
    
    rp.set_url(baseURL + "/robots.txt")
    # print(baseURL + "/robots.txt")
    rp.read()
    
    all_sitemaps = []
    
    all_sitemaps = rp.site_maps()
    
    #  baseURL = getBaseURL(url)
     
    # robotsURL = baseURL + "/robots.txt"
    # xmlDict = {}
  
    if not all_sitemaps:
        #try sitemap.xml with base url
        all_sitemaps = [baseURL + "/sitemap.xml"]
       
    # more_sitemaps = []  
    #does it have more sitemaps in the basic sitemap.xml
    for sitemap in all_sitemaps:
        more_sitemaps = check_has_more_sitemaps(sitemap)
        
     
    if more_sitemaps:
        all_sitemaps = more_sitemaps
        
    # if all_sitemaps:
    #     sitemaps = all_sitemaps
       
        
    urls = {}
    for sitemap in all_sitemaps:
        # print("sitemap: ", sitemap)
        out = parse_sitemap(sitemap)
        
        if out:
            urls[sitemap] = out
        
    # print(urls)    
    return urls
   
    
 
def parse_sitemap(sitemapURL):

    resp = requests.get(sitemapURL)

    # we didn't get a valid response, bail
    if 200 != resp.status_code:
        return False

    # BeautifulStoneSoup to parse the document
    soup = bs(resp.content, features='xml')


    # find all the <url> tags in the document
    urls = soup.findAll('url')

    # no urls? bail
    if not urls:
        return False

    # storage for later...
    out = []

    #extract what we need from the url
    for u in urls:
        loc = u.find('loc').string if u.find('loc') else None

        # skips url if its path is not potentially one that has kindness acts
        if not loc or not is_potentially_kindness_url(loc):
            continue
            
        prio =  u.find('priority').string if u.find('priority') else None 
        change = u.find('changefreq').string if u.find('changefreq') else None
        last = u.find('lastmod').string if u.find('lastmod') else None
        out.append([loc, prio, change, last])
        
    return out


def check_has_more_sitemaps(sitemap):
    
    resp = requests.get(sitemap)

    # we didn't get a valid response, bail
    if 200 != resp.status_code:
        return False

    # BeautifulStoneSoup to parse the document
    soup = bs(resp.content, features='xml')


    # find all the <url> tags in the document
    urls = soup.findAll('sitemap')
    
     # no urls? bail
    if not urls:
        return False

    # storage for later...
    out = []

    #extract what we need from the url
    for u in urls:
        loc = u.find('loc').string if u.find('loc') else None
        out.append(loc)
        
    return out

    return
    
def get_kindness_urls(urls):
    ### processes the given urls to return the top most related to kindness
    ### that be: onces that mention acts of kindness (preferrably as a whole unit) or just kindness in the path (not the base)
    
    filteredURLs = []
    
    for url in urls:
        if is_potentially_kindness_url(url):
            filteredURLs.append(url)
            
    return filteredURLs
   
    
def is_potentially_kindness_url(url): 
    ### checks if the given url is potentially good to look for aoks
    ### criteria: onces that mention acts of kindness (preferrably as a whole unit) or just kindness in the path (not the base)
    parsedURL = urlparse(url)
    
    path = str(parsedURL.path)
    
    matches =["kindness", "kind-", "kind_", "aok","act-of-kindness","act_of_kindness", "acts-of-kindness", "acts_of_kindness", "kindness-acts", "kindness_acts", "kindness-act", "kindness_act"]
    
    if path:
       # contains kindness word
       if any(x in path for x in matches):
           return True
    
    return False  
 
 
            
def canScrap(url):
    rp = urobot.RobotFileParser()
    
    baseURL = getBaseURL(url)
     
    robotsURL = baseURL + "/robots.txt"
      
    rp.set_url(robotsURL)
    
    rp.read()
    
    # parsedURL = urlparse(url)
    
    # path = parsedURL.path  
   
   ## almost always this returrns false
    # print("######## ", url, " ", rp.can_fetch("*", url))
    return rp.can_fetch("*", url)

      
        
    
def getBaseURL(url):
    parsedURL = urlparse(url)
    
    base = parsedURL.scheme + "://"+ parsedURL.netloc
    
    return base

def getRobotsURL(url):
    
    return getBaseURL(url) + "/robots.txt"
    

def doesAoKExist(aokDescription):
    
   res = db.session.query(exists().where(Aok.act==aokDescription)).scalar()  
   
#    if aokDescription.contains("RAK"):
   print("### res checking ", aokDescription, ": ", res)  
   return res