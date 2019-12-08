# Avalanche forecasting

## Description
The overall goal of this project is to reduce avalanche-related deaths across the world. 
The idea is to apply machine learning to automatically forecast avalanche danger and take advantages of current state of the art ML models to improve performances both in spatial and temporal resolutions.

## Current approach

Professional avalanche forecasts are currently based on weather, snow and manually collected information. These forecasts are made at regional scale, one day in advance. They heavily rely on professional expertise, weather information and physical modelisation of snow pack.

## Propose approach
Very few attempts have been done to forecast avalanche danger using machine learning methods. Since a few years, many weather, snow and historical forecast information have been made available on the internet as open dataset (see https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=265&id_rubrique=50 for French open datasets).
Moreover, more and more information about avalanches are reported every year by professionals as well as individuals in an effort to gain knowledge about avalanche processes (see http://www.avalanches.fr/epa_lobservation-actuelle/ for french avalanche occurences recorded by professionals)

The goal of this open source project is to evaluate the possibility to improve avalanche danger prediction based on open datasets and individually collected information.
Current professional forecasts have a good precision but lack of granularity in space: the idea is to use very local information about avalanche activity (based on avalanche occurrences reported by individuals) with snow and weather information made available online to create machine learning models that will be able to forecast avalanche danger in a very fine resolution.

We could then take advantage of knowledge gained in regions where we have substancial information (for example the Alps) to give avalanche danger forcasts in region that currently lack of them (mainly Himalayan region).

## Contacts

Feel free to send me an email at benoit.desvignes@protonmail.com for more detailed information. I would love to work on this problem with ML enthousiasts, person with avalanche modelisation knowledge and everyone who believe that we can change things with collective and opensource project!
