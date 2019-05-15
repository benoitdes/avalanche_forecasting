#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 20:33:13 2018

@author: plume
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier



from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.preprocessing import LabelBinarizer,StandardScaler
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np

idx = pd.IndexSlice


FEAT = ['dd', 'ff', 'u', 'ht_neige', 't', 'ssfrai', 'td', 'grain_predom', 'prof_sonde', 'grain_nombre']



def persistence_baseline(Y):
    
    pred = Y.copy()
    pred = pred.reset_index()
        
    pred['date'] = pred['date'] + pd.Timedelta(days=1)
    pred_Y = pred.merge(Y.reset_index(),
                        on=['date', 'Nom'],
                        suffixes=['_pred', '_true']).dropna()
    
    pred_Y.set_index(['date', 'Nom'], inplace=True)
    return pred_Y['aval_risque_true'], pred_Y['aval_risque_pred']
    

def report_classif(Y, pred, class_=['class 1', 'class 2', 'class 3', 'class 4']):   
    
    metrics = classification_report(Y, pred,target_names = class_)

    return metrics

def accuracy(Y, pred):

    return accuracy_score(Y, pred), f1_score(Y, pred, average='weighted')

def scale(X):
    
    X = preprocessing.scale(X.copy())

    return X
    

def evaluate_model(X, Y, dic_model):
    
    X = scale(X)
    
    metrics = {}
    for name, model in dic_model.items():
    
        metrics[name] = cross_val_score(model, X, np.ravel(Y), cv=3, scoring='accuracy')

    return metrics


def create_lag_features(data):
    
    for feat in FEAT + ['aval_risque'] :
        data[feat+'_minus_1'] = data[[feat]].shift(1)
        
    return data
    

def create_X_Y(data):
    
    data = data.copy()
    data = data.drop(['Latitude', 'Longitude'], axis=1)
    data = create_lag_features(data.copy())
    
    data.reset_index('date', inplace=True)
    data['date_minus_1'] = data['date'].shift(1)
    data[(data['date_minus_1'] - data['date'] == '-1 days')]
    data = data.set_index('date', append=True).dropna()
    data.drop(['date_minus_1'], axis=1, inplace=True)
    
    X = data[list(set(data.columns) - set(['aval_risque'] + FEAT))]
    Y = data[['aval_risque']]

    lb = LabelBinarizer()
    aval_risque_m_1 = pd.DataFrame(lb.fit_transform(X['aval_risque_minus_1']), index=X.index)

    X = pd.concat([X, aval_risque_m_1], axis=1)
    X = X.drop(['aval_risque_minus_1'], axis=1)
    
    return X, Y

def return_prediction(data, model):
    
    X, Y = create_X_Y(data)
    X_tr, X_te, Y_tr, Y_te = train_test_split(X, Y, test_size=0.33)
   
    idx_tr = X_tr.index
    idx_te = X_te.index
    
    X_tr = scale(X_tr)
    X_te = scale(X_te)
    model.fit(X_tr, Y_tr)
    
    pred_tr = pd.DataFrame(model.predict(X_tr), index=idx_tr, columns=['aval_risque'])
    pred_te = pd.DataFrame(model.predict(X_te), index=idx_te, columns=['aval_risque'])

    return pred_tr, Y_tr, pred_te, Y_te
    

def evaluate_perf_station(data):

    dic_model = {'rand_forest': RandomForestClassifier(),
             'knn': KNeighborsClassifier(),
             'logis_reg': LogisticRegression(),
             'svm': SVC(class_weight='balanced'),
             'grad_boosting': GradientBoostingClassifier()}

    perf_stat = {}
    
    for station in data.index.get_level_values(0).unique():
        data_stat = data.loc[idx[station, :],:]
        if len(data_stat) < 500:
            print('no enough data for {}'.format(station))
        else:
            print('training for {} ...'.format(station))
            X, Y = create_X_Y(data_stat)

            perf = evaluate_model(X, np.ravel(Y), dic_model)
            for model in perf.keys():
                perf[model] = np.mean(perf[model])
            perf_stat[station] = perf  
            Y_base, pred_base = persistence_baseline(Y)
            perf_stat[station]['baseline'] = accuracy(Y_base, pred_base)[0]

    return perf_stat
    
    

    
    
    
    
    
    
    
