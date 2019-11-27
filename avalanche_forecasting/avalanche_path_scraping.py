#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:52:09 2019

@author: plume
"""

### Get elevation profile of each avalanche_path

### To do so, you need to use geoportail, type the name of the city, find the
### avalanche path, trace the elevation profile with proposed tools and 
### use the code below



from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import json
from collections import defaultdict
import os



url = 'https://www.geoportail.gouv.fr/carte'

chrome_options = webdriver.ChromeOptions()
options = webdriver.ChromeOptions() 
driver = webdriver.Chrome()
driver.implicitly_wait(2)
driver.get(url)



## before that, you need to create the elevation profile on geoportail

elems = driver.find_elements_by_xpath("//*[name()='svg']//*[name()='circle']")

altitudes = []
pentes = []
coords = []
for i, elem in enumerate(elems, start=1):
    hov = ActionChains(driver).move_to_element(elem)
    hov.perform()
    print(f'get element number {i}')
    a = driver.find_elements_by_xpath('//*[@class="altiPathValue"]')
    if not a:
        print('empty')
        continue
    altitudes.append(float(a[0].text.split(':')[1][:-2].replace(',', '.').replace(' ', '')))
    pentes.append(int(a[1].text.split(':')[1][:-1].replace(' ', '')))
    coord = driver.find_element_by_xpath('//*[@class="altiPathCoords"]').text
    lat, lon = coord.split('/')
    lat = float(lat.split(':')[-1].replace(' ', ''))
    lon = float(lon.split(':')[1].replace(')', ''))
    coord = [lat, lon]
    coords.append(coord)


## save avalanche path info into json
site_id = '205'

with open(f'../data/avalanche_path/bessans/{site_id}.json', 'w') as f:
    json.dump({'altitude': altitudes, 'pente': pentes, 'coordinate': coords}, f)


with open(f'../data/avalanche_path/bessans/{site_id}.json', 'r') as f:
    a = json.load(f)

## start exploring avalanche path data

import glob
import json
import pandas as pd
import numpy as np

paths = glob.glob('../data/avalanche_path/bessans/*')

with open(paths[0], 'r') as f:
    info = json.load(f)

geo_data = pd.read_csv('../data/geospatial_data/geo_data_bessans.csv')
geo_data[['lat', 'lon']] = geo_data[['lat', 'lon']].round(4)

for lat, lon in info['coordinate'][:-1]:
    lat_df = geo_data.iloc[np.argmin(np.abs(geo_data['lat'] - lat))].lat
    lon_df = geo_data.iloc[np.argmin(np.abs(geo_data['lon'] - lon))].lon
    print(geo_data[(geo_data['lat'] == lat_df) & (geo_data['lon'] == lon_df)])

geo_data[geo_data['lat'] == 45.307700]

geo_data.iloc[(geo_data['lat'] - lat).abs().argsort()[0]]


a = 6.9785
round(a, 3)





