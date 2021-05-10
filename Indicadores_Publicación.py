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
from datetime import datetime, date, timedelta
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
api2= "https://graph.facebook.com/"+'v10.0'+'/'+me2+'/'+'published_posts?access_token='+token1+'&period=day&since='+fecha2+'&until='+fecha2+' 23:59:59&limit=100'
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

#fecha de publicacion--prueba
fecha = owned_apps[0]['created_time']
fecha= fecha[0:10]

#####################ITERACION PARA METRICA 1 ################
#Lifetime Post Total Reach
token3 = resultadosprueba[3]['access_token']
headers3 = {
    'Content-Type': 'application/json'
                }
item2=0
listaReach=[]
while item2 <= len(owned_apps):
    resultadosprueba_1=[]
    ##api3= "https://graph.facebook.com/"+'v10.0'+'/'+listatemp[item2]['id_pub']+'/insights/post_impressions_unique?access_token='+token3
    api=""
    api="https://graph.facebook.com/"+'v10.0'+'/'+owned_apps[item2]['id']+'/insights/post_impressions_unique?access_token='+token3
    print(api)    
    responseprueba_1=requests.get(api,
                                 stream=True,
                                 headers=headers3)
    responseprueba_1 = responseprueba_1.json()
    resultadosprueba_1=responseprueba_1["data"][0]["values"]
    resultadospruebafinal_1=resultadosprueba_1[0]["value"]
    fechapub11=owned_apps[item2]['created_time']
    id_22=owned_apps[item2]['id']
    titulo22=owned_apps[item2]['message']
    listaReach.append( ##formato para agregar a una lista de forma manual
        {
             "Fecha Publicación":fechapub11,
             "ID Publicación":id_22,
             "Título Publicación":titulo22,
             "Lifetime Post Total Reach":resultadospruebafinal_1,
        }
    )
    item2+=1
    if item2==len(owned_apps):
        print(item2)
        break
##########################CREACION PRUEBA DATAFRAME PARA LA METRICA###################
listaReach=pd.DataFrame(listaReach)
#asdq=asdq.insert(4, "Prueba2",asdq.columns[3])
#asdq.to_excel('Indicadores_v2.xlsx', sheet_name='Metricas',index=False)
#asdq.to_excel('Indicadores_v3.xlsx', sheet_name='Metricas',columns=["Lifetime Post Total Reach"],index=False,startcol=5)


###########################
# #Lifetime Post Total Reach
# token3 = resultadosprueba[3]['access_token']
# me3= owned_apps[3]['id']
# api3= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_impressions_unique?access_token='+token3
# print(api3)
# headers3 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba3=requests.get(api3,stream=True,headers=headers3)
# #print(response.url)
# responseprueba3 = responseprueba3.json()
# resultadosprueba3=responseprueba3["data"][0]["values"]
# resultadospruebafinal1=resultadosprueba3[0]["value"]
############################

# #Lifetime Post organic reach
# token4 = resultadosprueba[3]['access_token']
# me3= owned_apps[3]['id']
# api4= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_impressions_organic_unique?access_token='+token4
# print(api4)
# headers4 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba4=requests.get(api4,stream=True,headers=headers4)
# #print(response.url)
# responseprueba4 = responseprueba4.json()
# resultadosprueba4=responseprueba4["data"][0]["values"]
# resultadospruebafinal2=resultadosprueba4[0]["value"]


#####################ITERACION PARA METRICA 2 ################
#Lifetime Post organic reach
token3 = resultadosprueba[3]['access_token']
headers3 = {
    'Content-Type': 'application/json'
                }
item2=0
listaReachOrganic=[]
while item2 <= len(owned_apps):
    resultadosprueba_2=[]
    ##api3= "https://graph.facebook.com/"+'v10.0'+'/'+listatemp[item2]['id_pub']+'/insights/post_impressions_unique?access_token='+token3
    api=""
    api="https://graph.facebook.com/"+'v10.0'+'/'+owned_apps[item2]['id']+'/insights/post_impressions_organic_unique?access_token='+token3
    print(api)
    responseprueba_2=requests.get(api,
                                 stream=True,
                                 headers=headers3)
    responseprueba_2 = responseprueba_2.json()
    resultadosprueba_2=responseprueba_2["data"][0]["values"]
    resultadospruebafinal_2=resultadosprueba_2[0]["value"]
    fechapub11=owned_apps[item2]['created_time']
    id_22=owned_apps[item2]['id']
    titulo22=owned_apps[item2]['message']
    listaReachOrganic.append( ##formato para agregar a una lista de forma manual
        {
             "ID Publicación":id_22,
             "Lifetime Post organic reach":resultadospruebafinal_2,
        }
    )
    item2+=1
    if item2==len(owned_apps):
        print(item2)
        break
##########################CREACION PRUEBA DATAFRAME PARA LA METRICA###################
listaReachOrganic=pd.DataFrame(listaReachOrganic)
#asdq.to_excel('PruebaCelda2.xlsx', sheet_name='TotalReach',columns=["Lifetime Post organic reach"],index=False,startcol=4)

#uniendo dataframe
listaReach=listaReach.merge(listaReachOrganic,on="ID Publicación",how="left")

# #Lifetime Post Paid Reach
# token5 = resultadosprueba[3]['access_token']
# me3= owned_apps[3]['id']
# api5= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_impressions_paid_unique?access_token='+token5
# print(api5)
# headers5 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba5=requests.get(api5,stream=True,headers=headers5)
# #print(response.url)
# responseprueba5 = responseprueba5.json()
# resultadosprueba5=responseprueba5["data"][0]["values"]
# resultadospruebafinal3=resultadosprueba5[0]["value"]

#####################ITERACION PARA METRICA 3 ################
#Lifetime Post Paid Reach
token3 = resultadosprueba[3]['access_token']
headers3 = {
    'Content-Type': 'application/json'
                }
item2=0
listaReachPaid=[]
while item2 <= len(owned_apps):
    resultadosprueba_3=[]
    ##api3= "https://graph.facebook.com/"+'v10.0'+'/'+listatemp[item2]['id_pub']+'/insights/post_impressions_unique?access_token='+token3
    api=""
    api="https://graph.facebook.com/"+'v10.0'+'/'+owned_apps[item2]['id']+'/insights/post_impressions_paid_unique?access_token='+token3
    #print(api)
    responseprueba_3=requests.get(api,
                                 stream=True,
                                 headers=headers3)
    responseprueba_3 = responseprueba_3.json()
    resultadosprueba_3=responseprueba_3["data"][0]["values"]
    resultadospruebafinal_3=resultadosprueba_3[0]["value"]
    fechapub11=owned_apps[item2]['created_time']
    id_22=owned_apps[item2]['id']
    titulo22=owned_apps[item2]['message']
    listaReachPaid.append( ##formato para agregar a una lista de forma manual
        {
             "ID Publicación":id_22,
             "Lifetime Post Paid Reach":resultadospruebafinal_3,
        }
    )
    item2+=1
    if item2==len(owned_apps):
        print(item2)
        break
##########################CREACION PRUEBA DATAFRAME PARA LA METRICA###################
listaReachPaid=pd.DataFrame(listaReachPaid)
#asdq.to_excel('PruebaCelda2.xlsx', sheet_name='TotalReach',columns=["Lifetime Post Paid Reach"],index=False,startcol=4)

#uniendo dataframe2
listaReach=listaReach.merge(listaReachPaid,on="ID Publicación",how="left")

# #Lifetime Post Total Impressions
# token6 = resultadosprueba[3]['access_token']
# me3= owned_apps[3]['id']
# api6= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_impressions?access_token='+token6
# print(api6)
# headers6 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba6=requests.get(api6,stream=True,headers=headers6)
# #print(response.url)
# responseprueba6 = responseprueba6.json()
# resultadosprueba6=responseprueba6["data"][0]["values"]
# resultadospruebafinal4=resultadosprueba6[0]["value"]


#####################ITERACION PARA METRICA 4 ################
#Lifetime Post Total Impressions
token3 = resultadosprueba[3]['access_token']
headers3 = {
    'Content-Type': 'application/json'
                }
item2=0
listaImpressions=[]
while item2 <= len(owned_apps):
    resultadosprueba_4=[]
    ##api3= "https://graph.facebook.com/"+'v10.0'+'/'+listatemp[item2]['id_pub']+'/insights/post_impressions_unique?access_token='+token3
    api=""
    api="https://graph.facebook.com/"+'v10.0'+'/'+owned_apps[item2]['id']+'/insights/post_impressions?access_token='+token3
    #print(api)
    responseprueba_4=requests.get(api,
                                 stream=True,
                                 headers=headers3)
    responseprueba_4 = responseprueba_4.json()
    resultadosprueba_4=responseprueba_4["data"][0]["values"]
    resultadospruebafinal_4=resultadosprueba_4[0]["value"]
    fechapub11=owned_apps[item2]['created_time']
    id_22=owned_apps[item2]['id']
    titulo22=owned_apps[item2]['message']
    listaImpressions.append( ##formato para agregar a una lista de forma manual
        {
             "ID Publicación":id_22,
             "Lifetime Post Total Impressions":resultadospruebafinal_4,
        }
    )
    item2+=1
    if item2==len(owned_apps):
        print(item2)
        break
##########################CREACION PRUEBA DATAFRAME PARA LA METRICA###################
listaImpressions=pd.DataFrame(listaImpressions)
#asdq.to_excel('PruebaCelda2.xlsx', sheet_name='TotalReach',columns=["Lifetime Post Total Impressions"],index=False,startcol=4)

#uniendo dataframe3
listaReach=listaReach.merge(listaImpressions,on="ID Publicación",how="left")


# #Lifetime Post Total organic Impressions
# token7 = resultadosprueba[3]['access_token']
# me3= owned_apps[3]['id']
# api7= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_impressions_organic?access_token='+token7
# print(api7)
# headers7 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba7=requests.get(api7,stream=True,headers=headers7)
# #print(response.url)
# responseprueba7 = responseprueba7.json()
# resultadosprueba7=responseprueba7["data"][0]["values"]
# resultadospruebafinal5=resultadosprueba7[0]["value"]

#####################ITERACION PARA METRICA 5 ################
#Lifetime Post Total organic Impressions
token3 = resultadosprueba[3]['access_token']
headers3 = {
    'Content-Type': 'application/json'
                }
item2=0
listaImpressionsOrganic=[]
while item2 <= len(owned_apps):
    resultadosprueba_5=[]
    ##api3= "https://graph.facebook.com/"+'v10.0'+'/'+listatemp[item2]['id_pub']+'/insights/post_impressions_unique?access_token='+token3
    api=""
    api="https://graph.facebook.com/"+'v10.0'+'/'+owned_apps[item2]['id']+'/insights/post_impressions_organic?access_token='+token3
    print(api)
    responseprueba_5=requests.get(api,
                                 stream=True,
                                 headers=headers3)
    responseprueba_5 = responseprueba_5.json()
    resultadosprueba_5=responseprueba_5["data"][0]["values"]
    resultadospruebafinal_5=resultadosprueba_5[0]["value"]
    fechapub11=owned_apps[item2]['created_time']
    id_22=owned_apps[item2]['id']
    titulo22=owned_apps[item2]['message']
    listaImpressionsOrganic.append( ##formato para agregar a una lista de forma manual
        {
             "ID Publicación":id_22,
             "Lifetime Post Total organic Impressions":resultadospruebafinal_5,
        }
    )
    item2+=1
    if item2==len(owned_apps):
        print(item2)
        break
##########################CREACION PRUEBA DATAFRAME PARA LA METRICA###################
listaImpressionsOrganic=pd.DataFrame(listaImpressionsOrganic)
#asdq.to_excel('PruebaCelda2.xlsx', sheet_name='TotalReach',columns=["Lifetime Post Total organic Impressions"],index=False,startcol=4)

#uniendo dataframe4
listaReach=listaReach.merge(listaImpressionsOrganic,on="ID Publicación",how="left")

# #Lifetime Post Total Paid Impressions
# token8 = resultadosprueba[3]['access_token']
# me3= owned_apps[3]['id']
# api8= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_impressions_paid?access_token='+token8
# print(api8)
# headers8 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba8=requests.get(api8,stream=True,headers=headers8)
# #print(response.url)
# responseprueba8 = responseprueba8.json()
# resultadosprueba8=responseprueba8["data"][0]["values"]
# resultadospruebafinal6=resultadosprueba8[0]["value"]

#####################ITERACION PARA METRICA 6 ################
#Lifetime Post Total Paid Impressions
token3 = resultadosprueba[3]['access_token']
headers3 = {
    'Content-Type': 'application/json'
                }
item2=0
listaImpressionsPaid=[]
while item2 <= len(owned_apps):
    resultadosprueba_6=[]
    ##api3= "https://graph.facebook.com/"+'v10.0'+'/'+listatemp[item2]['id_pub']+'/insights/post_impressions_unique?access_token='+token3
    api=""
    api="https://graph.facebook.com/"+'v10.0'+'/'+owned_apps[item2]['id']+'/insights/post_impressions_paid?access_token='+token3
    #print(api)
    responseprueba_6=requests.get(api,
                                 stream=True,
                                 headers=headers3)
    responseprueba_6 = responseprueba_6.json()
    resultadosprueba_6=responseprueba_6["data"][0]["values"]
    resultadospruebafinal_6=resultadosprueba_6[0]["value"]
    fechapub11=owned_apps[item2]['created_time']
    id_22=owned_apps[item2]['id']
    titulo22=owned_apps[item2]['message']
    listaImpressionsPaid.append( ##formato para agregar a una lista de forma manual
        {
             "ID Publicación":id_22,
             "Lifetime Post Total Paid Impressions":resultadospruebafinal_6,
        }
    )
    item2+=1
    if item2==len(owned_apps):
        print(item2)
        break
##########################CREACION PRUEBA DATAFRAME PARA LA METRICA###################
listaImpressionsPaid=pd.DataFrame(listaImpressionsPaid)
#asdq.to_excel('PruebaCelda2.xlsx', sheet_name='TotalReach',columns=["Lifetime Post Total Paid Impressions"],index=False,startcol=4)

#uniendo dataframe5
listaReach=listaReach.merge(listaImpressionsPaid,on="ID Publicación",how="left")

# #Lifetime Engaged Users
# token9 = resultadosprueba[3]['access_token']
# me3= owned_apps[3]['id']
# api9= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_engaged_users?access_token='+token9
# print(api9)
# headers9 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba9=requests.get(api9,stream=True,headers=headers9)
# #print(response.url)
# responseprueba9 = responseprueba9.json()
# resultadosprueba9=responseprueba9["data"][0]["values"]
# resultadospruebafinal7=resultadosprueba9[0]["value"]

#####################ITERACION PARA METRICA 7 ################
#Lifetime Engaged Users
token3 = resultadosprueba[3]['access_token']
headers3 = {
    'Content-Type': 'application/json'
                }
item2=0
listaEngaged=[]
while item2 <= len(owned_apps):
    resultadosprueba_7=[]
    ##api3= "https://graph.facebook.com/"+'v10.0'+'/'+listatemp[item2]['id_pub']+'/insights/post_impressions_unique?access_token='+token3
    api=""
    api="https://graph.facebook.com/"+'v10.0'+'/'+owned_apps[item2]['id']+'/insights/post_engaged_users?access_token='+token3
    #print(api)
    responseprueba_7=requests.get(api,
                                 stream=True,
                                 headers=headers3)
    responseprueba_7 = responseprueba_7.json()
    resultadosprueba_7=responseprueba_7["data"][0]["values"]
    resultadospruebafinal_7=resultadosprueba_7[0]["value"]
    fechapub11=owned_apps[item2]['created_time']
    id_22=owned_apps[item2]['id']
    titulo22=owned_apps[item2]['message']
    listaEngaged.append( ##formato para agregar a una lista de forma manual
        {
             "ID Publicación":id_22,
             "Lifetime Engaged Users":resultadospruebafinal_7,
        }
    )
    item2+=1
    if item2==len(owned_apps):
        print(item2)
        break
##########################CREACION PRUEBA DATAFRAME PARA LA METRICA###################
listaEngaged=pd.DataFrame(listaEngaged)
#asdq.to_excel('PruebaCelda2.xlsx', sheet_name='TotalReach',columns=["Lifetime Engaged Users"],index=False,startcol=4)

#uniendo dataframe6
listaReach=listaReach.merge(listaEngaged,on="ID Publicación",how="left")

# #Lifetime Negative Feedback from Users
# token10 = resultadosprueba[3]['access_token']
# me3= owned_apps[3]['id']
# api10= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_negative_feedback_unique?access_token='+token10
# print(api10)
# headers10 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba10=requests.get(api10,stream=True,headers=headers10)
# #print(response.url)
# responseprueba10 = responseprueba10.json()
# resultadosprueba10=responseprueba10["data"][0]["values"]
# resultadospruebafinal8=resultadosprueba10[0]["value"]


#####################ITERACION PARA METRICA 8 ################
#Lifetime Negative Feedback from Users
token3 = resultadosprueba[3]['access_token']
headers3 = {
    'Content-Type': 'application/json'
                }
item2=0
listaNegative=[]
while item2 <= len(owned_apps):
    resultadosprueba_8=[]
    ##api3= "https://graph.facebook.com/"+'v10.0'+'/'+listatemp[item2]['id_pub']+'/insights/post_impressions_unique?access_token='+token3
    api=""
    api="https://graph.facebook.com/"+'v10.0'+'/'+owned_apps[item2]['id']+'/insights/post_negative_feedback_unique?access_token='+token3
    #print(api)
    responseprueba_8=requests.get(api,
                                 stream=True,
                                 headers=headers3)
    responseprueba_8 = responseprueba_8.json()
    resultadosprueba_8=responseprueba_8["data"][0]["values"]
    resultadospruebafinal_8=resultadosprueba_8[0]["value"]
    fechapub11=owned_apps[item2]['created_time']
    id_22=owned_apps[item2]['id']
    titulo22=owned_apps[item2]['message']
    listaNegative.append( ##formato para agregar a una lista de forma manual
        {
             "ID Publicación":id_22,
             "Lifetime Negative Feedback from Users":resultadospruebafinal_8,
        }
    )
    item2+=1
    if item2==len(owned_apps):
        print(item2)
        break
##########################CREACION PRUEBA DATAFRAME PARA LA METRICA###################
listaNegative=pd.DataFrame(listaNegative)
#asdq.to_excel('PruebaCelda2.xlsx', sheet_name='TotalReach',columns=["Lifetime Negative Feedback from Users"],index=False,startcol=4)

#uniendo dataframe7
listaReach=listaReach.merge(listaNegative,on="ID Publicación",how="left")

# #Lifetime Negative Feedback
# token11 = resultadosprueba[3]['access_token']
# me3= owned_apps[3]['id']
# api11= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_negative_feedback?access_token='+token11
# print(api11)
# headers11 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba11=requests.get(api11,stream=True,headers=headers11)
# #print(response.url)
# responseprueba11 = responseprueba11.json()
# resultadosprueba11=responseprueba11["data"][0]["values"]
# resultadospruebafinal9=resultadosprueba11[0]["value"]

#####################ITERACION PARA METRICA 9 ################
#Lifetime Negative Feedback
token3 = resultadosprueba[3]['access_token']
headers3 = {
    'Content-Type': 'application/json'
                }
item2=0
listaFeedback=[]
while item2 <= len(owned_apps):
    resultadosprueba_9=[]
    ##api3= "https://graph.facebook.com/"+'v10.0'+'/'+listatemp[item2]['id_pub']+'/insights/post_impressions_unique?access_token='+token3
    api=""
    api="https://graph.facebook.com/"+'v10.0'+'/'+owned_apps[item2]['id']+'/insights/post_negative_feedback?access_token='+token3
    #print(api)
    responseprueba_9=requests.get(api,
                                 stream=True,
                                 headers=headers3)
    responseprueba_9 = responseprueba_9.json()
    resultadosprueba_9=responseprueba_9["data"][0]["values"]
    resultadospruebafinal_9=resultadosprueba_9[0]["value"]
    fechapub11=owned_apps[item2]['created_time']
    id_22=owned_apps[item2]['id']
    titulo22=owned_apps[item2]['message']
    listaFeedback.append( ##formato para agregar a una lista de forma manual
        {
             "ID Publicación":id_22,
             "Lifetime Negative Feedback":resultadospruebafinal_9,
        }
    )
    item2+=1
    if item2==len(owned_apps):
        print(item2)
        break
##########################CREACION PRUEBA DATAFRAME PARA LA METRICA###################
listaFeedback=pd.DataFrame(listaFeedback)
#asdq.to_excel('PruebaCelda2.xlsx', sheet_name='TotalReach',columns=["Lifetime Negative Feedback"],index=False,startcol=4)

#uniendo dataframe8
listaReach=listaReach.merge(listaFeedback,on="ID Publicación",how="left")

# #Reacciones
# token13 = resultadosprueba[3]['access_token']
# me3= owned_apps[0]['id']
# api13= "https://graph.facebook.com/"+'v10.0'+'/'+me3+'/insights/post_reactions_by_type_total?access_token='+token13
# print(api13)
# headers13 = {
#     'Content-Type': 'application/json'
#                 }
# responseprueba13=requests.get(api13,stream=True,headers=headers13)
# #print(response.url)
# responseprueba13 = responseprueba13.json()
# resultadosprueba13=responseprueba13["data"][0]["values"]
# resultadospruebafinal11=resultadosprueba13[0]["value"]
# anger=resultadospruebafinal11["anger"]
# haha=resultadospruebafinal11["haha"]
# like=resultadospruebafinal11["like"]
# love=resultadospruebafinal11["love"]
# sorry=resultadospruebafinal11["sorry"]
# wow=resultadospruebafinal11["wow"]

#####################ITERACION PARA METRICA 10 ################
#Reacciones
token3 = resultadosprueba[3]['access_token']
headers3 = {
    'Content-Type': 'application/json'
                }
item2=0
Reacciones=[]

while item2 <= len(owned_apps):
    resultadosprueba_10=[]
    ##api3= "https://graph.facebook.com/"+'v10.0'+'/'+listatemp[item2]['id_pub']+'/insights/post_impressions_unique?access_token='+token3
    api=""
    api="https://graph.facebook.com/"+'v10.0'+'/'+owned_apps[item2]['id']+'/insights/post_reactions_by_type_total?access_token='+token3
    #print(api)
    responseprueba_10=requests.get(api,
                                 stream=True,
                                 headers=headers3)
    responseprueba_10 = responseprueba_10.json()
    resultadosprueba_10=responseprueba_10["data"][0]["values"]
    resultadospruebafinal_10=resultadosprueba_10[0]["value"]
    try:
      anger=resultadospruebafinal_10["anger"]
    except(ValueError,KeyError,ZeroDivisionError,NameError):
        print('falla anger')  
        anger=0
    
    try:
      haha=resultadospruebafinal_10["haha"]
    except(ValueError,KeyError,ZeroDivisionError,NameError):
        print('falla haha')  
        anger=0
        
    try:
      like=resultadospruebafinal_10["like"]
    except(ValueError,KeyError,ZeroDivisionError,NameError):
        print('falla like')  
        like=0
        
    try:
      love=resultadospruebafinal_10["love"]
    except(ValueError,KeyError,ZeroDivisionError,NameError):
        print('falla love')  
        love=0
     
    try:
      sorry=resultadospruebafinal_10["sorry"]
    except(ValueError,KeyError,ZeroDivisionError,NameError):
        print('falla sorry')  
        sorry=0
    
    try:
      wow=resultadospruebafinal_10["wow"]
    except(ValueError,KeyError,ZeroDivisionError,NameError):
        print('falla sorry')  
        wow=0
    
    fechapub11=owned_apps[item2]['created_time']
    id_22=owned_apps[item2]['id']
    titulo22=owned_apps[item2]['message']
    Reacciones.append( ##formato para agregar a una lista de forma manual
        {
             "ID Publicación":id_22,
             "Like":like,
             "Me Encanta":love,
             "Me Entristece":sorry,
             "Me Asombra":wow,
             "Me Enfada":anger,
             "Me Divierte":haha,
        }
    )
    item2+=1
    if item2==len(owned_apps):
        print(item2)
        break
##########################CREACION PRUEBA DATAFRAME PARA LA METRICA###################
Reacciones=pd.DataFrame(Reacciones)
#asdq.to_excel('PruebaCelda2.xlsx', sheet_name='TotalReach',columns=["Lifetime Negative Feedback"],index=False,startcol=4)

#uniendo dataframe9
listaReach=listaReach.merge(Reacciones,on="ID Publicación",how="left")

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


listaReach.to_excel('IndicadoresPublicación.xlsx', sheet_name='DetallePublicación',index=True)
subir_archivo('IndicadoresPublicación.xlsx','1YmZfGqBMIFN9pBgRElTo8fIa5DeGJ0ZT')