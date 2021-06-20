#!/usr/bin/python3
import os
import requests
from sys import argv


def generate_honeytoken(memo):
    multipart_form_data = {
        'type': 'web',
        'email': 'matthew.vorhees@gmail.com',
        'webhook': '',
        'fmt': '',
        'memo': memo,
        'clonedsite': '',
        'sql_server_table_name': 'TABLE1',
        'sql_server_view_name': 'VIEW1',
        'sql_server_function_name': 'FUNCTION1',
        'sql_server_trigger_name': 'TRIGGER1',
        'redirect_url': '',
    }
	
    session = requests.Session()

	# Send an HTTP POST request an existing comment with the stored XSS payload to send the cookie of any user navigating to this page back to our server.
    response = requests.post('https://canarytokens.org/generate', files=multipart_form_data)
	
    if str(response.status_code) == "200":
        data = response.json()
        honeytoken = "http://canarytokens.org/" + str(data['Token'])
        return honeytoken
    else:
        print("Didn't get a 200 response code...Exiting.")
        exit()

if __name__ == "__main__":
    if len(argv) == 2:
        memo =str(argv[1])
        honeytoken = generate_honeytoken(memo)
        print("\n" + honeytoken + "\n")
    else:
        print("Please provide a memo argument.")
        exit()
