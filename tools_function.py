#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 22:30:53 2018

@author: plume
"""
import pandas as pd
import datetime
import numpy as np
import urllib
import os

import matplotlib.pyplot as plt

import matplotlib.ticker as ticker
import matplotlib.cm as cm

idx = pd.IndexSlice

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
    return {k: [info[k]] for k in keys}

    

#### populate a pandas dataframe with data from data-avalanche.org ####

final_data = pd.DataFrame()
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import json
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://www.data-avalanche.org/explore?winter=2018')
links = driver.find_elements_by_partial_link_text('avalanche')
for link in links[:20]:
    time.sleep(2)
    url = link.get_attribute('href')
    soup = parse_html(url)
    dic_data = get_avalanche_info(soup)
    data = pd.DataFrame(dic_data)
    final_data = final_data.append(data)


keys = ['id',
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






### downoad BRA 




    
import glob
report_downloaded(zone, date)  
zone = 'CHABLAIS'
date = '04142016'
print(f'../avalanche_forecasting/avalanche_report/{zone}_{date}.xml')
    


driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(url)

       
scrap_avalanche_report(driver, date_to_scrap, '../avalanche_forecasting/avalanche_report')


################################################
#### Get infomration from XML BRA ###########
################################################
################################################
     


    
import xml.etree.ElementTree as ET
import pandas as pd
import glob
final_bra_data = pd.DataFrame()


for bra_fp in glob.glob('bra_test/*'):
    print(bra_fp)
    tree = ET.parse(bra_fp)
    root = tree.getroot()
    info_xml = root[0].attrib

    try:
        risque = root[0].findall('CARTOUCHERISQUE')[0]
    except Exception:
        print(f'NO CARTOUCHERISQUE AVAILABLE FOR {bra_fp}')
        continue

    cartoucherisque_element = ['PENTE',
                               'RISQUE',
                               'ACCIDENTEL',
                               'NATUREL',
                               'AVIS',
                               'VIGILANCE']

    for elem in cartoucherisque_element:
        xml_elem = risque.findall(elem)[0].attrib
        if type(xml_elem) is dict:
            for key, val in xml_elem.items():
                info_xml[key] = val
        else:
            info_xml[elem] = xml_elem

    text_elements = ['STABILITE',
                      'QUALITE']
                  
    for elem in text_elements:

        info_xml[elem] = root[0].findall(elem)[0].findall('TEXTE')[0].text

    for xml_elem in ['ENNEIGEMENT']:
        for elem, val in root[0].findall(xml_elem)[0].attrib.items():
            if elem == 'DATE':
                elem = f'{elem}_MESURE_LIMITE_ENNEIGEMENT'
            info_xml[elem] = val
    
    for xml_elem in ['TENDANCES']:
        for child in root[0].findall(xml_elem)[0]:
            for elem, val in child.attrib.items():
                elem = f"{elem}_TENDANCE_RISQUE"
                info_xml[elem] = val
            

    for key in info_xml.keys():
        info_xml[key] = [info_xml[key]]

    bra_data = pd.DataFrame(info_xml)

    final_bra_data = final_bra_data.append(bra_data)


#########################################
#########################################
#########################################
#########################################


def download_data():
        
    url_to_nivo_data = 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Nivo/'


    list_month = ['0'+str(i) for i in range(1,10)] + [str(i) for i in range(10,13)]

    for ayear in np.arange(2010,2019,1) :
        for amonth in list_month :
            print(str(ayear)+amonth)
            urllib.request.urlretrieve(url_to_nivo_data+'Archive/nivo.'+str(ayear)+amonth+'.csv.gz',
                                   'data/'+str(ayear)+amonth+'.gz')
            try :
                _ = pd.read_csv('data/'+str(ayear)+amonth+'.gz',delimiter=';')
            except Exception:
                print('no data available for '+str(ayear)+amonth)
                os.remove('data/'+str(ayear)+amonth+'.gz')

    

def create_dataset(list_year,list_month) :
    
    res = pd.DataFrame()
    for ayear in list_year :
        for amonth in list_month :
            try :
                data_loaded = pd.read_csv('data/'+str(ayear)+amonth+'.gz',delimiter=';')
                res = pd.concat([res,data_loaded])
            except :
                print('no data available for',ayear+amonth)
            
    res = res[res['date'] != 'date']
    res['date'] = res['date'].apply(lambda x : datetime.datetime.strptime(str(x)[:10], '%Y%m%d%H'))

    #select only month between november and april
    res['month'] = res['date'].apply(lambda x : x.month)
    res = res[res['month'].isin([11, 12, 1, 2, 3, 4])]

    res.replace('mq',np.nan,inplace=True)

    station_infos = pd.read_csv('data/postesNivo.csv').dropna()
    res['numer_sta'] = res['numer_sta'].astype('int64')
    
    res = res.merge(station_infos,on='numer_sta')
    
    #drop not usefull feature
    res.drop(['month', 'ww','w2','w1','cl','cm','ch',
              'nnuage1','nuage_val','etat_neige',
              'phenspe2','perssfrai','phenspe1','numer_sta','nbas','n','haut_sta'], 
            axis=1,
            inplace=True)

    #keep only cols where at least 80 percent of values are not nan except for aval_risque
    res = select_cols(res, threshold=0.8)
    
    #deal with error linked to type of data
    res = put_type_float(res)
    
    #keep one observation per day/station
    res = res.groupby('Nom').resample('1D', level=1).min().dropna(how='all')

    #keep stations where at least 50 observations
    res = station_enough_obs(res, threshold=50)

    #delete row where aval_risque equal to 0 (not normal)
    res = res[res['aval_risque'] != 0]

    return res


def station_enough_obs(data, threshold):

    df_bool = (data.groupby(level=0).size()>50)
    good_stat = df_bool[df_bool == True].index
    data = data.loc[idx[good_stat, :], :]

    return data


def select_cols(data, threshold):
    
    selected_cols = list(set(data.columns)-set(['aval_risque']))
    good_data = data[selected_cols].dropna(thresh=int(len(data)*threshold),axis=1)
    good_cols = good_data.columns.tolist()
    good_cols += ['aval_risque']
    data = data[good_cols]
    
    return data
    

def put_type_float(data):
    
    new_data = pd.DataFrame()    
    for acol in list(set(data.columns)-set(['Nom','date'])) :
        new_data = pd.concat([new_data,pd.DataFrame(data[[acol]].values.astype(float),columns=[acol])],axis=1)            

    new_data = pd.concat([data[['Nom', 'date']], new_data], axis=1)
    
    new_data.dropna(subset=['Nom','date'],inplace=True)
    new_data = new_data.sort_values(['Nom','date'])
    new_data = new_data.set_index(['Nom','date'])
    
    return new_data
    

def plot_correlation(data, feature=[]):
    
    if feature == [] :
        feature = data.columns.tolist()
        
    data = data[feature]
        
    fig, ax = plt.subplots()
    cmap = cm.get_cmap('jet', 30)

    cax = ax.matshow(data.corr(), cmap=cmap)
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[1]))
    ax.set_xticklabels(feature)
    ax.set_yticklabels(feature)
    
    ax.xaxis.set_ticks_position('bottom')
    
    plt.xticks(rotation=70)
    plt.colorbar(cax)
    plt.title('Correlation between different features')
    
    
