import os
import selenium
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException

#Install Driver
driver = webdriver.Chrome(ChromeDriverManager().install())

#Specify Search URL
search_url= "https://www.simple.co.uk/acts-of-kindness.html"

#Locate the images to be scraped from the current page
imgResults = driver.find_elements_by_xpath("//h1[@class='xTitle xHeading']")
totalResults=len(imgResults)

print(totalResults)



