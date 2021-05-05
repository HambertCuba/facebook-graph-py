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
import requests



token = "EAAfj47wzha8BAMAacVES9jcb2UJZAFwdJsAokZBCNZAzEVpCPSOHfodvgxqmUJEwtcvMdDKek9EiiPteLMVYIfkPrdLXZCP3f6CT9aQFq7onNCbDaKdvlYKxKKrvTJvAEHwTHvodpUMkhmxRZCMrxZBGZCHGMkcipPR4BZCXN0Qi1FZAKHgZA7dZBA5"
fields= ['name','access_token']
me= "122990462555483"
api= "https://graph.facebook.com/"+'v10.0'+'/'+me+'/'+'accounts?fields=name,access_token&access_token='+token
print(api)
headers1 = {
    'Content-Type': 'application/json'
                }
responseprueba=requests.get(api,stream=True,headers=headers1)
#print(response.url)
responseprueba = responseprueba.json()
resultadosprueba=responseprueba["data"]
lista1=[]
for x in resultadosprueba:
   ### print(x["name"])
    accesstoken=x["access_token"]
    id=x["id"]
    name=x["name"]
    lista1.append( ##formato para agregar a una lista de forma manual
        {
             "accesstoken":accesstoken,
             "id":id,
             "name":name,
        }
    ) 
resultados=pd.DataFrame(lista1)

#print(resultadosprueba[0]['id'])

#sacar las publicaciones por cada objeto de la lista
token1 = resultadosprueba[0]['access_token']
me2= resultadosprueba[0]['id']
api2= "https://graph.facebook.com/"+'v10.0'+'/'+me2+'/'+'published_posts?access_token='+token1
print(api2)
headers2 = {
    'Content-Type': 'application/json'
                }
responseprueba2=requests.get(api2,stream=True,headers=headers2)
#print(response.url)
responseprueba2 = responseprueba2.json()
    
   
    
  
    


