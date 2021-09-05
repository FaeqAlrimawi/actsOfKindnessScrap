# Importing Libraries
import pandas as pd
from bs4 import BeautifulSoup as bs

pd.set_option('display.max_colwidth', 500)
import requests
import re


def get_act_details(act_url):
    page = requests.get(act_url)
    soup = bs(page.content)

    actURLs = []
    actTitleURLs = soup.find_all('a', attrs={'href': re.compile("/kindness-stories/")})
    baseURL = "https://www.randomactsofkindness.org"
    for link in actTitleURLs:
        fullLink = baseURL + link.get('href')
        if fullLink not in actURLs:
            actURLs.append(fullLink)

    # print(actURLs)
    #
    # prepare file for write
    # file_name = "actsOfKindnessStories.txt"

    f = open(file_name, 'a', encoding='utf8')
    # f.write("Title$Description" + '\n')
    # f = open(fileName, 'a')

    # get title + description from act URLs
    # index 0: title
    # the rest of indices: description
    for actURL in actURLs:
        page = requests.get(actURL)
        soup = bs(page.content)
        descriptions = [i.text for i in soup.find_all(class_="col-12 blog-details-text last-paragraph-no-margin")]
        # descriptionsArray = descriptions.pop(0).split('\n')
        descriptionsArray = ''.join(descriptions).split('\n')

        # remove any empty cells
        while "" in descriptionsArray:
            descriptionsArray.remove("")

        # get title
        actTitle = ""
        if descriptionsArray:
            actTitle = descriptionsArray.pop(0)

        # get description
        wholeDes = ""
        for des in descriptionsArray:
            wholeDes += des + ' '

        print("title: " + actTitle)
        print("des: " + wholeDes)
        # write to file
        f.write(actTitle + "$" + wholeDes + "$" + actURL + '\n')
        # f.close()

    f.close()


file_name = "actsOfKindnessStories.txt"
f = open(file_name, 'w', encoding='utf8')
f.write("Title$Description$URL\n")
f.close()

# get links for stories of acts
actsOfKindessWebsiteStories = "https://www.randomactsofkindness.org/kindness-stories?page="
actsOfKindessWebsiteStoriesURLs = []

# get all pages (1-102)
for i in range(1, 103):

    print("########################################\ndoing page: " + str(i))
    get_act_details(actsOfKindessWebsiteStories+str(i))



