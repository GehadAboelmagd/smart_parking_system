#built in python libraries
import sqlite3
import multiprocessing 
import datetime
import math
import random
import string
import os  , sys , time , io
import tkinter 
import serial

#non standard python libraries
import cv2
import psutil
import cProfile
import textract
import pyautogui
import numpy 
import pytesseract 

#for google gmail api
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials as ServiceCredentials
from google.oauth2.credentials import Credentials as UserCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#mime library for more rich message from email.mime.multipart import MIMEMultipart
import emoji
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.message import Message

##################################################################################################################################
#NOTE 1: also install tesseract on CMD : 

# 1) open CMD (AS admin)
# 2) run this command: @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
# 3) restart CMD ( now choco is installed)
# 4) run this command :choco install tesseract
# 5) DONE 
# *) make sure version is tesseract 5.3.0.20221214
# *) to get current installed versoin run this command: choco list --local-only tesseract 


#NOTE 2: for gmail api

# in cmd (AS ADMIN): pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client email