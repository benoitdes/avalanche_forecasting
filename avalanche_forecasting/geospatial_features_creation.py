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
        grid[['lat', 'lon']] = grid[['lat', 'lon']]
        grid.to_csv(f'../data/geospatial_data/{type}_data.csv')


#### reconstruire geo_data_bessans avec les nouvelles données aspect, slope et dem
#### push les modifs du plume mac du script epa_reports_reading.py
