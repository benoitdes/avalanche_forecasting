#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 22:30:53 2018

@author: plume
"""
import pandas as pd
import datetime
import numpy as np
import os

import matplotlib.pyplot as plt

import matplotlib.ticker as ticker
import matplotlib.cm as cm

idx = pd.IndexSlice

SCRIPT_DIRPATH = os.path.dirname(__file__)

#########################################
#########################################
#########################################
#########################################

def create_dataset(list_year,list_month):
    
    res = pd.DataFrame()
    for ayear in list_year:
        for amonth in list_month:
            try:
                print(os.path.join(SCRIPT_DIRPATH, '../', 'data/weather_snow_data/'+str(ayear)+amonth+'.gz'))
                data_loaded = pd.read_csv(os.path.join(SCRIPT_DIRPATH, '../', 'data/weather_snow_data/'+str(ayear)+amonth+'.gz'), delimiter=';')
                res = pd.concat([res, data_loaded])
            except:
                print('no data available for',ayear+amonth)
            
    res = res[res['date'] != 'date']
    res['date'] = res['date'].apply(lambda x: datetime.datetime.strptime(str(x)[:10], '%Y%m%d%H'))

    #select only month between november and april
    res['month'] = res['date'].apply(lambda x: x.month)
    res = res[res['month'].isin([11, 12, 1, 2, 3, 4])]

    res.replace('mq', np.nan, inplace=True)

    station_infos = pd.read_csv(os.path.join(SCRIPT_DIRPATH, '../', 'data/weather_snow_data/postesNivo.csv')).dropna()
    res['numer_sta'] = res['numer_sta'].astype('int64')
    
    res = res.merge(station_infos, on='numer_sta')
    
    return res

    
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
    
    
