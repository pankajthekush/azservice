from azwmail import send_email2,imap_session,get_credentials,return_email_session
import email
import os
from pathlib import Path
import json
import time
from email.utils import parseaddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage
import subprocess
from subprocess import check_output,PIPE,CREATE_NEW_CONSOLE
from signal import signal,SIGINT
import sys

username,_ = get_credentials()

server = None
def signal_handler(signal_received,frame):
    print('\n')
    print('closing connection')
    try:
        server.close()
        server.logout()
        sys.exit(0)
    except Exception:
        print('error while closing connection')
        sys.exit(1)


def config_file():
    config_file_path = os.path.join(Path.home(),'config.json')

    if os.path.exists(config_file_path):
        jobj = dict()    
        with  open(config_file_path,'r',encoding='utf-8') as f:
            jobj = json.load(f)
        
        try:
            trigger_subject = jobj['trigger_subject']
        except KeyError:
            jobj['trigger_subjecr'] = input('Enter trigger subject : ')
        
        with open(config_file_path,'w',encoding='utf-8') as fp:
            json.dump(jobj,fp)
                   
        return jobj
    else:
        dict_config_data = dict()
        num_instances = int(input('number of instances you are running : '))
        db_table_name = input('table name from database :')
        s3_bucket_name = input('s3 bucket name to upload :')
        s3_folder = input('s3 folder for upload :')
        notifier_name = input('emails delimiated by ; :')


        dict_config_data['num_instances'] = num_instances
        dict_config_data['db_table_name'] = db_table_name
        dict_config_data['s3_bucket_name'] = s3_bucket_name
        dict_config_data['s3_folder'] = s3_folder
        dict_config_data['notification_addr'] = notifier_name

        with open(config_file_path,'w',encoding='utf-8') as fp:
            json.dump(dict_config_data,fp)
        return dict_config_data

#https://stackoverflow.com/a/2189630/3025905
def create_reply_message(originalemail,mailcontent):
    #removing attachment
    for part in originalemail.walk():
        if(part.get('Content-Disposition') and part.get('Content-Disposition').startswih('attachment')):
            part.set_type('text/plain')
            part.set_payload("Attachment removed : %s (%s,%d,bytes)"%(part.get_filename(),
                                                                    part.get_content_type(),
                                                                    len(part.get_payload(decode=True))))
            del part['Content-Disposition']
            del part["Content-Transfer-Encoding"]
    #create reply email
    mailbody = f'your request executed through pid : {mailcontent}'
    new = MIMEMultipart('mixed')
    body = MIMEMultipart('alternative')
    body.attach(MIMEText(f'{mailbody}','plain'))
    body.attach(MIMEText(f'<html>{mailbody}</html>','html'))
    new.attach(body)
    new['Messasge-ID'] = email.utils.make_msgid()
    new['In-Reply-To'] = originalemail['Message-ID']
    new['Reference'] = originalemail['Message-ID']
    new['Subject'] = 'Re: '+originalemail['Subject']
    new['to']= originalemail['Reply-To']  or originalemail["From"]
    new['from'] = username
    #attach original email 
    new.attach(MIMEMessage(originalemail))
    smtp_session = return_email_session()
    #sendemail
    #input(new['to'])
    smtp_session.sendmail(username,[new['to']],new.as_string())
    smtp_session.quit()

def read_message():
    #Will read email, and take action
    global server
    server = imap_session()
    server.select('INBOX')

    for _ in range(100):
        signal(SIGINT, signal_handler)
        server.noop()
        _,response = server.search(None,'(UNSEEN)')
        new_messages = response[0].split()
        count_messages = len(new_messages)
        print(f'{count_messages} unread messages')
        
        for m_id in new_messages:
            #m_status, m_data = server.fetch(m_id, '(RFC822)')
            m_status, m_data = server.fetch(m_id, 'BODY.PEEK[]')
            if m_status =='OK':     
                email_content = m_data[0][1]
                msg = email.message_from_bytes(email_content)
                subject = msg['SUBJECT']
                if 'TRIGGER:' in subject:
                    m_status, m_data = server.fetch(m_id, '(RFC822)') #set it seen by actually fetching
                                                                    #this step is redundent but needs to be done
                    
                    command_name =  subject.split(':')[1].strip()
                    
                    invoke_cmd = command_name
                    handle_pid = None
                    handle = None
                    try:
                        handle = subprocess.Popen(invoke_cmd,creationflags=CREATE_NEW_CONSOLE)
                        handle_pid = handle.pid
                    except Exception as e:
                        handle_pid = e


                    create_reply_message(msg,mailcontent=str(handle_pid))
                    

                else:
                    print('no trigger found')
        
        time.sleep(10)       


    server.close()
    server.logout()




def read_message2(server,trigger_subject):
    #Will read email and return subject and body
    server = imap_session()
    server.select('INBOX')

    signal(SIGINT, signal_handler)
    server.noop()
    _,response = server.search(None,'(UNSEEN)')
    new_messages = response[0].split()
    count_messages = len(new_messages)
    print(f'{count_messages} unread messages')
    
    for m_id in new_messages:
        #m_status, m_data = server.fetch(m_id, '(RFC822)')
        m_status, m_data = server.fetch(m_id, 'BODY.PEEK[]')
        input(m_status)
        if m_status =='OK':     
            email_content = m_data[0][1]
            msg = email.message_from_bytes(email_content)
            subject = msg['SUBJECT']
            body = msg['BODY']

            input(trigger_subject)
            input(subject)

            if trigger_subject in subject:
                m_status, m_data = server.fetch(m_id, '(RFC822)') #set it seen by actually fetching,this step is redundent but needs to be done
                return 'TRIGGER',subject,body,msg
            else:
                return 'NOTRIGGER',subject,body,msg
    
    return 'NOEMAIL','NOEMAIL','NOEMAIL','NOEMAIL'


            







if __name__ == "__main__":
    server = imap_session()
    server.select('INBOX')

    t,_,_,_ = read_message2(server,'TRIGGER')
    #print(t)
    #config_file()
    server.close()
    server.logout()