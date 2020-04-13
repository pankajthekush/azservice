from azwmail import send_email2,imap_session
import email
import os
from pathlib import Path
import json


def config_file():
    config_file_path = os.path.join(Path.home(),'config.json')

    if os.path.exists(config_file_path):
        jobj = dict()    
        with  open(config_file_path,'r',encoding='utf-8') as f:
            jobj = json.load(f)
        
        try:
            trigger_subject = jobj['trigger_subjecr']
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





def read_message():
    server = imap_session()
    server.select('INBOX')
    _,response = server.search(None,'(UNSEEN)')
    
    new_messages = response[0].split()
    count_messages = len(new_messages)
    
    for m_id in new_messages:
        #m_status, m_data = server.fetch(m_id, '(RFC822)')
        m_status, m_data = server.fetch(m_id, 'BODY.PEEK[]')
        if m_status =='OK':     
            email_content = m_data[0][1]
            msg = email.message_from_bytes(email_content) # this needs to be corrected in your case
            subject = msg['SUBJECT']
            if 'TRIGGER:' in subject:
                m_status, m_data = server.fetch(m_id, '(RFC822)') #set it seen by actually fetching
                                                                  #this step is redundent but needs to be done
                print(subject)
                #send a reply
            else:
                pass
            


    server.close()



if __name__ == "__main__":
    read_message()
    #config_file()