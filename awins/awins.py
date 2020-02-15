import boto3
from time import sleep
import subprocess

client = boto3.client('ec2', region_name='ap-south-1')
import logging
logging.basicConfig(level=logging.DEBUG)



import os
current_path = os.path.dirname(os.path.dirname(__file__))

def get_instance_id():
    if not os.path.exists(os.path.join(current_path,'instance_file.txt')):
        with open(os.path.join(current_path,'instance_file.txt'),'w') as f:
            instance_info = input('Enter Instance Name/Number : ')
            f.write(instance_info)

    else:
        with open(os.path.join(current_path,'instance_file.txt'),'r') as f:
            instance_info = f.readline()
    instance_info = instance_info.strip()
    return instance_info



def get_public_ip(instance_id = None):

    if instance_id is None:
        l_instance_id= []
        input_instance_id = get_instance_id()
        l_instance_id.append(input_instance_id)
    else:
        l_instance_id= []
        l_instance_id.append(instance_id)
    
    response = client.describe_instances(InstanceIds=l_instance_id)
    res_data = response['Reservations'][0]
    instances = res_data['Instances']
    
    status_name = instances[0]['State']['Name']
    status_code = instances[0]['State']['Code']

    if  status_code == 16:
        public_ip = instances[0]['PublicIpAddress']
    else:
        public_ip = 'notfound'
    return public_ip


def start_instance(instance_id = None):
    
    if instance_id is None:
        l_instance_id= []
        input_instance_id = get_instance_id()
        l_instance_id.append(input_instance_id)
    else:
        l_instance_id= []
        l_instance_id.append(instance_id)
    
    ins_state = get_instance_status(instance_id=instance_id)
    
    if (ins_state == 'RUNNING'):
        public_ip =  get_public_ip()
        logging.debug(f'Instance running at : {public_ip}')
        return public_ip

    elif(ins_state == 'INITIALIZING'):
        while (not ins_state == 'RUNNING') or (not ins_state == 'RUNNING') :
            logging.debug("System Already Initialized , waiting to close or start")
            if(ins_state == 'RUNNING'):
                public_ip =  get_public_ip()
                logging.debug(f'Instance running at : {public_ip}')
                return public_ip


    try:
        client.start_instances(InstanceIds=l_instance_id)
    except Exception:
        logging.debug('could not start instance, try again')
        return 'could not start instance, try again'
    ins_state = get_instance_status(instance_id=instance_id)

    while not (ins_state == 'RUNNING'):
        ins_state = get_instance_status(instance_id=instance_id)
        sleep(20)
    
    return get_public_ip()
        

def stop_instance(instance_id = None):
    

    if instance_id is None:
        l_instance_id= []
        input_instance_id = get_instance_id()
        l_instance_id.append(input_instance_id)

    else:
        l_instance_id= []
        l_instance_id.append(instance_id)
    
    client.stop_instances(InstanceIds=l_instance_id)
    
    ins_state = get_instance_status(instance_id=instance_id)

    while not (ins_state == 'STOPPED'):
        ins_state = get_instance_status(instance_id=instance_id)
        sleep(10)
    
    return 'STOPPED'

def get_instance_status(instance_id = None):
    
    if instance_id is None:
        l_instance_id = []
        input_instance_id = get_instance_id()
        l_instance_id.append(input_instance_id)
    else:
        l_instance_id= []
        l_instance_id.append(instance_id)

    InstanceState = None
    tanceStatus_reachability = None
    tanceStatus_status = None
    SystemStatus_reachablity = None
    SystemStatus_status = None
    
    dict_resp = client.describe_instance_status(InstanceIds=l_instance_id)
        
        
    try:
        all_status = dict_resp['InstanceStatuses'][0]
        InstanceState = all_status['InstanceState']['Name'] #should be running
        tanceStatus_reachability = all_status['InstanceStatus']['Details'][0]['Status'] #should be passed
        tanceStatus_status = all_status['InstanceStatus']['Status'] #should be ok
        SystemStatus_reachablity = all_status['SystemStatus']['Details'][0]['Status'] #should be passed
        SystemStatus_status = all_status['SystemStatus']['Status'] #should be ok

        logging.debug(f'Instance State :{InstanceState}')
        logging.debug(f'Instance Reachiblity :{tanceStatus_reachability}')
        logging.debug(f'Instance Status :{tanceStatus_status}')
        logging.debug(f'System Status :{SystemStatus_status}')
        logging.debug(f'System Reachiblity :{SystemStatus_status}')

        if (InstanceState == 'running' and 
                tanceStatus_reachability == 'passed' and 
                tanceStatus_status == 'ok'and 
                SystemStatus_reachablity == 'passed' and
                SystemStatus_status=='ok') :

                return 'RUNNING'
        else:
            return 'INITIALIZING'

    except Exception:
        tanceStatus_reachability = 'not found' #should be passed
        tanceStatus_status = 'not found' #should be ok
        SystemStatus_reachablity = 'not found' #should be passed
        SystemStatus_status = 'not found' #should be ok

        logging.debug(f'Instance State :{InstanceState}')
        logging.debug(f'Instance Reachiblity :{tanceStatus_reachability}')
        logging.debug(f'Instance Status :{tanceStatus_status}')
        logging.debug(f'System Status :{SystemStatus_status}')
        logging.debug(f'System Reachiblity :{SystemStatus_status}')
        
        return 'STOPPED'
        
        
    
def connect_rdp():
    public_ip = start_instance()

    if public_ip == 'notfound':
        logging.debug("Something Wrong, can't get public IP")
    else:
        aws_ip = f'/v:{public_ip}'
        subprocess.run(['mstsc',aws_ip])
    logging.debug("launched rdp")

if __name__ == "__main__":
    #print(stop_instance())
    #print(start_instance())
    #print(get_instance_id())
    get_instance_status()
    #get_public_ip()
    #connect_rdp()