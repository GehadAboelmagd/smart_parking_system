
import os  , sys , time , io
import cv2
import psutil
import cProfile
import textract
import pyautogui
import numpy 
import pytesseract 
import multiprocessing 
import sqlite3
import datetime
import math
import random
import string
import tkinter 
import communicatoin 
import serial


#NOTE : also install tesseract on CMD : 
# open CMD (AS admin)
# run this command: @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
#restart CMD ( now choco is installed)
# run this command :choco install tesseract
#DONE 

#make sure version is tesseract 5.3.0.20221214
#to get current installed versoin run this command: choco list --local-only tesseract 