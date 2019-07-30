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


#### NEED TO FIND A WAY TO CONVERT PDF TO XLSX OR OTHER WAY TO TRANSFORM PDF TO PANDAS DATAFRAME






### CREATE DATASET FROM XLSX

xlsx_file = 'data/epa_reports/EPA_ListeEvts_04006_ALLOS.xlsx'


xl = pd.ExcelFile(xlsx_file)
xl.sheet_names
final_res = pd.DataFrame()

for page in xl.sheet_names:
    print(page)
    if True: #try:
        df = xl.parse(page) 
        df.columns = ['first_col'] + list(df.columns[1:])
        
        for i in range(len(df)):
            #print(i)
            try:
                if 'id' in df.iloc[i]['first_col']:
                    start_index = i
                    break
            except TypeError:
                pass #print('nan value')
        
        df = df.iloc[start_index + 1:]
        
        start_event = []
        for i in range(len(df)):
            #print(i)
            try:
                if 'n°' in df.iloc[i]['first_col']:
                    start_event.append(i)
            except TypeError:
                pass #print('nan value')
        #print(df.shape)
        #print(df['Unnamed: 6'], df['Unnamed: 7'], df['Unnamed: 8'], df['Unnamed: 9'], df['Unnamed: 10'])
        
        info = defaultdict(list)
        for i in range(len(start_event)-1):
            data_event = df.iloc[start_event[i] : start_event[i + 1]]
            #if len(data_event) < 3:
            #    print('not enough information')
            #    continue
            info['page'].append(page)
            info['site_id'].append(data_event['first_col'].iloc[0])
            info['numero_id'].append(data_event['first_col'].iloc[1])
            try:
                info['date_constat'].append(data_event['first_col'].iloc[2])
            except:
                info['date_constat'].append(np.nan)
            info['date_1'].append(data_event['Unnamed: 1'].iloc[0])
            info['date_2'].append(data_event['Unnamed: 2'].iloc[0])
            info['altitude_depart'].append(data_event['Unnamed: 4'].iloc[0])
            info['altitude_arrivee'].append(data_event['Unnamed: 5'].iloc[0])
            if df.shape[1] in [44, 45]:
                info['longueur'].append(data_event['Unnamed: 7'].iloc[0])
                info['largeur'].append(data_event['Unnamed: 9'].iloc[0])
                info['hauteur'].append(data_event['Unnamed: 10'].iloc[0])
            elif df.shape[1] == 43:
                info['longueur'].append(data_event['Unnamed: 6'].iloc[0])
                info['largeur'].append(data_event['Unnamed: 8'].iloc[0])
                info['hauteur'].append(data_event['Unnamed: 9'].iloc[0])
            elif df.shape[1] == 46:
                info['longueur'].append(data_event['Unnamed: 8'].iloc[0])
                info['largeur'].append(data_event['Unnamed: 9'].iloc[0])
                info['hauteur'].append(data_event['Unnamed: 10'].iloc[0])
            else:
                print(df.shape)

        res_page = pd.DataFrame(info)        
        final_res = pd.concat([final_res, res_page])    
    else:#except:
        print(f'error for {page}')
    




