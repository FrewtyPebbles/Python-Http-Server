"""
 Implements a simple HTTP/1.0 Server

"""

import os
import threading
import socket

from Twig.util import utf8len

class Server:

    def __init__(self, root_directory, SERVER_HOST = '0.0.0.0', SERVER_PORT = 8000) -> None:
        # Define socket host and port
        self.SERVER_HOST = SERVER_HOST
        self.SERVER_PORT = SERVER_PORT
        self.root_directory = root_directory
        self.routes = {}

    def route(self, route):
        """Decorator that returns the page content."""
        def wrapper(func):
            self.routes[route] = func
            #print(self.routes)
        return wrapper

    def run(self):
        self.server_runtime_handler()

    def server_runtime_handler(self):
        # Create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.server_socket.listen(1)
        print(f'Twig Server started on port {self.SERVER_PORT}')

        while True:    
            # Wait for client connections
            client_connection, client_address = self.server_socket.accept()
            # Handle client connection
            threading.Thread(target=lambda: self.client_handler(client_connection, client_address), daemon=True).start()

    def client_handler(self, client_connection: socket, client_address):
        
        # Get the client request
        request = client_connection.recv(1024).decode()

        # Parse HTTP headers
        headers = request.split('\n')
        main_req_params = headers[0].split()
        filename = main_req_params[1]
        filename = filename[1:]
        
        is_defined_route = filename in self.routes.keys()

        if not is_defined_route:
            if filename == '':
                filename = 'index'
            
            if "." not in filename:
                filename = f"{filename}.html"
        
        #print(f'REQUESTING PATH : "{filename}"')
        print(' - INCOMING REQUEST\n"""' + request + '"""')
        #Generate response headers
        response_headers = "HTTP/1.1 200 OK\n"

        try:
            if is_defined_route:
                response = self.routes[filename]().generate()
            else:
                fin = open(self.root_directory + filename)
                content = fin.read()
                fin.close()

                if main_req_params[0] == "POST":
                    response_headers += f"Content-Length: {utf8len(content)}\n"
                    if  filename.split(".")[1] == "html":
                        response_headers += f"Content-Type: text/html\n"
                    elif  filename.split(".")[1] == "json":
                        response_headers += f"Content-Type: application/json\n"
                    elif  filename.split(".")[1] == "css":
                        response_headers += f"Content-Type: text/css\n"
                elif main_req_params[0] == "GET":
                    pass

                response_headers += "\n"
                # Send HTTP response
                response = response_headers + content
            #print('Response : """')
            #print(response)
            #print('"""')
        except FileNotFoundError:
            errfile = open(os.path.join(os.path.dirname(__file__), 'pagenotfound.html'))
            ErrContent = errfile.read()
            errfile.close()
            response = f'HTTP/1.1 404 NOT FOUND\n\n{ErrContent}'
        
        client_connection.sendall(response.encode())
        #print("Request Handled.")

    def exit(self):
        # Close socket
        self.server_socket.close()