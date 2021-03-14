#!/usr/bin/env python3
import requests
import json
import pandas as pd
import tweepy
import os
import config as cfg
import time
from datetime import datetime, timedelta
from pytz import timezone
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def main():
    # get data
    cvs = get_cvs_data()
    print(cvs)

   

    # book urls
    cvs_url = 'https://www.cvs.com/immunizations/covid-19-vaccine'

    # img urls
    cvs_img = '<img alt="" src="https://favicons.githubusercontent.com/www.cvs.com" height="13">'

    tz = timezone('EST')
    date = str(datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'))
    sites = ['CVS']
    appointments = [ cvs ]
    df_long = pd.DataFrame({'date': date, 'appointments': appointments, 'sites': sites})
    df_long.head()

    # wide format
    df_wide = df_long.pivot(index = 'date', columns = 'sites', values = 'appointments').reset_index()
    df_wide.head()

    try:
        df_historical = pd.read_csv('data/site-data.csv')

        ##Pull data from last row of history
        last_data = df_historical.iloc[0]

        ##Maybe tweet new availability
        if cvs.startswith( 'Available' ) and not last_data['CVS'].startswith( 'Available' ):
            tweet_it('Vaccination appointments are available at CVS. ' + cvs[9:] + " " + cvs_url)
            #print("Vaccine app available " + cvs[9:] + " " + +cvs_url 

        ##Maybe tweet new unavailability
        if "Unavailable" == cvs and last_data['CVS'].startswith( 'Available' ):
            tweet_it('CVS vaccination appointments are now closed.')
            #print("Appointments are not available")

    except pd.errors.EmptyDataError:
        df_historical = pd.DataFrame()


    # append today's data 
    df_historical = df_historical.append(df_wide).sort_values(by = 'date', ascending = False)

    # save updated file 
    df_historical.to_csv('data/site-data.csv', index = False)

    md_file = open('README.md', 'r')
    new_md_content = ''
    start_rpl = False
    for line in md_file:
        stripped_line = line.rstrip('\r\n')
        if '<!--end: status pages-->' == stripped_line:
            start_rpl = False
            new_md_content += "**Last Updated**: " + str(datetime.now(tz).strftime('%Y-%m-%d %I:%M %p')) + "\n\n"
            new_md_content += "| Site                | Status         |\n"
            new_md_content += "| ------------------- | -------------- |\n"
            new_md_content += "| " + cvs_img + " [CVS](" + cvs_url + ")               | " + stat_check(cvs) + "    |\n"

        if start_rpl != True:
            new_md_content += stripped_line + "\n"
        if '<!--start: status pages-->' == stripped_line:
            start_rpl = True

    md_file.close()

    md_file = open('README.md', 'w')
    md_file.write(new_md_content)
    md_file.close()

def stat_check(data):
    if data.startswith( 'Available' ):
        data = ':white_check_mark: ' + data + '  '
    else:
        data = ':no_entry: ' + data
    return data


def get_cvs_data():
    headers = {'referer': 'https://www.cvs.com/immunizations/covid-19-vaccine?icid=coronavirus-lp-nav-vaccine'}
    try:
        req = requests.get('https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.ma.json?vaccineinfo', headers=headers)
    except requests.exceptions.RequestException as e:
        return "ERROR - Requests"

    json_response = req.json()
    if 'responsePayloadData' not in json_response:
        return "ERROR - No Payload Data"
    else:
        if 'data' not in json_response['responsePayloadData']:
            return "ERROR"
        else:
            if 'MA' not in json_response['responsePayloadData']['data']:
                return "ERROR"
    
    message = ''
    for provider in json_response['responsePayloadData']['data']['MA']:
        city = provider['city']
        status = provider['status']
        total = 0
        if 'totalAvailable' in provider:
            total = provider['totalAvailable']
        if city in cfg.config["cvs_sites"] and status != 'Fully Booked':
            message = message + city + ' '
    if message != "":
        return "Available " + message
    else:
        return "Unavailable"

def tweet_it(message):
    CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    ACCESS_KEY = os.environ.get('TWITTER_ACCESS_KEY')
    ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    ##TODO: Error handling
    ##Try to get around twitter duplicate messaging
    tz = timezone('EST')
    message = message + " [" + str(datetime.now(tz).strftime('%m-%d-%Y %I:%M %p')) + "]"
    print("Tweeting message: " + message)
    api.update_status(message)


main()