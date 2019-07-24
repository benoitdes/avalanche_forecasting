#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:36:23 2019

@author: plume
"""

import xml.etree.ElementTree as ET
import pandas as pd
import glob
import dateutil.parser


## when you have _0 it means the day after the bulleting _1 the second day after etc
## for tendance value, -1 means lower risk, 0 is same and 1 is greter risk


def create_bulletin_dataset():

    final_bra_data = pd.DataFrame()

    for bra_fp in glob.glob('avalanche_bulletin/*'):
    
        print(bra_fp)
        tree = ET.parse(bra_fp)
        root = tree.getroot()
        info_xml = {}
        info_xml = root.attrib.copy()
        
        for child in root.iter():
            
            if child.tag in ['CARTOUCHERISQUE', 'ENNEIGEMENT', 'STABILITE', 'QUALITE', 'TENDANCES', 'AVALANCHES']:
                count_tag = 0
                for elem in child.iter():
                    if elem.tag in ['ImageCartoucheRisque', 'Content', 'ImageEnneigement']:
                        continue
                                
                    elif not elem.attrib and elem.text is not None:
                        info_xml[f'{child.tag}_{elem.tag}'] = elem.text
                    
                    elif elem.attrib:
                            
                        if elem.tag in ['NIVEAU', 'TENDANCE', 'AVALANCHE']:
                            elem.tag = f'{elem.tag}_{count_tag}'
                            count_tag += 1
                            
                        for key, val in elem.attrib.items():
                                
                            if elem.tag in child.tag:
                                info_xml[f'{child.tag}_{key}'] = val
                            else:
                                info_xml[f'{child.tag}_{elem.tag}_{key}'] = val
                    
        for key in info_xml.keys():
            info_xml[key] = [info_xml[key]]
    
        bra_data = pd.DataFrame(info_xml)
        final_bra_data = final_bra_data.append(bra_data, sort=True)

    final_bra_data = final_bra_data.drop(['CARTOUCHERISQUE_CARTOUCHERISQUE',
                                          'QUALITE_QUALITE',
                                          'TENDANCES_TENDANCES',
                                          'AVALANCHES_AVALANCHES',
                                          'TYPEBULLETIN',
                                          'STABILITE_STABILITE',
                                          'AMENDEMENT'], axis=1)

    return final_bra_data



def clean_bulletin_dataset(raw_dataset):

    raw_dataset.columns = [col.lower() for col in raw_dataset.columns]
    raw_dataset = raw_dataset.replace('', np.nan)
    raw_dataset= raw_dataset.replace('/', np.nan)

    col_int = ['cartoucherisque_risque1',
               'cartoucherisque_risque2',
               'cartoucherisque_evolurisque1',
               'cartoucherisque_evolurisque2',
               'cartoucherisque_risquemaxi']

    col_comment = ['cartoucherisque_accidentel',
                  'cartoucherisque_commentaire',
                  'cartoucherisque_naturel',
                  'cartoucherisque_pente_commentaire',
                  'cartoucherisque_resume',
                  'qualite_texte',
                  'stabilite_texte']

    col_info = ['datebulletin',
                'datediffusion',
                'dateecheance',
                'datevalidite',
                'id',
                'massif',
                'producteur']


    for col in raw_dataset.columns:   
        if 'date' in col:
            raw_dataset[col] = raw_dataset[col].apply(lambda x: dateutil.parser.parse(x) if type(x) is str else x)
            raw_dataset[col] = raw_dataset[col].apply( lambda x: x.replace(hour=0, minute=0))
        if col in col_int:
            raw_dataset[col] = raw_dataset[col].astype(float)
        if col in col_comment:
            raw_dataset = raw_dataset.rename(columns={col: f'cm_{col}'})
        if col in col_info:
            raw_dataset = raw_dataset.rename(columns={col: f'info_{col}'})
        if 'cartoucherisque' in col:
            raw_dataset = raw_dataset.rename(columns={col: col.replace('cartoucherisque', 'dg')})        
        if 'tendances' in col:
            raw_dataset = raw_dataset.rename(columns={col: col.replace('tendances_tendance', 'td')}) 
        if 'enneigement' in col:
            raw_dataset = raw_dataset.rename(columns={col: col.replace('enneigement', 'en')}) 
        if 'avalanche' in col:
            raw_dataset = raw_dataset.rename(columns={col: col.replace('avalanches_avalanche', 'avy')}) 
    
    
    raw_dataset = raw_dataset[raw_dataset['dg_risque1']!=-1]
    raw_dataset = raw_dataset.dropna(subset=['info_massif'])
    raw_dataset = raw_dataset.sort_values('info_datevalidite')
    
    raw_dataset.drop(['info_datebulletin', 'info_datediffusion', 'info_datevalidite'], axis=1, inplace=True)
    raw_dataset.rename(columns={'info_dateecheance': 'info_datebulletin'}, inplace=True)
    
    
    
    
    return raw_dataset
    #data.to_csv('avy_bulletin_data.csv', index=False)


def load_bulletin_dataset(file_path):

    data = pd.read_csv(file_path, low_memory=False)
    col_date = [col for col in data.columns if "date" in col]
    data[col_date] = data[col_date].apply(lambda x: pd.to_datetime(x))

    return data

if __name__=='__main__':
    
    raw_dataset = create_bulletin_dataset()
    cleam_dataset = clean_bulletin_dataset(raw_dataset)
    clean_dataset.to_csv('data/avy_bulletin_data.csv', index=False)
    
    