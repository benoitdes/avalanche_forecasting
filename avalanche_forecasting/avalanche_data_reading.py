#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 20:54:45 2019

@author: plume
"""

import json


def create_dataset_from_report(report_fp):

    data_info = pd.DataFrame()
    for path in Path(report_fp).glob('*.json'):
        print(path)
        with path.open(mode='r') as file:
            info = json.loads(file.read())
        data = pd.DataFrame({k: [info[k]] for k in list(set(info.keys()) & set(KEYS))})
        data_info = data_info.append(data, sort=True)
    return data_info



data = create_dataset_from_report('data_avalanche_report')
data.to_csv('avalanche_report_data.csv', index=False)