import pandas as pd
import matplotlib.pyplot as plt
import dateutil.parser
import math
from datetime import date
from datetime import datetime, timedelta
import re
import os
import shutil
pd.set_option("display.max_rows", 3000)


today = date.today()
yesterday = today - pd.Timedelta(days=1)
before_yesterday = yesterday - pd.Timedelta(days=1)

yesterday_reformatted = yesterday.strftime('%m-%d-%Y')
before_yesterday_reformatted = before_yesterday.strftime('%m-%d-%Y')

#look for all old files and move them to historic 
for filename in os.listdir('data'):
   if 'PROCESSED' in filename or 'jhu-csse-newly-reported-cases' in filename:
       os.rename('data/' + filename, 'historic/' + filename)

#read in latest dataset
jhu = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+str(yesterday_reformatted)+'.csv')

#read in data from one day earlier
jhu_y = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+str(before_yesterday_reformatted)+'.csv')

#make a list of unique countries
jhu_countries=jhu['Country_Region'].unique()

#calculate number of new cases/deaths by substracting yesterday's figure from today's figure
new_data_list = []

for country in jhu_countries:
    country_dict = {}
    country_dict['country'] = country   
    country_dict['dateRep'] = today
    country_dict['yesterday'] = yesterday
    if (country == 'Denmark') | (country == 'France'):
        #get today's value
        df_temp_today = jhu[(jhu['Country_Region']==country)&(jhu['Province_State'].isnull())]
        acc_cases_today = df_temp_today[df_temp_today['Country_Region']== country]['Confirmed'].sum()
        acc_deaths_today = df_temp_today[df_temp_today['Country_Region']== country]['Deaths'].sum()
        country_dict['acc_cases_today'] = acc_cases_today
        #get yesterday's value
        df_temp_yesterday = jhu_y[(jhu_y['Country_Region']==country)&(jhu_y['Province_State'].isnull())]
        acc_cases_yesterday = df_temp_yesterday[df_temp_yesterday['Country_Region']== country]['Confirmed'].sum()
        acc_deaths_yesterday = df_temp_yesterday[df_temp_yesterday['Country_Region']== country]['Deaths'].sum()
        country_dict['acc_cases_yesterday'] = acc_cases_yesterday
        #calculate difference
        country_dict['NewCases_dateRep'] = acc_cases_today - acc_cases_yesterday
        country_dict['NewDeaths_dateRep'] = acc_deaths_today - acc_deaths_yesterday
        new_data_list.append(country_dict)
    else:
        #get today's value
        df_temp_today = jhu[jhu['Country_Region']==country]
        acc_cases_today = df_temp_today[df_temp_today['Country_Region']== country]['Confirmed'].sum()
        acc_deaths_today = df_temp_today[df_temp_today['Country_Region']== country]['Deaths'].sum()
        country_dict['acc_cases_today'] = acc_cases_today
        #get yesterday's value
        df_temp_yesterday = jhu_y[jhu_y['Country_Region']==country]
        acc_cases_yesterday = df_temp_yesterday[df_temp_yesterday['Country_Region']== country]['Confirmed'].sum()
        acc_deaths_yesterday = df_temp_yesterday[df_temp_yesterday['Country_Region']== country]['Deaths'].sum()
        country_dict['acc_cases_yesterday'] = acc_cases_yesterday
        #calculate difference
        country_dict['NewCases_dateRep'] = acc_cases_today - acc_cases_yesterday
        country_dict['NewDeaths_dateRep'] = acc_deaths_today - acc_deaths_yesterday
        new_data_list.append(country_dict)

#turn list into dataframe
newcases_jhu = pd.DataFrame(new_data_list)

# select and rename colums
newcases_jhu=newcases_jhu[['NewCases_dateRep', 'NewDeaths_dateRep', 'country', 'dateRep']]
newcases_jhu.columns=(['cases', 'deaths', 'countriesAndTerritories', 'dateRep'])

# merge with iso code
iso_codes = pd.read_csv('data_input/JHU_CSSE-configured_country-and-continent-codes-list.csv', delimiter=';')
newcases_jhu_merged = newcases_jhu.merge(iso_codes[['country', 'ISO-alpha3 code']], left_on='countriesAndTerritories', right_on='country')
newcases_jhu_merged=newcases_jhu_merged[['cases', 'deaths', 'countriesAndTerritories', 'dateRep', 'ISO-alpha3 code']]
newcases_jhu_merged.columns=(['cases', 'deaths', 'countriesAndTerritories', 'dateRep', 'countryterritoryCode'])

# save dataset containing only the new cases on this day
newcases_jhu_merged.to_csv('data/jhu-csse-newly-reported-cases_'+str(today)+'.csv', index = False)

#read in latest ecdc_base version
ecdc_base = pd.read_csv('data/ecdc_base-plus_update.csv')

#configure date to match date format in jhu_daily
ecdc_base['dateRep'] = [re.sub(r'(\d\d)\/(\d\d)\/(\d\d\d\d)','\g<3>-\g<2>-\g<1>', date) for date in ecdc_base['dateRep']]

# concat to reduced ecdc data ecdc_base
jhu_daily = pd.read_csv('data/jhu-csse-newly-reported-cases_'+str(today)+'.csv')
ej = pd.concat([jhu_daily,ecdc_base], ignore_index = True, sort=False)

# save the dataset to be read in for concating more data in the future
ej.to_csv('data/ecdc_base-plus_update.csv', index = False)

# merge with population data and continent data
meta = pd.read_csv('data_input/iso3-continent-population.csv')
ej_merged=ej.merge(meta, left_on='countryterritoryCode', right_on='countryterritoryCode', how='left')

# save merged dataset -- this one is used as a base for all analysis scripts
ej_merged.to_csv('data/PROCESSED_daily_cases_ecdc_jhu_'+str(today)+'.csv', index = False)
