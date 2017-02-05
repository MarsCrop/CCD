#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import facebook
import mysql.connector
import json

def facebook_database():
    conectar_base_de_datos = mysql.connector.connect(host= "localhost",                                  
              user=#nombre del usuario,                           
              passwd=#password,  
              charset="utf8", #lectura de caracteres                   
              db=#nombre de la base de datos )     
                                                                       
    cursor = conectar_base_de_datos.cursor()                           
                                                                       
    #token de acceso                                                   
                                                            
    token_acceso = #token de acceso para aplicacion creada desde facebook (sin la cual no se pueden obtener credenciales para acceder a la API)
    api_graph = facebook.GraphAPI(token_acceso)

    perfil = api_graph.get_object(#buscar en un perfil de facebook o pagina de facebook relacionada con el tema, para obtener el n de perfil buscar en www.findmyfid.com)

    conexion_con_perfil = api_graph.get_connections(perfil['id'], 'posts?format=json&limit=100') #otro defecto de facebook, la búsqueda esta limitada a los últimos 100 posts

    #comando_tabla = "CREATE TABLE IF NOT EXISTS `facebook` (`fecha` varchar(255), `post` varchar(255), `desastre` varchar(255), `usuario` varchar(255))"
    #cursor.execute(comando_tabla) 
    queries = ['sismo', 'terremoto', 'inundacion', 'incendio', 'alud', 'maremoto', 'incendio forestal', 'sequia', 'tsunami', 'desprendimiento de tierra', 'delizamiento de tierra']        

    for query in queries:                                               
        with open("facebook.json", 'a') as f:                          
            for i in conexion_con_perfil['data']:                                                                        
                if 'message' in i:                                                                        
                    if query in i['message']:   #cambiar message por description si el sitio es un perfil y no una pagina de facebook
                        cursor.execute("INSERT INTO facebook (fecha, post, desastre, usuario) VALUES (%s,%s,%s,%s);",(i['created_time'].split('T')[0], 'facebook.com/'+str(i['id']), query, #el id del perfil))     
                        conectar_base_de_datos.commit()

if __name__ == '__main__':
    try:
        facebook_database()
    except Exception, e:
        sys.exit(1)
