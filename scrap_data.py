#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 16:10:30 2018

@author: benoit
"""
%load_ext autoreload
%autoreload 2

import numpy as np
import urllib.request
import pandas as pd
import os
import importlib as imp
import datetime
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier




import tools_function as tf

idx = pd.IndexSlice



#code to download data
tf.download_data()


#clean station id infos             
station_infos = pd.read_csv('data/postesNivo.csv').dropna()
station_infos.ID = station_infos.ID.apply(lambda x : int(x))
station_infos.rename(columns = {'ID' : 'numer_sta'},inplace=True)
station_infos.to_csv('data/postesNivo.csv',index=False)


#create dataset with all data available
all_month = ['0'+str(i) for i in range(1,10)] + [str(i) for i in range(10,13)]
data = tf.create_dataset(list_year=[str(i) for i in range(2010,2019)],
                                          list_month=all_month)



# bar chart max height snow for 2018 winter
data = all_data[(all_data['date']>'2017-11-01')&(all_data['date']<'2018-05-01')]
data['ht_neige'] = data['ht_neige'].astype('float')
stat_neige = data.groupby('Nom')['ht_neige'].max().reset_index()
fig, ax = plt.subplots()
stat_neige.plot(kind='barh', x='Nom', y="ht_neige", ax=ax)


# bar chart station altitude 
data['haut_stat'] = data['haut_sta'].astype('float')
stat_neige = data.groupby('Nom')['haut_stat'].max().reset_index()
fig, ax = plt.subplots()
stat_neige.plot(kind='barh', x='Nom', y="haut_stat", ax=ax)


#check number of observations where aval_risque is available per station 
all_data['aval_risque'] = all_data['aval_risque'].astype('float')
stat_aval_risque = all_data['aval_risque'].notnull().groupby(all_data['Nom']).sum().reset_index()
fig, ax = plt.subplots()
stat_aval_risque.plot(kind='bar', x='Nom', y="aval_risque", ax=ax)



#plot on different stuff on one station 
station = data.groupby('Nom')['u'].count().idxmax()
fig, ax = plt.subplots(nrows=1,ncols=1)
df = data[data.Nom==station]
ax.hist(data['u'].dropna())

data[:1000].plot(kind='barh', y="ht_neige")





df = data[['ht_neige']].dropna()

#plot ht_neige in markers with different colors for eval_risque
fig, ax = plt.subplots(nrows=1,ncols=1)
ax.plot(df.index.levels[1],df['ht_neige'].values.tolist())


fig, ax = plt.subplots(nrows=1,ncols=1)

ax.plot(df['ht_neige'][:10])




fig, ax = plt.subplots(nrows=1,ncols=1)
ax.plot(new['ht_neige'])

data = pd.DataFrame()    
for acol in list(set(res.columns)-set(['Nom','date'])) :
    data = pd.concat([data,pd.DataFrame(data[[acol]].values.astype(float),columns=[acol])],axis=1)            



df = pd.concat([res[['Nom', 'date']], data], axis=1)


n = data[['ht_neige']].values.astype(float) 
        
res = data.copy()


'u : humidite / int / %'
'td : point de rosee / reel / K'
'dd : Direction du vent moyen 10 mn / int / degré'
'ff : Vitesse du vent moyen 10 mn / réel / m/s'
't : Température / réel / K'
'ssfrai : Hauteur de la neige fraîche / réel / m'
'ht_neige : Hauteur totale de neige / réel / m'
'aval_risque : Estimation du risque davalanche / int / code'
'haut_sta  : Altitude de la station / réel / m'

"A voir si prendre plus de feature et moins de donnees n'est pas plus interessant'


all_month = ['0'+str(i) for i in range(1,10)] + [str(i) for i in range(10,13)]
data = tf.create_dataset(list_year=[str(i) for i in range(2010,2019)],
                                          list_month=all_month)



        
X = data[['dd', 'ff', 'u', 'ht_neige', 't', 'ssfrai', 'td']].reset_index()
X.describe()    

    






# consistency aval risque evaluation between station 
#variance intra station 
data_ = data.dropna()
data_.groupby('date')['aval_risque'].mean()
data_.groupby('date')['aval_risque'].var().mean()



#check if data is mostly available every day at each station
df = data.reset_index('date')
for i in range(1,4):
    df['date_'+str(i)] = df['date'].shift(i)
    df['diff_'+str(i)] = df['date_'+str(i)] - df['date']    

for i in range(1,4):
    df['diff_'+str(i)] = df['diff_'+str(i)] == '-'+str(i)+' days'

one_conseq_days = len(df[df[['diff_'+str(i) for i in [1]]].sum(1) == 1])
two_conseq_days = len(df[df[['diff_'+str(i) for i in [1, 2]]].sum(1) == 2])
three_conseq_days = len(df[df[['diff_'+str(i) for i in [1, 2, 3]]].sum(1) == 3])
 

# plot correlation matrix
tf.plot_correlation(data, feature=[])


# count number of labels
count_ylabel = pd.DataFrame(data.groupby('aval_risque').size())
count_ylabel.plot(y=0, kind='bar', label='count events')

#first attend to do classification of the day

save_data = data.copy()
data = save_data.copy()
data = data.dropna()
# station with max observations
station = data.groupby('Nom').size().idxmax()




import ml_functions as mF


data.loc[data['aval_risque'] == 5] = 4

#perf per station
perf = mF.evaluate_perf_station(data)
for stat in perf.keys():
    for model in perf[stat].keys():
        if perf[stat][model] > perf[stat]['baseline']:
            print(stat, model, perf[stat][model], perf[stat]['baseline'])



#perf on all stations
            
            
X, Y = mF.create_X_Y(data.copy())


from sklearn.model_selection import train_test_split

X_tr, X_te, Y_tr, Y_te = train_test_split(X, Y, test_size=0.33)



pred_tr, Y_tr, pred_te, Y_te = mF.return_prediction(data.copy(), LogisticRegression(class_weight='balanced'))


df = pred_tr.join(Y_tr, rsuffix='_pred')
df['size_error'] = df['aval_risque'] - df['aval_risque_pred']

df[df['size_error'] != 0].groupby(['aval_risque']).size()
df.groupby(['size_error']).count()




mF.accuracy(Y_te, pred_te)
mF.accuracy(Y_tr, pred_tr)






Y_tr.groupby(['aval_risque']).size()
pd.DataFrame(pred_tr, columns = ['aval_risque']).groupby(['aval_risque']).size()

Y_te.groupby(['aval_risque']).size()
pd.DataFrame(pred_te, columns = ['aval_risque']).groupby(['aval_risque']).size()



fix, ax = plt.subplots()
ax.hist(Y_tr.reset_index(drop=True).values, bins=list(range(1,5)))




mF.accuracy(Y_te, pred_te)



dic_model = {'logis_reg': LogisticRegression()}  
    
perf = mF.evaluate_model(X, np.ravel(Y), dic_model)
perf
Y_base, pred_base = mF.persistence_baseline(Y)
mF.accuracy(Y_base, pred_base)




import pandas as pd

df_1 = pd.read_csv('finalSeriesForPrediction.csv')
df_2 = pd.read_csv('finalSeriesForTrainingWithLatLon.csv')
df_3 = pd.read_csv('CleanedForecastsNWAC.csv')



# improve station_enought_obs
# gerer le fait que ce soit un imbalance problem
# hauteur de neige assez faible dans les observations. Que faire ? 
# regarder changement perf en ajoutant des stations (plus ou moins proche)
# plot sur kepler des predicitions pour voir s'il y a de la consistence
# trouver des features de meteo hyper locale pour faire une prediction plus fine
# ploter DEM
# feature engineering
# clustering pour voir similitude entre stations


# scraper données de skiinfo + données des BRA et faire des stats sur # de sorties vs risque avalanche etc (regroupé par week end/semaine pour éventuellement remarquer des comportements
# à risque)






df_2[(df_2.Lat == 47.564)&(df_2.Lon == -119.692)]




df_2.iloc[2][['Lat', 'Long']]







