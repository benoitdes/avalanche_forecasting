#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 23:18:24 2019

@author: plume
"""
import glob
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import time
import json
from collections import defaultdict


REGIONS =     ['CHABLAIS',
               'MONT-BLANC',
               'ARAVIS',
               'CHARTREUSE',
               'BELLEDONNE',
               'GRANDES-ROUSSES',
               'VERCORS',
               'OISANS',
               'HAUTE-TARENTAISE',
               'BEAUFORTAIN',
               'BAUGES',
               'VANOISE',
               'HAUTE-MAURIENNE',
               'MAURIENNE',
               'UBAYE',
               'HAUT-VAR/HAUT-VERDON',
               'THABOR',
               'PELVOUX',
               'QUEYRAS',
               'CHAMPSAUR',
               'DEVOLUY',
               'EMBRUNAIS-PARPAILLON',
               'HAUT-VAR/HAUT-VERDON',
               'MERCANTOUR',
               'CINTO-ROTONDO',
               'RENOSO-INCUDINE',
               'ANDORRE',
               'ORLU__ST_BARTHELEMY',
               'HAUTE-ARIEGE',
               'COUSERANS',
               'COUSERANS',
               'LUCHONNAIS',
               'AURE-LOURON',
               'HAUTE-BIGORRE',
               'ASPE-OSSAU',
               'PAYS-BASQUE',
               'CERDAGNE-CANIGOU',
               'CAPCIR-PUYMORENS']


class AvalancheBulletinScraper():

    def __init__(self, url, where_to_save, implicity_wait=10):

        self.url = url
        self.wait = implicity_wait
        self.where_to_save = where_to_save
        self.create_driver(url)
      
    def is_bulletin_downloaded(self, zone, year, month, day):

        if glob.glob(f'../avalanche_forecasting/avalanche_bulletin/{zone}_{year}{str(int(month)+1)}{day}.xml'):
            return True
        else:
            return False

    def create_driver(self, url):

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(self.wait)
        self.driver.get(url)

    def click_calendar(self, where, value):
    
        xpath = f"//select[@class='ui-datepicker-{where}']/option[@value='{value}']"
        WebDriverWait(self.driver, self.wait).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    

    def scrap_bulletin(self, zone, year, month, day, where_to_save):

        element = self.driver.find_element_by_xpath("//div[@class='publication-info telechargements replie']/h3[contains(., 'Téléchargement')]")
        self.driver.execute_script("arguments[0].click();", element)

        self.select_day(year, month, day)
        WebDriverWait(self.driver, self.wait).until(EC.element_to_be_clickable((By.XPATH, f"//select[@id='select_massif']/option[text()='{zone}']"))).click()
        WebDriverWait(self.driver, self.wait).until(EC.element_to_be_clickable((By.XPATH, "//select[@name='extension']/option[@value='xml']"))).click()
        WebDriverWait(self.driver, self.wait).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Télécharger']"))).click()
        
        link = self.driver.find_element_by_partial_link_text('Accès aux données')
        url = link.get_attribute('href')
        urlretrieve(url,
                    f'{where_to_save}/{zone}_{year}{str(int(month)+1)}{day}.xml')
        self.driver.execute_script("window.history.go(-1)")
    
        return True


    def select_day(self, year, month, day):
    
        element = WebDriverWait(self.driver, self.wait).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='datepicker'][@class='hasDatepicker']"))).click()

        self.click_calendar('year', year)
        self.click_calendar('month', month)
        WebDriverWait(self.driver, self.wait).until(EC.element_to_be_clickable((By.XPATH, f"//td[@data-handler='selectDay']/a[text()='{day}']"))).click()

    def is_bulletin_available(self, year, month, day):

        element = self.driver.find_element_by_xpath("//div[@class='publication-info telechargements replie']/h3[contains(., 'Téléchargement')]")
        self.driver.execute_script("arguments[0].click();", element)

        self.select_day(year, month, day)
        time.sleep(3)
        element = WebDriverWait(self.driver, self.wait).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='select_massif']")))
        self.driver.execute_script("arguments[0].click();", element)
        if self.driver.find_element_by_xpath("//select[@id='select_massif']").get_attribute('value') == '':
            available_region = []
        else:
            dropdown_region = Select(self.driver.find_element_by_xpath("//select[@id='select_massif']"))
            available_region = [region.get_attribute('value') for region in dropdown_region.options]

        element = self.driver.find_element_by_xpath("//div[@class='publication-info telechargements']/h3[contains(., 'Téléchargement')]")
        self.driver.execute_script("arguments[0].click();", element)

        return available_region
    
    def scrap_bulletins(self, date_to_scrap):
        
        for year, available_months in date_to_scrap.items():
            for month, available_days in available_months.items():
                for day in available_days:
                    time.sleep(1)
                    print(year, month, day)
                    regions = self.is_bulletin_available(year, month, day)
                    if regions:
                        for zone in regions:
                            print(zone, year, month, day)
                            downloaded = self.is_bulletin_downloaded(zone, year, month, day)
                            if downloaded:
                                print('REPORT ALREADY DOWNLOADED')
                                continue
                            try:
                                self.scrap_bulletin(zone, year, month, day, self.where_to_save)
                            except Exception as e:
                                print(e)
                                self.driver.close()
                                self.create_driver(self.url)
                    else:
                        print(f'NO REPORT AVAILABLE for {year}-{month}-{day}')
                        continue
        return True

    def scrap_calendar_available_date(self):
        """
        Find available date to scrap
        """

        self.driver.find_element_by_xpath("//div[@class='publication-info telechargements replie']/h3[contains(., 'Téléchargement')]").click()
        self.driver.find_element_by_id('datepicker').click()

        json_date = defaultdict(lambda : defaultdict(list))

        dropdown_year = Select(self.driver.find_element_by_xpath("//select[@class='ui-datepicker-year']"))
        available_year = [year_option.get_attribute('value') for year_option in dropdown_year.options]
        for year in available_year:
            print(year)
            self.driver.find_element_by_xpath(f"//select[@class='ui-datepicker-year']/option[@value='{year}']").click()
            dropdown_month = Select(self.driver.find_element_by_xpath("//select[@class='ui-datepicker-month']"))
            available_month = [month_option.get_attribute('value') for month_option in dropdown_month.options] 
        
            available_month = list(set(available_month)-set(['5', '6', '7', '8', '9', '10']))
        
            for month in available_month:
                print(month)
                self.driver.find_element_by_xpath(f"//select[@class='ui-datepicker-month']/option[@value='{month}']").click()
                available_days = [day.text for day in self.driver.find_elements_by_xpath("//td[@data-handler='selectDay']")]
                for day in available_days:
                    if day != '':
                        json_date[year][month].append(day)
        
        element = self.driver.find_element_by_xpath("//div[@class='publication-info telechargements']/h3[contains(., 'Téléchargement')]")
        self.driver.execute_script("arguments[0].click();", element)

        return json_date


if __name__=='__main__':

    url = 'https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=265&id_rubrique=50'
    where_to_save = 'avalanche_bulletin'
    scraper = aB.AvalancheBulletinScraper(url, where_to_save)
    date_to_scrap = scraper.scrap_calendar_available_date()
    scraper.scrap_bulletins(date_to_scrap)


