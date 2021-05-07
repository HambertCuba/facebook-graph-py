import json
import pandas as pd
import csv
import webbrowser
import time
import pandas
import paramiko
import shutil
import logging
import pprint
from datetime import datetime, date, time, timedelta
import calendar
import facebook_business
import requests, urllib3
import pandas.io.formats.excel
from openpyxl import load_workbook
from openpyxl import Workbook
import xlsxwriter
import pydrive2
from googledrive import subir_archivo

#sacar las fechas de filtro
formato1="%Y-%m-%d"
now = datetime.today()
fecha_atras = now - timedelta(days=1)
#print(fecha_atras)
fecha1=now.strftime(formato1)
fecha2=fecha_atras.strftime(formato1)
#print(fecha2)

#sacar la cuenta de facebook:id y token
token = "EAAfj47wzha8BAMAacVES9jcb2UJZAFwdJsAokZBCNZAzEVpCPSOHfodvgxqmUJEwtcvMdDKek9EiiPteLMVYIfkPrdLXZCP3f6CT9aQFq7onNCbDaKdvlYKxKKrvTJvAEHwTHvodpUMkhmxRZCMrxZBGZCHGMkcipPR4BZCXN0Qi1FZAKHgZA7dZBA5"
fields= ['me','access_token']
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

#####sacar las publicaciones por cada objeto de la lista - cantidad e id del objeto
token1 = resultadosprueba[3]['access_token']
me2= resultadosprueba[3]['id']
api2= "https://graph.facebook.com/"+'v10.0'+'/'+me2+'/'+'published_posts?access_token='+token1+'&period=day&since='+fecha2+'&until='+fecha1+'&limit=100'
print(api2)
headers2 = {
    'Content-Type': 'application/json'
                }
owned_apps = []
responseprueba2=requests.get(api2,stream=True,headers=headers2)
#print(response.url)
responseprueba2 = responseprueba2.json()
resultadosprueba2=responseprueba2["data"]
owned_apps.extend(responseprueba2['data'])
after = responseprueba2.get('paging',{}).get('cursors',{}).get('after',None)
#print(responseprueba2["paging"]['next'])

while after:            
            api_paginated = api2  + "&after=" + after
            responseprueba_2 = requests.get(url=api_paginated, stream=True, headers = headers2)
            #pprint(responseprueba2.url) 
            responseprueba_2 = responseprueba_2.json()
            owned_apps.extend(responseprueba_2['data'])
            after = responseprueba_2.get('paging',{}).get('cursors',{}).get('after',None)
 
            if not after or after == '':
                #print(after)
                break

cantidad=len(owned_apps)


#######################parametros para la publicacion
#identificador de la publicacion
id = owned_apps[0]['id']

#fecha de publicacion
fecha = owned_apps[0]['created_time']
fecha= fecha[0:10]


#Lifetime Post Total Reach
token3 = resultadosprueba[3]['access_token']
me3= owned_apps[3]['id']
api3= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_posts_impressions_unique?access_token='+token3
print(api3)
headers3 = {
    'Content-Type': 'application/json'
                }
responseprueba3=requests.get(api3,stream=True,headers=headers3)
#print(response.url)
responseprueba3 = responseprueba3.json()
resultadosprueba3=responseprueba3["data"][0]["value"]
resultadospruebafinal1=resultadosprueba3[0]["value"]


#Lifetime Post organic reach
token4 = resultadosprueba[3]['access_token']
me3= owned_apps[3]['id']
api4= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_posts_impressions_organic_unique?access_token='+token4
print(api4)
headers4 = {
    'Content-Type': 'application/json'
                }
responseprueba4=requests.get(api4,stream=True,headers=headers4)
#print(response.url)
responseprueba4 = responseprueba4.json()
resultadosprueba4=responseprueba4["data"][0]["values"]
resultadospruebafinal2=resultadosprueba4[0]["value"]

#Lifetime Post Paid Reach
token5 = resultadosprueba[3]['access_token']
me3= owned_apps[3]['id']
api5= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_posts_impressions_paid_unique?access_token='+token5
print(api5)
headers5 = {
    'Content-Type': 'application/json'
                }
responseprueba5=requests.get(api5,stream=True,headers=headers5)
#print(response.url)
responseprueba5 = responseprueba5.json()
resultadosprueba5=responseprueba5["data"][0]["values"]
resultadospruebafinal3=resultadosprueba5[0]["value"]

#Lifetime Post Total Impressions
token6 = resultadosprueba[3]['access_token']
me3= owned_apps[3]['id']
api6= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_posts_impressions?access_token='+token6
print(api6)
headers6 = {
    'Content-Type': 'application/json'
                }
responseprueba6=requests.get(api6,stream=True,headers=headers6)
#print(response.url)
responseprueba6 = responseprueba6.json()
resultadosprueba6=responseprueba6["data"][0]["values"]
resultadospruebafinal4=resultadosprueba6[0]["value"]

#Lifetime Post Total organic Impressions
token7 = resultadosprueba[3]['access_token']
me3= owned_apps[3]['id']
api7= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_posts_impressions_organic?access_token='+token7
print(api7)
headers7 = {
    'Content-Type': 'application/json'
                }
responseprueba7=requests.get(api7,stream=True,headers=headers7)
#print(response.url)
responseprueba7 = responseprueba7.json()
resultadosprueba7=responseprueba7["data"][0]["values"]
resultadospruebafinal5=resultadosprueba7[0]["value"]

#Lifetime Post Total Paid Impressions
token8 = resultadosprueba[3]['access_token']
me3= owned_apps[3]['id']
api8= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_posts_impressions_paid?access_token='+token8
print(api8)
headers8 = {
    'Content-Type': 'application/json'
                }
responseprueba8=requests.get(api8,stream=True,headers=headers8)
#print(response.url)
responseprueba8 = responseprueba8.json()
resultadosprueba8=responseprueba8["data"][0]["values"]
resultadospruebafinal6=resultadosprueba8[0]["value"]

#Lifetime Engaged Users
token9 = resultadosprueba[3]['access_token']
me3= owned_apps[3]['id']
api9= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_posts_engaged_users?access_token='+token9
print(api9)
headers9 = {
    'Content-Type': 'application/json'
                }
responseprueba9=requests.get(api9,stream=True,headers=headers9)
#print(response.url)
responseprueba9 = responseprueba9.json()
resultadosprueba9=responseprueba9["data"][0]["values"]
resultadospruebafinal7=resultadosprueba9[0]["value"]

#Lifetime Negative Feedback from Users
token10 = resultadosprueba[3]['access_token']
me3= owned_apps[3]['id']
api10= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_posts_negative_feedback_unique?access_token='+token10
print(api10)
headers10 = {
    'Content-Type': 'application/json'
                }
responseprueba10=requests.get(api10,stream=True,headers=headers10)
#print(response.url)
responseprueba10 = responseprueba10.json()
resultadosprueba10=responseprueba10["data"][0]["values"]
resultadospruebafinal8=resultadosprueba10[0]["value"]


#Lifetime Negative Feedback
token11 = resultadosprueba[3]['access_token']
me3= owned_apps[3]['id']
api11= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_posts_negative_feedback?access_token='+token11
print(api11)
headers11 = {
    'Content-Type': 'application/json'
                }
responseprueba11=requests.get(api11,stream=True,headers=headers11)
#print(response.url)
responseprueba11 = responseprueba11.json()
resultadosprueba11=responseprueba11["data"][0]["values"]
resultadospruebafinal9=resultadosprueba11[0]["value"]


#Reacciones
token13 = resultadosprueba[3]['access_token']
me3= owned_apps[0]['id']
api13= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_reactions_by_type_total?access_token='+token13
print(api13)
headers13 = {
    'Content-Type': 'application/json'
                }
responseprueba13=requests.get(api13,stream=True,headers=headers13)
#print(response.url)
responseprueba13 = responseprueba13.json()
resultadosprueba13=responseprueba13["data"][0]["values"]
resultadospruebafinal11=resultadosprueba13[0]["value"]


# #Link clicks
# token13 = resultadosprueba[3]['access_token']
# me3= owned_apps[3]['id']
# api14= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_post_consumptions?access_token='+token13+'&period=day&since='+fecha2+'&until='+fecha1
# print(api13)
# headers13 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba13=requests.get(api14,stream=True,headers=headers13)
# #print(response.url)
# responseprueba13 = responseprueba13.json()
# resultadosprueba13=responseprueba13["data"][0]["values"]
# resultadospruebafinal11=resultadosprueba13[0]["value"]




listafinal2=[]
listafinal2 = {'Resultados' : pd.Series([cantidad,resultadospruebafinal1,resultadospruebafinal2,
                                         resultadospruebafinal3,resultadospruebafinal4,
                                         resultadospruebafinal5,resultadospruebafinal6,
                                         resultadospruebafinal7,resultadospruebafinal8,
                                         resultadospruebafinal9,resultadospruebafinal10,
                                         resultadospruebafinal11,resultadospruebafinal12,
                                         resultadospruebafinal13], index =['Cantidad de publicaciones',
                                        'Lifetime Post Total Reach','Lifetime Post organic reach',
                                        'Lifetime Post Paid Reach','Lifetime Post Total Impressions',
                                        'Lifetime Post Organic Impressions','Lifetime Post Paid Impressions',
                                        'Lifetime Engaged Users','Lifetime Negative Feedback from Users',
                                        'Lifetime Negative Feedback','Like','Link clicks','Visualizaciones de video totales Total',
                                        'Reproducciones totales de 30 segundos Total'])}

dataframefinal = pd.DataFrame(listafinal2)

dataframefinal.to_excel('Indicadores.xlsx', sheet_name='DetallePagina',index=True)
subir_archivo('Indicadores.xlsx','1YmZfGqBMIFN9pBgRElTo8fIa5DeGJ0ZT')