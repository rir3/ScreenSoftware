import http.server
from socketserver import TCPServer
from urllib.parse import urlparse, parse_qs
import json
from queue import Queue
import threading
import os

# Define a custom request handler to parse the query parameters
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Define a sample JSON response
        json_response = {
            'message': 'Hello, this is JSON data!',
            'data': [1, 2, 3, 4, 5]
        }

        # Convert the JSON data to a string
        json_str = json.dumps(json_response)

        # Parse the query parameters from the URL
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Access and print specific query parameters
        if 'param1' in query_params:
            param1_value = query_params['param1'][0]
            print(f'param1: {param1_value}')
            statuses.put(param1_value)
            '''if(param1_value == "Quit"):
                print("got here")
                httpd.shutdown()
                httpd.server_close()
                #os._exit(1)'''

        if 'param2' in query_params:
            param2_value = query_params['param2'][0]
            print(f'param2: {param2_value}')

        # Set the response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.end_headers()

        # Send the JSON response
        self.wfile.write(json_str.encode('utf-8'))

def start(httpd, statuse=Queue()):
    global statuses
    statuses = statuse

    '''# Create a socket server with the custom request handler
    with TCPServer(('', 8000), MyHandler) as httpd:
        print('Server started on port 8000...')
        httpd.allow_reuse_address = True
        httpd.serve_forever()
    '''

    print('Server started on port 8000...')
    httpd.serve_forever()

def set_httpd():
    # Create an instance of the custom server
    httpd = TCPServer(('', 8000), MyHandler)
    httpd.allow_reuse_address = True

    return httpd

def start_helper(statuses):
    global server_thread

    httpd =  set_httpd()
    server_thread = threading.Thread(target=start, args=(httpd, statuses,))
    server_thread.start()

    return httpd

def main():
    start(set_httpd())

if __name__ == "__main__":
    main()
