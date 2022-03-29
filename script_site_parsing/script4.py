import requests
import random
from bs4 import BeautifulSoup
import os
import time
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

folder_path = '/home/wym/pj3a/image_voitures'
page_index = 1
div_class = 'img ergov3-imgannonce'
title_class = 'sc-gGBfsJ dfVwVQ'
url = 'https://www.paruvendu.fr/auto-moto/listefo/default/default?auto-typeRech=&reaf=1&r2=&px1=&md=&codeINSEE=&lo=&pa=&ray=15&r=VVO00000&r1=&trub=&nrj=&km1=&co2=&a0=&a1=&npo=0&tr=&pf0=&pf1=&fulltext=&codPro=&p='+str(page_index)
profile = webdriver.FirefoxProfile('/home/wym/.mozilla/firefox/lpxxevpm.default-release')

PROXY_HOST = "12.12.12.123"
PROXY_PORT = "1234"
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", PROXY_HOST)
profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
# desired = desired_capabilities.FIREFOX

# driver = webdriver.Firefox(firefox_profile=profile)
# driver = webdriver.Firefox()

def searchend():
    
        for i in range(80):
             driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)
             time.sleep(0.1)





headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0', 
            'Referer' : 'https://www.leboncoin.fr/recherche?category=2',
            'Origin': 'https://www.leboncoin.fr/recherche?category=2'}


def find_img(url) :
    titles = []
    srcs = []
    driver.get(url)
    searchend()
    soup = BeautifulSoup(driver.find_element_by_css_selector("body").get_attribute("innerHTML"), 'html.parser')
    # div_items = soup.find_all('div',class_=div_class)
    for reqa in soup.findAll('div', attrs={'class':div_class}):
        for img in reqa.findAll('img'):
            try:
                titles.append(img.attrs['alt'])
                srcs.append(img.attrs['src'])
            except:
                pass
    return titles,srcs

def down_load(titles,srcs):
    index = 0
    for item in enumerate(srcs):
        if item : 
            print(item)
            html = requests.get(item[1])
            img_name = titles[index] + str(index) +'.jpg'  
            with open(img_name,'wb') as file :
                file.write(html.content)
                file.close()
                index = index+1
            print("downloaded pic"+str(index))
            time.sleep(1)
    driver.close()                  #close the window after downloading

max_page = input("please input the max page you want")

while (int(page_index)<=int(max_page)) :
    driver = webdriver.Firefox(firefox_profile=profile)
    titles, srcs = find_img(url)
    down_load(titles,srcs)
    page_index = page_index+1
    url = 'https://www.paruvendu.fr/auto-moto/listefo/default/default?auto-typeRech=&reaf=1&r2=&px1=&md=&codeINSEE=&lo=&pa=&ray=15&r=VVO00000&r1=&trub=&nrj=&km1=&co2=&a0=&a1=&npo=0&tr=&pf0=&pf1=&fulltext=&codPro=&p='+str(page_index)
