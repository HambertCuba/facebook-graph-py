import requests
import json
import pandas as pd
import csv
from datetime import datetime
import webbrowser
import zipfile
import time
import pandas
import csv
import paramiko
import shutil
import csv
import logging
import pprint
#import psycopg2
import facebook_business
#import graph

#llamada de cuentas
#2
token = "EAAfj47wzha8BAEUZCWUSytRh1rRh4BDJwrHTpv76rYHjYQ2L2ZAl6MAGGE0D5uzEIpDjFogsmDDaL5EE6Got4HWR6b5qeuE0aL0HZBaY5nkfLtPyOe6ZAlPegVxhoQLe96aZCKGcm3l2H8rBIrIU1Bmqx5HTCTXuWqWYnPQMQsXmIGqRXzWDqzyRkRzp5P8A5fTeoTUcZAX7y48JOPQnZA8n1kqwSxedDql3QViInlcb1u0JcZCDn9jX"
fields= ['name','access_token']
me= "122990462555483"
api= "https://graph.facebook.com/"+'v.10.0'+'/'+me+'/'+'accounts?fields=name,access_token&access_token'+token
print(api)
headers1 = {
    'Content-Type': 'application/json'
                }
response=requests.get(api,stream=True,headers=headers1)
pprint(response.url)
response = response.json()

    
    
   
    
  
    
# path_descarga="C:/Users/jesus.soto/Downloads/"
# path_copia="C:/Users/jesus.soto/Downloads/bases/"
# connectionPy=None

# url1 = "https://api.embluemail.com/Services/Emblue3Service.svc/json/Authenticate"
# payload1 = json.dumps({
#   "User": "businessintelligencegec@gmail.com",
#   "Pass": "Comercio*01",
#   "Token": "SqHVdkQY-ADa5B-Y7xA1-l1gikbBozg"
# })
# headers1 = {
#   'Content-Type': 'application/json'
# }

# response1 = requests.request("POST", url1, headers=headers1, data=payload1)
# token1 = response1.text
# print(token1)
# token2=token1[10:42]
# print(token2)

# url = "https://api.embluemail.com/Services/EmBlue3Service.svc/Json/GetAutomaticReportsFiles"
# payload = json.dumps({"Token": token2 })
# headers = {
#   'Content-Type': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data=payload)
# data=response.text
# print(data)

# indice_ini=data.index("https:\/\/appreportes.embluemail.com\/repositorio\/15273\/ACTIVIDADDETALLEDIARIO_")
# indice_fin=indice_ini+99
# link=data[indice_ini:indice_fin]
# print(link)
# nuevo_link=link.replace("\/\/","//")
# print(nuevo_link)
# nuevo_link2=nuevo_link.replace("\/","//")
# print(nuevo_link2)



# #obtener el nombre del archivo
# indice2=link.index("ACTIVIDADDETALLEDIARIO_")
# indice_fin2=indice2+37
# nombre=link[indice2:indice_fin2]
# print(nombre)

# #webbrowser.open(link, new=2, autoraise=True)

# downloaded_obj = requests.get(nuevo_link2)

# with open(path_descarga, "wb") as file:

#     file.write(downloaded_obj.content)

# time.sleep(20)

# ruta_zip = path_descarga+nombre+".zip"
# print(ruta_zip)
# ruta_extraccion = path_descarga
# password = None

# archivo_zip = zipfile.ZipFile(ruta_zip, "r")
# try:
#     print(archivo_zip.namelist())
#     archivo_zip.extractall(pwd=password, path=ruta_extraccion)
# except:
#     pass

# archivo_zip.close()

# # Copia el archivo a una carpeta
# shutil.copy(nombre+".csv", path_copia)

# Copia el csv a la tabla
# connectionPy = psycopg2.connect(user = "usr_bi",
# 										password = "xRM4i5BVStauP94nSuA2",
# 										host = "vp4-pos-001.cdofp4nk2b2p.us-east-1.rds.amazonaws.com",
# 										port = "5432",
# 										database = 'Campanias_UNP')
# cur = connectionPy.cursor()
# f = open(path_copia/nombre+".csv" , 'r')
# cur.copy_from(f, campanias.tabla_gestion, sep=';')
# f.close()

