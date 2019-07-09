#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 22:00:09 2019

@author: plume
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

def parse_html(url):

    html = urlopen(url)
    soup = BeautifulSoup(html)

    return soup


def get_avalanche_info(soup_object):

    q = soup.find_all('script')[1]
    a = q.get_text()
    b = a.split('var avalanche = ')[1]
    c = b[len('JSON.parse(\\'):][:-6]
    c = c.replace(r'\"', '"').replace(r'\"', '"')
    info = json.loads(c)
    return info


def save_avalanche_info(dic_data):

    id_info = dic_data['id']
    with open(f'data_avalanche_report/avalanche_{id_info}.json', 'w') as f:
        json.dump(dic_data, f)


#### save information from data-avalanche.org ####

from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import json
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://www.data-avalanche.org/explore?winter=all')
time.sleep(10) # wait for page to load   
links = driver.find_elements_by_xpath("//a[@href][@target]")
good_links = []
for link in links:
    if 'avalanche' in link.get_attribute('href'):
        good_links.append(link)

report_fp = 'data_avalanche_report'


already_downloaded_reports = []
for path in Path(report_fp).glob('*.json'):
    already_downloaded_reports.append(str(path).split('_')[-1].split('.')[0])

for link in good_links:
    url = link.get_attribute('href')
    avalanche_id = url.split('/')[-1]
    if avalanche_id in already_downloaded_reports:
        print('ALREADY DOWNLOADED')
        continue
    time.sleep(2)
    print(url)
    soup = parse_html(url)
    dic_data = get_avalanche_info(soup)
    save_avalanche_info(dic_data)


KEYS = ['id',
        'pays',
        'massif',
        'sommet', 
        'itineraire', 
        'orientation', 
        'dateEvenement', 
        'dateAvalanche', 
        'heureAuPlusTot', 
        'description', 
        'declenchement_a_distance', 
        'distance_declenchement', 
        'caracteristique', 
        'denivele', 
        'origine_principale', 
        'origine_secondaire', 
        'altitude_depart', 
        'commentaire_zone_depart', 
        'epaisseur_rupture', 
        'epaisseur_max_rupture', 
        'longueur_rupture', 
        'type_ecoulement_principal', 
        'commentaire_type_ecoulement', 
        'altitude_arrivee', 
        'commentaire_zone_arrivee', 
        'qualite_neige', 
        'commentaire_qualite_neige', 
        'commentaire_qualite_transportee', 
        'risque_meteo_france', 
        'latitude', 
        'longitude', 
        'localisation', 
        'url_description', 
        'legalFilesPublic', 
        'draft', 
        'isPrivate', 
        'organisation', 
        'tags', 
        'updated', 
        'isSlab', 
        'isTriggeredBySkier']


