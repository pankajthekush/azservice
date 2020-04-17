from setuptools import setup
from setuptools import setup,find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from azwmail.azwmail import send_email2
from subprocess import check_call
from glob import glob
import os
import sys
#https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools

setup(
    name='azservice',
    version='0.4',
    packages=['supload','awins','azwmail'],
    install_requires=['boto3>=1.10.46','keyring>=21.1.0'],
    entry_points ={'console_scripts': ['azrdp = awins.awins:connect_rdp',
                                        'azip = awins.awins:get_public_ip',
                                        'azstatus=awins.awins:get_instance_status',
                                        'azstop=awins.awins:stop_instance',
                                        'azstart=awins.awins:start_instance'
                                        ]}

)