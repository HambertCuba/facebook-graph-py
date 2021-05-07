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

#sacar las publicaciones por cada objeto de la lista
token1 = resultadosprueba[3]['access_token']
me2= resultadosprueba[3]['id']
api2= "https://graph.facebook.com/"+'v10.0'+'/'+me2+'/'+'published_posts?access_token='+token1+'&period=day&since='+fecha2+'&until='+fecha1
print(api2)
headers2 = {
    'Content-Type': 'application/json'
                }
responseprueba2=requests.get(api2,stream=True,headers=headers2)
#print(response.url)
responseprueba2 = responseprueba2.json()
resultadosprueba2=responseprueba2["data"]
#print(resultadosprueba2[0]['id'])

#######################parametros para la pagina
#Lifetime Post Total Reach
token3 = resultadosprueba[3]['access_token']
me3= resultadosprueba[3]['id']
api3= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_impressions_unique?access_token='+token3+'&period=day&since='+fecha2+'&until='+fecha1
print(api3)
headers3 = {
    'Content-Type': 'application/json'
                }
responseprueba3=requests.get(api3,stream=True,headers=headers3)
#print(response.url)
responseprueba3 = responseprueba3.json()
resultadosprueba3=responseprueba3["data"][0]["values"]
resultadospruebafinal1=resultadosprueba3[0]["value"]

#resultadosprueba2=responseprueba2["data"]


#Lifetime Post organic reach
token4 = resultadosprueba[3]['access_token']
me3= resultadosprueba[3]['id']
api4= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_impressions_organic_unique?access_token='+token4+'&period=day&since='+fecha2+'&until='+fecha1
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
me3= resultadosprueba[3]['id']
api5= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_impressions_paid_unique?access_token='+token5+'&period=day&since='+fecha2+'&until='+fecha1
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
me3= resultadosprueba[3]['id']
api6= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_impressions?access_token='+token6+'&period=day&since='+fecha2+'&until='+fecha1
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
me3= resultadosprueba[3]['id']
api7= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_impressions_organic?access_token='+token7+'&period=day&since='+fecha2+'&until='+fecha1
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
me3= resultadosprueba[3]['id']
api8= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_impressions_paid?access_token='+token8+'&period=day&since='+fecha2+'&until='+fecha1
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
me3= resultadosprueba[3]['id']
api9= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_engaged_users?access_token='+token9+'&period=day&since='+fecha2+'&until='+fecha1
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
me3= resultadosprueba[3]['id']
api10= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_negative_feedback_unique?access_token='+token10+'&period=day&since='+fecha2+'&until='+fecha1
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
me3= resultadosprueba[3]['id']
api11= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_negative_feedback?access_token='+token11+'&period=day&since='+fecha2+'&until='+fecha1
print(api11)
headers11 = {
    'Content-Type': 'application/json'
                }
responseprueba11=requests.get(api11,stream=True,headers=headers11)
#print(response.url)
responseprueba11 = responseprueba11.json()
resultadosprueba11=responseprueba11["data"][0]["values"]
resultadospruebafinal9=resultadosprueba11[0]["value"]


#Like
token12 = resultadosprueba[3]['access_token']
me3= resultadosprueba[3]['id']
api12= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_actions_post_reactions_like_total?access_token='+token12+'&period=day&since='+fecha2+'&until='+fecha1
print(api12)
headers12 = {
    'Content-Type': 'application/json'
                }
responseprueba12=requests.get(api12,stream=True,headers=headers12)
#print(response.url)
responseprueba12 = responseprueba12.json()
resultadosprueba12=responseprueba12["data"][0]["values"]
resultadospruebafinal10=resultadosprueba12[0]["value"]


#Link clicks
token13 = resultadosprueba[3]['access_token']
me3= resultadosprueba[3]['id']
api13= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_consumptions?access_token='+token13+'&period=day&since='+fecha2+'&until='+fecha1
print(api13)
headers13 = {
    'Content-Type': 'application/json'
                }
responseprueba13=requests.get(api13,stream=True,headers=headers13)
#print(response.url)
responseprueba13 = responseprueba13.json()
resultadosprueba13=responseprueba13["data"][0]["values"]
resultadospruebafinal11=resultadosprueba13[0]["value"]


#Visualizaciones de video totales Total
token14 = resultadosprueba[3]['access_token']
me3= resultadosprueba[3]['id']
api14= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_video_views?access_token='+token14+'&period=day&since='+fecha2+'&until='+fecha1
print(api14)
headers14 = {
    'Content-Type': 'application/json'
                }
responseprueba14=requests.get(api14,stream=True,headers=headers14)
#print(response.url)
responseprueba14 = responseprueba14.json()
resultadosprueba14=responseprueba14["data"][0]["values"]
resultadospruebafinal12=resultadosprueba14[0]["value"]

#Reproducciones totales de 30 segundos Total
token15 = resultadosprueba[3]['access_token']
me3= resultadosprueba[3]['id']
api15= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/page_video_complete_views_30s?access_token='+token14+'&period=day&since='+fecha2+'&until='+fecha1
print(api15)
headers15 = {
    'Content-Type': 'application/json'
                }
responseprueba15=requests.get(api15,stream=True,headers=headers15)
#print(response.url)
responseprueba15 = responseprueba15.json()
resultadosprueba15=responseprueba15["data"][0]["values"]
resultadospruebafinal13=resultadosprueba15[0]["value"]

listafinal = {resultadospruebafinal1,resultadospruebafinal2,resultadospruebafinal3,
                              resultadospruebafinal4,resultadospruebafinal5,resultadospruebafinal6,
                              resultadospruebafinal7,resultadospruebafinal8,resultadospruebafinal9,
                              resultadospruebafinal10,resultadospruebafinal11,resultadospruebafinal12,
                              resultadospruebafinal13}




listafinal2 = {'Resultados' : pd.Series([resultadospruebafinal1,resultadospruebafinal2], index =['Life', 
                                                                                                 'Life2'])}

dataframefinal = pd.DataFrame(listafinal2)

dataframefinal.to_excel('Libro.xlsx', sheet_name='Detalle',index=True)
subir_archivo('Libro.xlsx','1YmZfGqBMIFN9pBgRElTo8fIa5DeGJ0ZT')