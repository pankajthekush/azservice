
import boto3
import json
import os
from botocore.exceptions import ClientError
import sys
import time


def upload_file(file_name,in_sub_folder,bucket_name):
    client = boto3.client('s3')
    fname = os.path.basename(file_name)
    str_dt = time.strftime("%m%d%Y")
    key = f'{in_sub_folder}/{str_dt}/{fname}'

    s3_url = f's3://{bucket_name}/{key}'

    try:
        client.upload_file(file_name, Bucket=bucket_name ,Key=key)
        print(f'{fname}--->{key}')
        return True,s3_url
    except Exception as e:
        print(e)
        return False,s3_url
    

def is_already_exist(file_name,in_sub_folder,bucket_name):
    fname = os.path.basename(file_name)
    str_dt = time.strftime("%m%d%Y")
    key = f'{in_sub_folder}/{str_dt}/{fname}'

    client = boto3.client('s3')

    try:
        client.head_object(Bucket=bucket_name,Key=key)
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True


if __name__ == "__main__":
    print(upload_file('tes.txt','kapowautostorerhoaiindia/google-scrape/05202020','rhoaiautomationindias3'))
 
