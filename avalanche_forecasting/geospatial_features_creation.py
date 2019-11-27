#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 11:51:15 2019

@author: plume
"""

import numpy as np
import pandas as pd
import rasterio
from pyproj import Proj, transform
import glob


### On pourrait eventuellement récupérer le dem via l'API geoportail
### normalement gratuite pour 2 millions de transactions par an
### On peut faire un appel de 5000 point d'un coup donc potentiel 5000 * 2M de points, à voir si possible
### Cela permettrait de récupérer le DEM à 10m de précision
### https://geoservices.ign.fr/documentation/geoservices/alti.html
### API elevation de google est payante (en tout cas il faut contacter les sales pour y avoir accès)


def line_btw_coordinates(p1, p2, resolution=0.0001):
    """"Return a list equally spaced points
    between p1 and p2. Points are represented like (lon, lat) tuple"""
    # If we have 8 intermediate points, we have 8+1=9 spaces
    # between p1 and p2
    nb_points = int(max(np.abs(p1[0] - p2[0]), np.abs(p2[0] - p1[0])) / resolution)
    
    lons = np.linspace(p1[0], p2[0], nb_points)
    lats = np.linspace(p1[1], p2[1], nb_points)

    return list(zip(np.round(lons, 4), np.round(lats, 4)))


def regular_grid(upper_left, lower_right, resolution):
    """
    Builds a regular grid of latitudes and longitudes.
    """

    lons = np.linspace(upper_left[0], lower_right[0], 1 + (lower_right[0] - upper_left[0]) / resolution)
    lats = np.linspace(upper_left[1], lower_right[1], 1 + (upper_left[1] - lower_right[1]) / resolution)

    return lons, lats


p1 = (10, 30)
p2 = (0, 10)

print(line_btw_coordinates(p1, p2, resolution = 1))




#### read DEM file and find the one covering VANOISE massif ####
outProj = Proj(init='epsg:4326')


grid = {}
tif = []

for i, folder in enumerate(glob.glob('../data/dem_30/*')):
    print(folder)
    dem_file = f'{folder}/{folder.split("/")[-1]}.tif'
    tif.append(folder)
    with rasterio.open(dem_file) as src:
        data = src.read(1)
        print(src.bounds)
        transformation = src.transform
        projection = Proj(src.crs)
        upper_left = transform(projection, outProj, src.bounds.left, src.bounds.top)
        lower_right = transform(projection, outProj, src.bounds.right, src.bounds.bottom)
        lon, lat = np.meshgrid(*regular_grid(upper_left, lower_right, 0.01))
        grid[i] = pd.DataFrame(np.concatenate((lon.reshape(-1, 1), lat.reshape(-1, 1)), axis=1), columns=['lon', 'lat'])
        grid[i][['lat', 'lon']] = grid[i][['lat', 'lon']].round(4)
        grid[i]['val'] = i
        

big_grid = pd.DataFrame()
for key in grid.keys():
    big_grid = pd.concat([big_grid, grid[key]])

big_grid.to_csv('../data/geospatial_data/big_grid.csv')

#### TIF CORRESPONDING TO VANOISE MASSIF IS  LOCATED IN data/dem_30/N245E405/N245E405.tif
#### WE THEN CREATE ASPECT AND SLOPE TIF FILE USING QGIS



#### COMPUTE SLOPE AND ASPECT FROM VANOISE DEM
for type, file in {'aspect': '../data/geospatial_data/aspect_vanoise.tif', 'slope': '../data/geospatial_data/slope_vanoise.tif', 'dem': '../data/geospatial_data/dem_vanoise.tif'}.items():
    with rasterio.open(file) as src:
        elevation_data = src.read(1)
        print(src.bounds)
        transformation = src.transform
        projection = Proj(src.crs)
        upper_left = transform(projection, outProj, src.bounds.left, src.bounds.top)
        lower_right = transform(projection, outProj, src.bounds.right, src.bounds.bottom)
        x, y = np.array(range(len(elevation_data))), np.array(range(elevation_data.shape[1]))
        x, y = transform(projection, outProj, *transformation * (x, y))
        x, y = np.meshgrid(np.round(x, 4), np.round(y, 4))
        grid = pd.DataFrame(np.concatenate((x.reshape(-1, 1), y.reshape(-1, 1)), axis=1), columns=['lon', 'lat'])
        grid['val'] = elevation_data.reshape(-1, 1)
        grid.to_csv(f'data/geospatial_data/{type}_data.csv')



#### For now, we work on Bessans city

### Upper left and lower right coordinates around Bessans
upper_left = 6.820573, 45.380776#6.896154, 45.346260
lower_right = 7.183430, 45.241721#7.129268, 45.304818, 

bessans_data = pd.DataFrame()
for type in ['slope', 'aspect', 'dem']:
    data = pd.read_csv(f'data/geospatial_data/{type}_data.csv')
    data = data[(data['lat'] < upper_left[1]) & (data['lat'] > lower_right[1])]
    data = data[(data['lon'] > upper_left[0]) & (data['lon'] < lower_right[0])]
    bessans_data = pd.concat([bessans_data, data.rename(columns={'val': type})], axis=1)

# clean data
bessans_data = bessans_data.loc[:, ~bessans_data.columns.duplicated()]
bessans_data = bessans_data[(bessans_data['aspect'] != -9999.0)]
bessans_data = bessans_data[(bessans_data['slope'] != -9999.0)]
bessans_data['sin_aspect'] = bessans_data['aspect'].apply(lambda x: np.sin(np.pi * x / 180))
bessans_data['cos_aspect'] = bessans_data['aspect'].apply(lambda x: np.cos(np.pi * x / 180))



# bessans_data.drop('Unnamed: 0', axis=1, inplace=True)
bessans_data.to_csv('data/geospatial_data/geo_data_bessans.csv', index=False)


a = pd.concat([data for i in range(10)], axis=1)
b = pd.concat([data for i in range(100)])



np.sin(np.pi * 360/180)
np.cos(np.pi * 360/180)


grid[['lat', 'lon']] = grid[['lat', 'lon']]
grid.to_csv(f'../data/geospatial_data/{type}_data.csv')



#### reconstruire geo_data_bessans avec les nouvelles données aspect, slope et dem
#### push les modifs du plume mac du script epa_reports_reading.py
