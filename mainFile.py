# -*- coding: utf-8 -*-
"""
Created on Thu May 04 11:24:37 2017

@author: temp
"""

from bs4 import BeautifulSoup as bs
import urllib2
import re 
import pandas as pd
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait

df = pd.DataFrame(columns = ['Name', 'Points', 'Weight', 'Height'])
UCIRidersURL = 'http://www.procyclingstats.com/rankings.php'
browser = webdriver.Chrome()
for page in range(10):
    browser.get(UCIRidersURL+'?page='+ str(page+1))
    WebDriverWait(browser, 1)
    UCIRidersPage = browser.page_source.encode('utf8')

    states = bs(UCIRidersPage, 'html.parser')
    table = states.find('table', {'class':'basic'})
    
    
    for row in table.tbody.find_all('tr'):
        
        RiderName =  row.find_all('td')[3].text
        Points = int(row.find_all('td')[5].text)
        riderRef = row.find_all('td')[3].a['href']
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        riderPageReg = urllib2.Request('http://www.procyclingstats.com/' + riderRef, headers = hdr)
        riderPage = urllib2.urlopen(riderPageReg).read()
        states = bs(riderPage, 'html.parser')
        try:
            Weight = [tr.contents for tr in states.find_all('span') if tr.find('b') !=None and tr.find('b').text == 'Weight:'][0][1]
            Weight = float(re.findall('(\d*.\d*) kg', Weight)[0])
            Height = [tr.contents for tr in states.find_all('span') if tr.find('b') !=None and tr.find('b').text == 'Height:'][0][1]
            Height = float(re.findall('(\d*.\d*) m', Height)[0])
        except:
            print 'there is no info about weight or height of ' + RiderName
            continue
        df2 = pd.DataFrame([[RiderName, Poins, Weight, Height]], columns = ['Name','Points', 'Weight', 'Height'])
        df = df.append(df2, ignore_index= True)