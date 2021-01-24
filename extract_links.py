from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import sys

arg_v = sys.argv

browser = webdriver.Chrome('chromedriver.exe')
hashtags=arg_v[1:]
print("BREAK POINT---------------------",hashtags)



for hashtag in hashtags:
    browser.get('https://www.instagram.com/explore/tags/'+hashtag)
    #a=input()
    accept_cookies = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button[1]')
    print("BREAK POINT---------------------",accept_cookies)
    accept_cookies.click()
    #Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    Pagelength = browser.execute_script("return document.documentElement.scrollHeight")
    browser.execute_script("window.scrollTo(0, " + str(Pagelength) + ");")
    print(Pagelength)
    source = browser.page_source
    f=open(hashtag+".txt",'w+')
    data=bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)
    for link in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
        f.write('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/'+'\n')
    f.close()
#print(links)