"""
 Implements a simple HTTP/1.0 Server

"""

import os
import threading
import socket
import webbrowser
from typing import Dict

from Twig.util import TermCol, utf8len

class Server:

    def __init__(self, root_directory, SERVER_HOST = '0.0.0.0', SERVER_PORT = 8000, verbose=False) -> None:
        # Define socket host and port
        self.SERVER_HOST = SERVER_HOST
        self.SERVER_PORT = SERVER_PORT
        self.root_directory = root_directory
        self.routes = {}
        self.verbose = verbose

    def route(self, route:str):
        """Decorator that returns the page content."""
        def wrapper(func):
            self.routes[route] = func
            #print(self.routes)
        return wrapper

    def set_route(self, route:str, func):
        """Used to set routes from external file without decorator."""
        self.routes[route] = func

    def run(self):
        self.server_runtime_handler()

    def server_runtime_handler(self):
        # Create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.server_socket.listen(1)
        print(f'{TermCol.OKGREEN}STARTED{TermCol.ENDC} - http://localhost:{self.SERVER_PORT}/')
        webbrowser.open(f"http://localhost:{self.SERVER_PORT}/")
        while True:    
            # Wait for client connections
            client_connection, client_address = self.server_socket.accept()
            # Handle client connection
            threading.Thread(target=lambda: self.client_handler(client_connection, client_address), daemon=True).start()

    def parse_headers(self, raw_headers:str) -> Dict[str, str]:
        headers = {}
        for raw_header in raw_headers:
            if ": " in raw_header:
                h_parts = raw_header.split(": ", 1)
                headers[h_parts[0]] = h_parts[1].strip()
        return headers

    def client_handler(self, client_connection: socket, client_address):
        
        # Get the client request
        request = client_connection.recv(1024).decode()

        # Parse HTTP headers
        headers = request.split('\n')
        main_req_params = headers[0].split()
        filename = main_req_params[1]
        filename = filename[1:]
        request_headers = self.parse_headers(headers[1:])
        
        request_print = request if self.verbose else headers[0]
        print(f'   {TermCol.OKCYAN}REQUEST{TermCol.ENDC} - {TermCol.WARNING}{request_print}{TermCol.ENDC}\n     {TermCol.FAIL}FROM{TermCol.ENDC} {TermCol.OKGREEN}{client_address[0]}{TermCol.ENDC}')
        if self.verbose:
            print(f'{TermCol.OKBLUE}\tREQUESTING PATH{TermCol.ENDC} - {TermCol.UNDERLINE}"{filename}"{TermCol.ENDC}')

        try:
            response = self.routes[filename](request_headers).generate()
        except:
            errfile = open(os.path.join(os.path.dirname(__file__), 'pagenotfound.html'))
            ErrContent = errfile.read()
            errfile.close()
            response = f'HTTP/1.1 404 NOT FOUND\n\n{ErrContent}'
        
        client_connection.sendall(response.encode())
        #print("Request Handled.")

    def exit(self):
        # Close socket
        self.server_socket.close()