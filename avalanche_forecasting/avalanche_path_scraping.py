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

elems =
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

list_paths = glob.glob('../data/avalanche_path/bessans/*.json')


def create_paths_info(path_fps):

    paths_info = pd.DataFrame()
    for path_fp in path_fps:
        print(path_fp)
        path_info = create_path_info(path_fp)
        site_id = path_fp.split('/')[-1].split('.')[0]
        path_info['site_id'] = site_id
        paths_info = pd.concat([paths_info, path_info])

    return paths_info


def create_path_info(path_fp):

    geo_data = pd.read_csv('../data/geospatial_data/geo_data_bessans.csv')
    geo_data[['lat', 'lon']] = geo_data[['lat', 'lon']].round(4)

    with open(path_fp, 'r') as f:
        info = json.load(f)

    path = pd.DataFrame(info)
    path[['lat', 'lon']] = path['coordinate'].apply(pd.Series)
    path = path.drop('coordinate', axis=1)
    path[['lat', 'lon']] = path[['lat', 'lon']].round(4)


    path_infos = pd.DataFrame()
    for lat, lon in zip(path.lat, path.lon):
        lat_df = geo_data.iloc[np.argmin(np.abs(geo_data['lat'] - lat))].lat
        lon_df = geo_data.iloc[np.argmin(np.abs(geo_data['lon'] - lon))].lon
        spatial_data = geo_data[(geo_data['lat'] == lat_df) & (geo_data['lon'] == lon_df)].rename(columns={'lat': 'lat_1', 'lon': 'lon_1'})
        path_info = pd.concat([path[(path.lat == lat) & (path.lon == lon)].reset_index(drop=True), spatial_data.reset_index(drop=True)], axis=1, sort=True)
        path_infos = pd.concat([path_infos, path_info])

    path_infos.dropna(inplace=True)

    ## assez grosse difference entre altitude du dem et altitude geoportail (autour de 200m)
    ## difference assez eleve quand la pente est raide (logique car dem à 30m)
    ## on utilise la colonne altitude car les données geoportail sont plus précise
    print('diff altitude', (path_infos['altitude'] - path_infos['dem']).mean())
    
    path_infos = path_infos[['altitude', 'pente', 'lat', 'lon', 'slope', 'sin_aspect', 'cos_aspect', 'aspect']]
    
    return path_infos



path_infos = create_paths_info(list_paths)
path_infos.to_csv('../data/avalanche_path/bessans/paths_info.csv', index=False)


same_orientation_side_ids = ['017', '046', '016', '018', '015', '014', '013', '012', '011', '020']



