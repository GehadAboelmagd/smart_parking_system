
''' This uses shared google cloud project  with msp mini college system proj & parking smart system temproraily '''
from __future__ import print_function

import getpass
import os.path
import ssl
import smtplib

#user defined modules
from enm import enm 

# for google api
# from google.oauth2.service_account import Credentials as ServiceCredentials #not needed now 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as UserCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#mime library for more rich message from email.mime.multipart import MIMEMultipart
# from email.message import Message #for simpler messages
from email.mime.text import MIMEText
from  email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart # for complex messages 
from email.mime.application import MIMEApplication
from emoji import emojize

#mime types map (attach any file type)
mime_types = {
    '.ai': 'postscript',
    '.avi': 'x-msvideo',
    '.bmp': 'bmp',
    '.csv': 'csv',
    '.doc': 'msword',
    '.docx': 'vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.gif': 'gif',
    '.htm': 'html',
    '.html': 'html',
    '.ico': 'x-icon',
    '.jpeg': 'jpeg',
    '.jpg': 'jpeg',
    '.mp3': 'mpeg',
    '.mp4': 'mp4',
    '.mpeg': 'mpeg',
    '.pdf': 'pdf',
    '.png': 'png',
    '.ppt': 'vnd.ms-powerpoint',
    '.pptx': 'vnd.openxmlformats-officedocument.presentationml.presentation',
    '.ps': 'postscript',
    '.rar': 'x-rar-compressed',
    '.rtf': 'rtf',
    '.svg': 'svg+xml',
    '.tif': 'tiff',
    '.tiff': 'tiff',
    '.tsv': 'tsv',
    '.txt': 'plain',
    '.wav': 'x-wav',
    '.xls': 'vnd.ms-excel',
    '.xlsx': 'vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.zip': 'zip',
    # Add more mappings as needed
}


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

###################################################################################################
def gmail_setup():
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first time
	
	if os.path.exists('token.json'):
		creds = UserCredentials.from_authorized_user_file('./token.json', SCOPES)
		
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('./client_secret.json', SCOPES)
				
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next runs
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	try:
	# Call the Gmail API
		#uncomment next 2 lines to grant access using API_KEY 
		# API_KEY : str = ... #from your google cloud project
		# service = build ( 'gmail' , 'v1' , developerKey= API_KEY)

		#comment next one line if u used API_KEY
		service = build('gmail', 'v1', credentials=creds)
		results = service.users().labels().list(userId='me').execute()
		labels = results.get('labels', [])


	except HttpError as error:
		print(f'An Gmail HTTP error occurred: {error}')
		return enm.GMAIL_BAD

	return enm.GMAIL_OK

###################################################################################################
def get_sys_pass( is_auto : bool = True ) :
	if is_auto :
		_sys_pass = None 
		with open('sys_pass.txt', 'r') as pass_file_obj: # ideally sys_pass.txt is encrepted and we decrept it but its testing gmail so no worries
			_sys_pass = pass_file_obj.read().strip()

		return _sys_pass
				
	else :
		sys_gmail_password = getpass.getpass("ADMIN Please Enter Your system gmail password : \n>> ").strip()
		print("  ", end = '')
		for i in range(len(sys_gmail_password)) :
			print ('*' ,  end ='')
		print ('\n')
		print (sys_gmail_password)#TESTING
		return sys_gmail_password


###################################################################################################
def main_gmail(  _to_email : str , _from_email = "system.python.web@gmail.com" , _msg_title = 'Operation Status :check_mark_button:' ,  _msg_content = "empty msg"  , attach_file = False  , file_path : str = None) -> enm: 
	print ( "Starting  new Connection session with Gmail API... \n\n")
 
	state = gmail_setup() #validate that google auth your program through a saved carden file
	if  state == enm.GMAIL_OK : 
		print ("*SUCESSS: Gmail-API Granted Access to The System Succesfully!* \n\n")
	else :
		print("*FAIL: System might not Be  validated to  be able to Access  gmail!* \n please Auth. your system program  OR check your auth. certificate file... \n\n")

	try:
		# port = 465(legacy deprecated)  # For SSL -> other SMTP serverports can be found in web (587 .. etc)
		port = 587
		from_sys_gmail = _from_email
		to_gmail = _to_email
		sys_key = None
		with open('./sys_pass.txt' , 'r') as file:
			sys_key = file.read().strip()

		
		#fill in your message 
		message = MIMEMultipart()
		message['Subject'] = emojize(_msg_title)
		message['From'] = from_sys_gmail
		message['To'] = to_gmail

  
		if attach_file == True :
			MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024  # 10 MB
			attach_size = os.path.getsize(file_path)
			if attach_size > MAX_ATTACHMENT_SIZE:
				print (f"Warning!: your attachment file size exceeded max allowed size ({attach_size} > 10MB) \n message will be sent without attachment...")
			else:
				with open( file_path , 'rb') as attachment_file:
					file_extension = os.path.splitext(file_path)[1]
					mime_type = mime_types.get(file_extension, 'octet-stream')
					attachment = MIMEApplication(attachment_file.read(), _subtype=mime_type)
					attachment.add_header('Content-Disposition', 'attachment', filename=file_path)
					message.attach(attachment)
     
		#prepare and attach message body 
		formatted_msg = emojize(_msg_content)
		formatted_msg ="<p><h3> {0} </h3></P>".format(formatted_msg)
		message.set_payload(MIMEText(formatted_msg , 'html')) 

  
	# start a secure SSL connection
		#ssl(Secure Sockets Layer) = secure and encrypted communication channel 
		context = ssl.create_default_context()
		#establish smtp ssl/tls gmail server session
		server = smtplib.SMTP(host= "smtp.gmail.com", port= port)
		server.ehlo() #not needed if used SMTP_SSL()
		server.starttls(context = context)#not needed if used SMTP_SSL()
		print ("*SUCESSS: system is linked to SMTP server* \n\n")
		print("linking system  Gmail to SMTP_SSL Gmail server...\n\n ")
		server.login(from_sys_gmail, sys_key)
		del sys_key 
  
		#send email
		server.send_message(message , from_sys_gmail , to_gmail) #send right formatted email
  
		# message = _msg_content
		# server.sendmail(from_sys_gmail , to_gmail_add , message) #send row string email

	except Exception as gmail_con_err :
		os.system(r"cls") #unix : clear
		print("***ERROR CONNECTING TO YOUR GMAIL. terminating... ***")
		print(" Details: "  , gmail_con_err,"\n\n")
		return enm.GMAIL_BAD

		
			
	
		

	finally : 
		print (f"*SUCESSS: Email Has been sent to {to_gmail} * \n\n")
  
		print("*Gmail Session Ended* \n Deleting Cached User Data & Quiting session ...\n\n")
		del to_gmail #clear for end user data security
		del from_sys_gmail 
		del message
		server.quit()
		return enm.GMAIL_OK #sucess

if __name__ == '__main__':

	#TESTING
	tst_email = "omar1xd@gmail.com"
	tst_msg ="hi this is test message from api_gmail.py omar code  :automobile: :construction: (dont reply)"
	main_gmail( _to_email = tst_email  ,  _msg_content = tst_msg )