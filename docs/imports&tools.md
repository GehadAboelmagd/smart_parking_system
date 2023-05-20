# Used Tools and Modules in Smart Parking System 


### Built in python libraries 

* sqlite3
* multiprocessing 
* datetime
* math
* random
* string
* os  , sys , time , io
* tkinter 
* serial
* concurrent.futures
* json
* base64

----
> ### Donwload non-standard python libraries

* `pip install cv2`
* `pip install`
* `pip install psutil`
* `pip install cProfile`
* `pip install textract`
* `pip install pyautogui`
* `pip install numpy`
* `pip install pytesseract`
* `pipr install emoji`

> ### Download for google Gmail API

* `pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`

-----

> ### Also install tesseract on CMD : 

 1. open CMD (AS admin)
 2. run this command: 
```cmd 
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin
```

 3. restart CMD ( now choco is installed)
 4. run this command :`choco install tesseract`
 5. DONE 
* _Note:_
 	* make sure version is tesseract 5.3.0.20221214
 	* to get current installed versoin run this command: `choco list --local-only tesseract`

