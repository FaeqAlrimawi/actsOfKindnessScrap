# Importing Libraries
import pandas as pd
from bs4 import BeautifulSoup as bs

pd.set_option('display.max_colwidth', 500)
import requests
import re


# Accessing the Website with requests
# page = requests.get(actsOfKindessWebsiteIdeas)

# soup = bs(page.content)

# text to find act title
# actTitleText = 'line-height-normal font-weight-600 text-small alt-font margin-5px-bottom text-extra-dark-gray text-uppercase d-block'

# Finding the act title
# actTitles = [i.text for i in soup.find_all(class_= actTitleText)]

# Finding the act description using url
# for title in actTitles:
#     titleFormat = title.lower().replace(" ", "-")
#     # print(titleFormat, title)
#     actTitleURLs = soup.find_all('a', attrs={'href': re.compile(titleFormat)})
#     # print(actTitleURLs)


# get links for ideas of acts
actsOfKindessWebsiteIdeas = "https://www.randomactsofkindness.org/kindness-ideas"
page = requests.get(actsOfKindessWebsiteIdeas)
soup = bs(page.content)

actURLs = []
actTitleURLs = soup.find_all('a', attrs={'href': re.compile("/kindness-ideas/")})
baseURL = "https://www.randomactsofkindness.org"
for link in actTitleURLs:
    fullLink = baseURL + link.get('href')
    if fullLink not in actURLs:
        actURLs.append(fullLink)

# prepare file for write
fileName = "actsOfKindness.txt"

f = open(fileName, 'w')
f.write("Title$Description$URL"+'\n')
f.close()
f = open(fileName, 'a')

# get title + description from act URLs
# index 0: title
# the rest of indices: description
for actURL in actURLs:
    page = requests.get(actURL)
    soup = bs(page.content)
    descriptions = [i.text for i in soup.find_all(class_="col-12 blog-details-text last-paragraph-no-margin")]
    # descriptionsArray = descriptions.pop(0).split('\n')
    descriptionsArray =  ''.join(descriptions).split('\n')

    # remove any empty cells
    while "" in descriptionsArray:
        descriptionsArray.remove("")

    # get title
    # actTitle = ""
    if descriptionsArray:
        actTitle = descriptionsArray.pop(0)

    # get description
    wholeDes = ""
    for des in descriptionsArray:
        wholeDes += des + ' '

    # print("title: " + actTitle)
    # print("des: "+ wholeDes)
    # write to file
    # f.write("demofile2.txt", "a")
    f.write(actTitle+"$"+wholeDes+ '$' + actURL + '\n')
    # f.close()

f.close()

print("Done! All acts are saved to file: "+fileName)
