#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import calendar
import time
import tweepy
import json
import mysql.connector

def twitter_database():                                                 
    conectar_base_de_datos = mysql.connector.connect(host= "localhost",         
                      user=#your username,                    
                      passwd=#your password, 
                      charset="utf8mb4", #lectura de caracteres         
                      db=#database name)                               
    cursor = conectar_base_de_datos.cursor()                                                                       
    clave_api =  #api key, you must have created a twitter app to obtain api access                     
    secreto_api = #api secret                               
    token_de_acceso =  #access token                                  
    secreto_de_acceso = #access secret                                                          
    autorizar = tweepy.OAuthHandler(clave_api, secreto_api)    
    autorizar.set_access_token(token_de_acceso, secreto_de_acceso)      
    api = tweepy.API(autorizar)                                                                        
    queries = ['#sismo ', '#terremoto ', '#inundacion ', '#incendio ', '#alud ', '#maremoto ', '#incendioforestal', '#sequia ', '#tsunami ', '#desprendimientodetierra', '#delizamientodetierra'] #queries list
                                         
    with open("tweets.json", 'a') as f:                                                             
        for query in queries:
            t = []  
            print query                                                                                                             
            try:                                                                      
                for tweet in tweepy.Cursor(api.search,                                                                       
                                           q= query + " filter:links",#busqueda de tweets por hashtag priorizando links                       
                                           rpp = 300,                                                                       
                                           result_type = "recent",#tweets mas recientes                                        
                                           include_entities = True,                                                                       
                                           lang = "es").items(300):  #busca los 300 tweets mas recientes                                  
                    t.append(tweet)                                    
            except Exception, e:
                rate_info = api.rate_limit_status()['resources']
                reset_time = rate_info['search']['/search/tweets']['reset']
                cur_time = calendar.timegm(datetime.datetime.utcnow().timetuple())
                try_again_time = reset_time - cur_time + 5
                print "Limite de busquedas excedido. Esperando para buscar mas" 
                time.sleep(try_again_time)

            for twt in t:                         
                for link in twt.entities['urls']:                                                                      
                    if link:                                                                       
                        usuario = twt._json['user']['screen_name']                                                                    
                        fecha = twt._json['created_at']                
                        link = link['expanded_url']                                                                       
                        tweet = twt.text                               
                        cursor.execute("INSERT INTO tweets (query, usuario, fecha, link, tweet) VALUES (%s,%s,%s,%s,%s);",(query, usuario, fecha, link, tweet)) #tweets are save here into *tweets table from the created database                                                   
                        conectar_base_de_datos.commit()
