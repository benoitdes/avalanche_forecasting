#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 21:18:11 2019

@author: plume
"""

import pandas as pd
import numpy as np
from  collections import defaultdict
import urllib
import glob
import datetime

from urllib.request import urlopen
from bs4 import BeautifulSoup



##### DOWNLOAD PDF FROM FTP
def parse_html(url):

    html = urlopen(url)
    soup = BeautifulSoup(html)

    return soup


epa_report_url = 'ftp://avalanchesftp.grenoble.cemagref.fr/epaclpa/EPA_listes_evenements/'
list_region = ['04_ALPES-DE-HAUTE-PROVENCE/'	,	
               '05_HAUTES-ALPES/',
               '06_ALPES-MARITIMES/',
               '09_ARIEGE/',
               '31_HAUTE-GARONNE/',
               '38_ISERE/',
               '64_PYRENEES-ATLANTIQUES/',
               '65_HAUTES-PYRENEES/',
               '66_PYRENEES-ORIENTALES/',
               '73_SAVOIE/',
               '74_HAUTE-SAVOIE/',
               ]

import glob
for region in list_region:
    print(region)
    region_url = f'{epa_report_url}/{region}'
    soup = parse_html(region_url)
    text = soup.text
    region_pdf = [word for word in text.split() if 'pdf' in word and 'EPA' in word]
    for pdf in region_pdf:
        print(pdf)
        if not glob.glob(f'data/epa_reports/{pdf}.pdf'):
            urllib.request.urlretrieve(f'{region_url}/{pdf}', f'data/epa_reports/{pdf}')




urllib.request.urlretrieve('http://vmapfishbda.grenoble.cemagref.fr/cgi-bin/mapserv?map=/var/www/prod/affichage_epa.map&LAYERS=talweg_branche&TRANSPARENT=true&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&EXCEPTIONS=application%2Fvnd.ogc.se_inimage&FORMAT=image%2Fpng&SRS=EPSG%3A27572&BBOX=968321.56043969,2047659.1795974,969221.14328725,2048558.7624449&WIDTH=340&HEIGHT=340', 'test')







## CONVERT PDF TO XLSX USING ILOVEPDF WEBSITE


import glob
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import time
import json
from collections import defaultdict



import os
url = 'https://www.ilovepdf.com/pdf_to_excel'

chrome_options = webdriver.ChromeOptions()
options = webdriver.ChromeOptions() 
download_fp = '/Users/plume/Desktop/divers/perso/avalanche_forecasting/data/epa_reports/xlsx'
prefs = {'download.default_directory' : download_fp}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(30)
driver.get(url)



for file in glob.glob('data/epa_reports/pdf/*'):
    try:
        print(file)
        xlsx_file = file.split('/')[-1].replace('pdf', 'xlsx')
        if glob.glob(f'{download_fp}/{xlsx_file}*'):
            print('file already exists')
            continue
    

        #button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='file']")))
        button = driver.find_element_by_xpath("//input[@type='file']")
        button.send_keys(os.path.join(os.getcwd(), file))
    
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='processTask']")))
        driver.execute_script("arguments[0].click();", element)
    
        while not os.path.exists(os.path.join(download_fp, xlsx_file)):
            time.sleep(1)
            print('Waiting for files to download...')
    
        button = driver.find_element_by_xpath("//a[@href='https://www.ilovepdf.com/pdf_to_excel']")
        button.click()
    except:
        chrome_options = webdriver.ChromeOptions()
        options = webdriver.ChromeOptions() 
        download_fp = '/Users/plume/Desktop/divers/perso/avalanche_forecasting/data/epa_reports/xlsx'
        prefs = {'download.default_directory' : download_fp}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.implicitly_wait(30)
        driver.get(url)





