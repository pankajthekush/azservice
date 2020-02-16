import smtplib,ssl
import os

import tkinter as tk
from tkinter import filedialog
import keyring

import logging

username = 'robot@rho-bot.awsapps.com'
service_name = 'workmail'
password = None

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
    server.login(username,password)
    return server

def send_email(send_to='pankaj.kushwaha@rho.ai'):
    server = return_email_session()
    server.sendmail(from_addr=username,to_addrs=send_to,msg='hello from cli')
    server.close()

if __name__ == "__main__":
    send_email()