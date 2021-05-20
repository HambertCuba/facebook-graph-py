# -*- coding: utf-8 -*-

import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import webbrowser
import time
import pandas
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
#from googledrive import subir_archivo
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from googleapiclient.discovery import build
from google.oauth2 import service_account
import sys
import logging
import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser



canal_com= "UCLtGUPjKLqa3zgdmhKCZONg"
api_key= "AIzaSyBFTQ6Co8paqw0PBh-vupCKjvfgU5OcwJk"
api= 'https://www.googleapis.com/youtube/v3/search?key='+api_key+'&channelId='+canal_com+'&part=snippet,id&order=date'
print(api)
headers1 = {
    'Content-Type': 'application/json'
                }
responseprueba=requests.get(api,stream=True,headers=headers1)
#print(response.url)
responseprueba = responseprueba.json()
  
  