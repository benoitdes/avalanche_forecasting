#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:36:23 2019

@author: plume
"""

import xml.etree.ElementTree as ET
import pandas as pd
import glob




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