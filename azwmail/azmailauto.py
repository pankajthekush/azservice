from azwmail import send_email2,imap_session
import email

def read_message():
    server = imap_session()
    server.select('INBOX')
    _,response = server.search(None,'(UNSEEN)')
    
    new_messages = response[0].split()
    count_messages = len(new_messages)
    
    for m_id in new_messages:
        m_status, m_data = server.fetch(m_id, '(RFC822)')

        input(m_status)

        email_content = m_data[0][1]
        msg = email.message_from_bytes(email_content) # this needs to be corrected in your case 
        

        msg = email.message_from_string(new_messages[0][1])

        input(msg)
        #stat,m_subject = server.fetch(m_id, '(UID BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
        stat,m_subject = server.fetch(m_id, '(UID BODY.PEEK[TEXT])')
        input(m_subject)
    server.close()



if __name__ == "__main__":
    read_message()