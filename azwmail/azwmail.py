import smtplib,ssl
import imaplib
import os
from email.message import EmailMessage
import tkinter as tk
from tkinter import filedialog
import keyring
import time
import sys
current_path = os.path.dirname(os.path.abspath(__file__))



username = ''
service_name = 'workmail'
password = None
sys.platform
if sys.platform == 'linux':
    ufilename = 'uname.txt'
    pfilename ='paswd.txt'
else:
    ufilename = os.path.join(current_path,'uname.txt')


def return_username_file():
    global username
    if os.path.exists(ufilename):
        with open(ufilename,'r') as f:
            username = f.readline()

    else:
        with open(ufilename,'w') as f:
            email = input("Please enter robot email id : ")
            f.write(email)
        with open(ufilename,'r') as f:
            username = f.readline()
    return username

def return_password_file():
    global pfilename
    if os.path.exists(pfilename):
        with open(pfilename,'r') as f:
            password = f.readline()

    else:
        with open(pfilename,'w') as f:
            password = input("Please enter robot password, this will be stored in plain text : ")
            f.write(password)
        with open(pfilename,'r') as f:
            password = f.readline()
    return password



def get_credentials():

    username = return_username_file()

    if sys.platform == 'linux':
        creds = return_password_file()
        return username,creds
    creds = None    
    creds = keyring.get_password(service_name=service_name,username=username)


    if creds is None:
        set_credentials()
        creds = keyring.get_password(service_name=service_name,username=username)
    
    return username,creds
    

def set_credentials():
    
    _username = return_username_file()
    _password = input(f"Enter Password for {username}: ")
    keyring.set_password(service_name=service_name,username=_username,password=_password)
    


def return_email_session():
    username,password =get_credentials()
    server = None

    #sometime server connection is not done , so try 10 time befor giving up
    for _ in range(10):
        try:
            server = smtplib.SMTP_SSL('smtp.mail.us-east-1.awsapps.com',465)
            server.ehlo()
            server.login(username,password)
            break
        except:
            server = None
            time.sleep(10)
            
    if server is None:
        #even after 10 attemts server connection is not established
        #screw this and return none
        return None
    
    
    return server

def imap_session():
    username,password =get_credentials()
    server = imaplib.IMAP4_SSL('imap.mail.us-east-1.awsapps.com',993)
    server.login(username,password)
    return server


def send_email2(send_to,body,subject,attacment_dir= None):
    username,_ = get_credentials()
    e_msg = EmailMessage()
    e_msg.set_content(body)
    e_msg['Subject'] = subject
    e_msg['From'] = username
    e_msg['To'] = send_to


    server = return_email_session()

    if server is None:
        #connection to servr not established exiting
        print('connection with server could not be established.no email')
        return 0

    if not attacment_dir is None:
        for fname in os.listdir(attacment_dir):
            full_path = os.path.join(attacment_dir,fname)
            if not os.path.isfile(full_path):
                continue
            # use a generic bag-of-bits type.
            #https://docs.python.org/3/library/email.examples.html#id3
            maintype,subtype = 'application','octet-stream'
            with open(full_path,'rb') as fp:
                e_msg.add_attachment(fp.read(),maintype=maintype,subtype=subtype,filename=fname)
    try:
        server.send_message(e_msg)
    except Exception as e:
        print(e)
    try:
        server.quit()
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    send_email2(send_to='pankaj.kushwaha@rho.ai',body='THIS IS new with atta',subject='THIS IS SUB',attacment_dir=None) 
