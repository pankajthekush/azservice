from setuptools import setup

setup(
    name='supload',
    version='0.2',
    packages=['supload','awins'],
    install_requires=['boto3>=1.10.46'],
    entry_points ={'console_scripts': ['azrdp = awins.awins:connect_rdp',
                                        'azip = awins.awins:get_public_ip',
                                        'azstatus=awins.awins:get_instance_status',
                                        'azstop=awins.awins:stop_instance',
                                        'azstart=awins.awins:start_instance'
                                        ]}

)