# Avalanche forecasting

## Description
The overall goal of this project is to reduce avalanche-related deaths across the world. 
The idea is to apply machine learning to automatically forecast avalanche danger and take advantages of current state of the art ML models to improve performances both in spatial and temporal resolutions.

## Current approach

Professional avalanche forecasts are currently based on weather, snow and manually collected information. These forecasts are made at regional scale, one day in advance. They heavily rely on professional expertise, weather information and physical modelisation of snow pack.

## Propose approach
Very few attempts have been done to forecast avalanche danger using machine learning methods. Since a few years, many weather, snow and historical forecast information have been made available on the internet as open dataset (see here for French open datasets).
Moreover, more and more information about avalanches are reported every year by individuals in an effort to gain knowledge about avalanche occurrences (see here)

The goal of this open source project is to evaluate the possibility to improve avalanche danger prediction based on open dataset and individually collected information.
Current professional forecasts have good precision but lack of granularity in space : the idea is to use very local information about avalanche activity (based on avalanche occurrences reported by individuals) with snow and weather information made available online to create machine learning models that will be able to forecast avalanche danger in a very fine resolution.

We could then take advantages of knowledges gained in region where we have ‘lot’ of information (for example the Alps) to give avalanche danger information in region that currently lack of them (mainly Himalayan region)
