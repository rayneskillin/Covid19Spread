#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 19:59:06 2020
@author: rayneskillin
"""
import pandas as pd
import requests 
import json 
import csv

#loads in businesses csv to convert to df
data = pd.read_csv('/Users/rayneskillin/Downloads/Businesses_Output.csv')
df = pd.DataFrame(data)

#sets up fields for reviews csv
fields = ['ID', 'Review']  
filename = "BusinessReviews.csv"

#put in your api key
api_key = ''
headers = {'Authorization' : 'Bearer %s' % api_key}

#starting row value of csv to loop through-- change this
a = 20
 
while a<25:

    lat = df.at[a,'Latitude']
    long = df.at[a,'Longitude']
    real_name = df.at[a,'Business Name']
    bus_id = df.at[a,'ID']
    
    url = 'https://api.yelp.com/v3/businesses/search'
    params = {'latitude': lat ,'longitude': long,}
    req = requests.get(url, params=params, headers=headers)
    parsed = json.loads(req.text)
    businesses = parsed["businesses"]

    for business in businesses:
    
        search_name = business['name']
        url="https://api.yelp.com/v3/businesses/" + business["id"] + "/reviews"
        req = requests.get(url, headers=headers)
        parsed = json.loads(req.text)
        reviews = parsed["reviews"]
 
        if search_name == real_name:
            
            for review in reviews:
            
                mydict =[{'ID': bus_id, 'Review': review["text"]}]
            
                # writing to csv file  
                with open(filename, 'a') as csvfile:    
                    writer = csv.DictWriter(csvfile, fieldnames= fields)  
                    writer.writerows(mydict)
    a += 1
