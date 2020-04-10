import requests
from bs4 import BeautifulSoup
# imports
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
SIGNURL='http://fae.plustek.com/adm/index.php?ex=O'
URL='http://fae.plustek.com/adm/srhcase.php?page=detail&caseId=80999'
#page = requests.get(URL)
#print(page.content)
#print('souping...')
#soup = BeautifulSoup(page.content, 'html.parser')
#results = soup.find(lambda tag:"Problem Description" in tag.text)
#print(results)

# chrome
option = webdriver.ChromeOptions()
browser = webdriver.Chrome(executable_path='C:\\Users\\qw\\Downloads\\chromedriver_win32', chrome_options=option)
browser.get(URL)
timeout = 20
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='avatar width-full rounded-2']")))
except TimeoutException:
    print('Timed out waiting for page to load')
    browser.quit()