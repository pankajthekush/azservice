
import boto3
import json
import os
from botocore.exceptions import ClientError
import sys
import time


def return_session(bucket_name,credential_json_file = 'keys.json'):
    accesskey,secretkey = None,None
    with open(credential_json_file) as f:
        creds = json.load(f)
        accesskey,secretkey = creds['acces_key'],creds['secret_access_key']

    session = boto3.Session(aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    return bucket



def upload_file(bucket_name,file_name,in_sub_folder):
    fname = os.path.basename(file_name)
    str_dt = time.strftime("%m%d%Y")

    key = f'{in_sub_folder}/{str_dt}/{fname}'
    already_exists = list(bucket_name.objects.filter(Prefix=key)).__len__() > 0
    
    if not already_exists:
        print(f'Uploaindg : {key}...')
        bucket_name.upload_file(fname,Key=key)
    else:
        print(f'File {key} already exits Skipping')


def is_already_exist(bucket_name,file_name,in_sub_folder):
    fname = os.path.basename(file_name)
    str_dt = time.strftime("%m%d%Y")
    key = f'{in_sub_folder}/{str_dt}/{fname}'
    already_exists = list(bucket_name.objects.filter(Prefix=key)).__len__() > 0
    
    if not already_exists:
        return False
    else:
        return True



if __name__ == "__main__":
    bckt = return_session('kapowautostorerhoaiindia')
    print (is_already_exist(bckt,'setup.py','LinkedIn/Profiles'))
    