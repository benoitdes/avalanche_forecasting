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
    html = urlopen(url)
    soup = BeautifulSoup(html)
    q = soup.find_all('script')
    q = q[1]
    a = q.get_text()
    b = a.split('var avalanche = ')[1]
    c = b[len('JSON.parse(\\'):]
    c = c[:-6]
    c = c.replace(r'\"', '"').replace(r'\"', '"')    
    final = json.loads(c)
    new_dict = {k: [final[k]] for k in keys}
    print(new_dict)
    data = pd.DataFrame(new_dict)
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

url = 'https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=265&id_rubrique=50'
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import time
import json
from collections import defaultdict
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(url)


################################################
#### find available date ###########
################################################
################################################

driver.find_element_by_xpath("//div[@class='publication-info telechargements replie']/h3[contains(., 'Téléchargement')]").click()
driver.find_element_by_id('datepicker').click()

json_date = defaultdict(lambda : defaultdict(dict))

dropdown_year = Select(driver.find_element_by_xpath("//select[@class='ui-datepicker-year']"))
available_year = [year_option.text for year_option in dropdown_year.options]
for year in available_year[:2]:
    driver.find_element_by_xpath(f"//select[@class='ui-datepicker-year']/option[text()='{year}']").click()
    dropdown_month = Select(driver.find_element_by_xpath("//select[@class='ui-datepicker-month']"))
    available_month = [month_option.text for month_option in dropdown_month.options] #month_option.get_attribute('value')
    print(available_month)
    for month in available_month:
        driver.find_element_by_xpath(f"//select[@class='ui-datepicker-month']/option[text()='{month}']").click()
        available_days = [day.text for day in driver.find_elements_by_xpath("//td[@data-handler='selectDay']")]
        json_date[year][month] = available_days

#########################################
#########################################
#########################################



################################################
#### download BRA from json_date (webdriver need to be open on the 'normal page') ###########
################################################
################################################
        
        
month_equivalent = {'janv.': '01',
                    'févr.': '02',
                    'mars': '03',
                    'avril': '04',
                    'mai': '05',
                    'juin': '06',
                    'juil.': '07',
                    'août': '08',
                    'sept.': '09', 
                    'oct.': '10',
                    'nov.': '11',
                    'déc.': '12'}        

        
driver.find_element_by_xpath("//div[@class='publication-info telechargements replie']/h3[contains(., 'Téléchargement')]").click()
driver.find_element_by_id('datepicker').click()
for year, available_month in json_date.items():
    print(year)
    driver.find_element_by_xpath(f"//select[@class='ui-datepicker-year']/option[text()='{year}']").click()
    for month, available_days in available_month.items():
        print(month)
        driver.find_element_by_xpath(f"//select[@class='ui-datepicker-month']/option[text()='{month}']").click()
        for day in available_days:
            date = f"{month_equivalent[month]}{day}{year}"
            print(day)
            driver.find_element_by_xpath(f"//td[@data-handler='selectDay']/a[text()='{day}']").click()
            dropdown_massif = Select(driver.find_element_by_xpath("//select[@id='select_massif']"))
            if not dropdown_massif: 
                driver.find_element_by_id('datepicker').click()
                print(f'no BRA available for this date: {date}')
                continue
            available_massif = [massif.text for massif in dropdown_massif.options]
            for zone in available_massif:
                time.sleep(1)
                print(zone)
                driver.find_element_by_xpath(f"//select[@id='select_massif']/option[text()='{zone}']").click()
                driver.find_element_by_xpath("//select[@name='extension']/option[@value='xml']").click()
                driver.find_element_by_xpath("//input[@value='Télécharger']").click()
                link = driver.find_element_by_partial_link_text('Accès aux données')
                url = link.get_attribute('href')
                urlretrieve(url,
                            f'bra_test/{zone}_{date}.xml')
                driver.execute_script("window.history.go(-1)")
                driver.find_element_by_xpath("//div[@class='publication-info telechargements replie']/h3[contains(., 'Téléchargement')]").click()
                driver.find_element_by_id('datepicker').click()
                driver.find_element_by_xpath(f"//select[@class='ui-datepicker-year']/option[text()='{year}']").click()
                driver.find_element_by_xpath(f"//select[@class='ui-datepicker-month']/option[text()='{month}']").click()
                
    

#########################################
#########################################
#########################################
    



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
        print(bra_fp)
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















    
url_bra = 'http://www.meteofrance.com/previsions-meteo-montagne/bulletin-avalanches'
regions = [['chablais', 'opp01'], ['aravis', 'opp02'], ['mont-blanc', 'opp03'], ['bauges','opp04'], ['maurienne', 'opp09'],
          ['vanoise', 'opp10'], ['beaufortain', 'opp05'], ['haute-tarentaise', 'opp06'], ['haute-maurienne', 'opp11'],
          ['chartreuse', 'opp07'], ['vercors', 'opp14'], ['belledonne', 'opp08'], ['oisans', 'opp15'], ['grandes-rousses', 'opp12'],
          ['thabor', 'opp13'], ['pelvoux', 'opp16'], ['champsaur', 'opp19'],
          ['devoluy', 'opp18'], ['embrunais-parpallon','OPP20'],['queyras', 'opp17'], 
          ['ubaye', 'opp21'], ['haut-var-haut-verdon', 'opp22'], ['mercantour', 'opp23']]

for region in regions:
    print(region[0])
    day = datetime.datetime.today().strftime('%d_%m_%y')
    url_pdf_bra = 'http://www.meteofrance.com/integration/sim-portail/generated/integration/img/produits/pdf/bulletins_bra'
    urllib.request.urlretrieve('{}/{}.pdf'.format(url_pdf_bra, region[1].upper()),
                               '../../divers/perso/avalanche_projet/bra/{}_{}.pdf'.format(region[0], day))







from urllib.request import urlopen
#url = "http://www.meteofrance.com/previsions-meteo-montagne/bulletin-avalanches/mont-blanc/OPP03"
url = 'http://www.meteofrance.com/previsions-meteo-montagne/bulletin-avalanches/aravis/OPP02'
html = urlopen(url)
from bs4 import BeautifulSoup
soup = BeautifulSoup(html)

images = soup.find_all('img')

img = images[6].get('src')
import base64
head, data = img.split(',', 1)
file_ext = head.split(';')[0].split('/')[1]
plain_data = base64.b64decode(data)
with open('image_bis.' + file_ext, 'wb') as f:
    f.write(plain_data)


for i, res in enumerate(soup.find_all('img')):
    #print(res.get('src'))
    print(i)
    try:
        list_var = url.split('/')
        resource = urlopen(list_var[0]+"//"+list_var[2]+res.get('src'))
        output = open('test/'+res.get('src').split('/')[-1],"wb")
        output.write(resource.read())
        output.close()
    except:
        print('FAILED')



from scipy.misc import imread
a = imread('image.png')
b = imread('image_bis.png')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,2)
ax[0].imshow(a[20:22, 225:230, :], cmap=plt.cm.gray)
ax[1].imshow(b[3:108, 210:300, :], cmap=plt.cm.gray)


from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
text = pytesseract.image_to_string(Image.open('image_bis.png'))


def download_pdf():
    
  url_bra = 'http://www.meteofrance.com/previsions-meteo-montagne/bulletin-avalanches'
  regions = [['chablais', 'opp01'], ['aravis', 'opp02'], ['mont-blanc', 'opp03'], ['bauges','opp04'], ['maurienne', 'opp09'],
            ['vanoise', 'opp10'], ['beaufortain', 'opp05'], ['haute-tarentaise', 'opp06'], ['haute-maurienne', 'opp11'],
            ['chartreuse', 'opp07'], ['vercors', 'opp14'], ['belledonne', 'opp08'], ['oisans', 'opp15'], ['grandes-rousses', 'opp12'],
            ['thabor', 'opp13'], ['pelvoux', 'opp16'], ['champsaur', 'opp19'],
            ['devoluy', 'opp18'], ['embrunais-parpallon','OPP20'],['queyras', 'opp17'], 
            ['ubaye', 'opp21'], ['haut-var-haut-verdon', 'opp22'], ['mercantour', 'opp23']]

  for region in regions:
      print(region[0])
      day = datetime.datetime.today().strftime('%d_%m_%y')
      url_pdf_bra = 'http://www.meteofrance.com/integration/sim-portail/generated/integration/img/produits/pdf/bulletins_bra'
      urllib.request.urlretrieve('{}/{}.pdf'.format(url_pdf_bra, region[1].upper()),
                                 'bra/{}_{}.pdf'.format(region[0], day))




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
    
    

    
    
    







