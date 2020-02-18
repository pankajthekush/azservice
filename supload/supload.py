
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
    try:
        client.upload_file(fname, Bucket=bucket_name ,Key=key)
    except:
        pass
        #File not uploaded
    

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
    pass
 