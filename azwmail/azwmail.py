import smtplib,ssl
import imaplib
import os
from email.message import EmailMessage
import tkinter as tk
from tkinter import filedialog
import keyring

current_path = os.path.dirname(os.path.abspath(__file__))


username = ''
service_name = 'workmail'
password = None

ufilename = os.path.join(current_path,'uname.txt')

if os.path.exists(ufilename):
    with open(ufilename,'r') as f:
        username = f.readline()

else:
    with open(ufilename,'w') as f:
        email = input("Please enter login email id : ")
        f.write(email)
    with open(ufilename,'r') as f:
        username = f.readline()


def get_credentials():
    creds = None
    creds = keyring.get_password(service_name=service_name,username=username)

    if creds is None:
        set_credentials()
        creds = keyring.get_password(service_name=service_name,username=username)
    
    return username,creds
    

def set_credentials():
    _username = username
    _password = input("Enter Password : ")
    keyring.set_password(service_name=service_name,username=_username,password=_password)
    


def return_email_session():
    username,password =get_credentials()
    server = smtplib.SMTP_SSL('smtp.mail.us-east-1.awsapps.com',465)
    server.ehlo()
    #input(f'{username},{password}')
    server.login(username,password)
    return server

def imap_session():
    username,password =get_credentials()
    server = imaplib.IMAP4_SSL('imap.mail.us-east-1.awsapps.com',993)
    server.login(username,password)
    return server


def send_email2(send_to,body,subject,attacment_dir= None):

    e_msg = EmailMessage()
    e_msg.set_content(body)
    e_msg['Subject'] = subject
    e_msg['From'] = username
    e_msg['To'] = send_to

    server = return_email_session()
    
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

    server.send_message(e_msg)

    server.close()
    
if __name__ == "__main__":
    send_email2(send_to='pankaj.kushwaha@rho.ai',body='THIS IS new with atta',subject='THIS IS SUB',attacment_dir='C:\\Users\\Pankaj\\Downloads\\test') 
