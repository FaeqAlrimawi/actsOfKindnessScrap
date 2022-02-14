import os
import tweepy as tw
import pandas as pd

# consumer_key= 'WCkTnaWJprWhQZxvT4HqYiTP1'
# consumer_secret= 'R01BIDUjukLUparRNWyjMfLhfezNnuBD2DgF2HQ0ZVf5ubkH8o'
# access_token= '1493262450145255428-zdBAyo9lgx9hve5x4msklLEkL7zQLX'
# access_token_secret= 'X8vGwdXwTzqPcW2mm6CCVrJ4ZElZFWYQzEuhCy6lZk3EF'
#
# auth = tw.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tw.API(auth, wait_on_rate_limit=True)
#
#
# # Post a tweet from Python
# # api.update_status("Look, I'm tweeting from #Python in my #earthanalytics class! @EarthLabCU")
# # Your tweet has been posted!
#
# # Define the search term and the date_since date as variables
# search_words = "#cat"
# date_since = "2018-11-16"
#
# # Collect tweets
# tweets = tw.Cursor(api.search_tweets,
#               q=search_words,
#               lang="en",
#               since=date_since).items(5)
#
#
# # Iterate and print tweets
# for tweet in tweets:
#     print(tweet.text)

# import requests
# from bs4 import BeautifulSoup
#
# class TwitterHashTagPosts:
#
#     def __init__(self, hashtag):
#         self.hashtag = hashtag
#         self.tweets = []
#         self.url = "https://mobile.twitter.com/hashtag/" + self.hashtag.strip()
#
#     def scrape_tweets(self):
#         content = requests.get(self.url)
#         print("content", content.text)
#         soup = BeautifulSoup(content.text, "html.parser")
#         print(soup.select("#main_content"))
#         tweet_divs = soup.select("#main_content")[0].select(".tweet")
#         for tweet in tweet_divs:
#             handle = tweet.find("div", {"class": "username"}).text.replace("\n", " ").strip()
#             post = tweet.find("div", {"class": "tweet-text"}).text.replace("\n", " ").strip()
#             self.tweets.append({handle: post})
#         return self.tweets
#
# x = TwitterHashTagPosts("tiktokrating")
# x.scrape_tweets()

# import requests
# import json
#
# bearer_token = "AAAAAAAAAAAAAAAAAAAAAPnuZAEAAAAACQaG7SsZlhKKV%2BkMXQhbkGlpteg%3DtNee2itBr9NyLly1R9qgY7w1yFm2icgbLBIAV4LILZ63JgLIln"
# url = "https://api.twitter.com/2/tweets/search/recent?query="
# twitter_params = "kindness"
# url = url + twitter_params
#
#
# headers = {"Authorization": "Bearer {}".format(bearer_token)}
# response = requests.request("GET", url, headers=headers)
# res_json = response.json()
# print(res_json)
#
# next_token = print(res_json["meta"]["next_token"])
#
# headers = {"Authorization": "Bearer {}".format(bearer_token)}
# response = requests.request("GET", url, headers=headers)
# res_json = response.json()
# print(res_json)

# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time

# os.environ['TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAPnuZAEAAAAACQaG7SsZlhKKV%2BkMXQhbkGlpteg%3DtNee2itBr9NyLly1R9qgY7w1yFm2icgbLBIAV4LILZ63JgLIln'


def auth():
    return 'AAAAAAAAAAAAAAAAAAAAAPnuZAEAAAAACQaG7SsZlhKKV%2BkMXQhbkGlpteg%3DtNee2itBr9NyLly1R9qgY7w1yFm2icgbLBIAV4LILZ63JgLIln'


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(keyword, start_date, end_date, max_results=10):
    search_url = "https://api.twitter.com/2/tweets/search/all"  # Change to the endpoint you want to collect data from

    # change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()



#Inputs for the request
bearer_token = auth()
headers = create_headers(bearer_token)
keyword = "xbox lang:en"
start_time = "2021-03-01T00:00:00.000Z"
end_time = "2021-03-31T00:00:00.000Z"
max_results = 15

url = create_url(keyword, start_time,end_time, max_results)

json_response = connect_to_endpoint(url[0], headers, url[1])

print(json.dumps(json_response, indent=4, sort_keys=True))
