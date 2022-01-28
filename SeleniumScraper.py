import os
import selenium
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import DriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Install Driver
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Firefox(executable_path="F:\PycharmProjects\geckodriver.exe")

#Specify Search URL
search_url= "https://www.simple.co.uk/acts-of-kindness.html"

driver.get(search_url)

#switch to internal frame
driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe'))

#Locate the elements of AoKs to be scraped from the current page
actResults = driver.find_elements(By.XPATH, "//h1[@class='xTitle xHeading']")

for element in actResults:
    print(element.text)

#move to the next page
btnNext = driver.find_element(By.XPATH, "//a[@class='xPagingButton xActionPaginate']")
# driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='xPagingButton xActionPaginate xActionShowNext']"))))
# driver.execute_script("arguments[0].click();", btnNext)
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btnNext)).click()
# WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element(By.XPATH, '//*[@id="ngxFrame911cf8af-4547-4844-9588-8581559255a0"]"')))
# time.sleep(30)
# print(btnNext.tag_name, btnNext.text)

# actResults = driver.find_elements(By.XPATH, "//h1[@class='xTitle xHeading']")

WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,
    '//button[@data-text="Allow"]'))).click()


WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
    '//*[@data-text = "Show More"]'))).click()


actResults = driver.find_elements(By.XPATH, "//h1[@class='xTitle xHeading']")

for element in actResults:
    print(element.text)

# btnNext.click()

driver.quit()


