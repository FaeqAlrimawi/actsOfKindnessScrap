import os
import selenium
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By

#Install Driver
driver = webdriver.Chrome(ChromeDriverManager().install())

#Specify Search URL
search_url= "https://www.simple.co.uk/acts-of-kindness.html"

driver.get(search_url)

#Locate the images to be scraped from the current page
imgResults = driver.find_elements(By.XPATH, "/html/body/div[1]/div/main/section[1]/div/div[3]/div/div/div/div[2]/div/div[3]/div/div/div[1]/div/div[1]/h1")
# imgResults = driver.find_elements_by_xpath('//td[@class="name"]')
totalResults=len(imgResults)

print(len(imgResults))

driver.quit()


