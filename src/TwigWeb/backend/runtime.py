"""
 Twig socket server implementation

"""

import os
from pathlib import Path
import threading
import socket
import webbrowser
from typing import Callable, Dict, Set, Union

from .routehandler.route import Route
from .types import ContentType, ext_content_type

from .util import TermCol, utf8len
from . import response as res

VERSION = "0.4.12"

class Server:

    def __init__(self, root_directory,
                    SERVER_HOST = '0.0.0.0',
                    SERVER_PORT = 8000,
                    verbose=False,
                    open_root=True,
                    debug=False,
                    error_page_path = ""
                ) -> None:
        # Define socket host and port
        self.SERVER_HOST = SERVER_HOST
        self.SERVER_PORT = SERVER_PORT
        self.root_directory = root_directory
        self.routes:Dict[Route, Union[Callable[[Dict[str, str], Dict[str, Union[int, str]]], res.Response], Callable[[Dict[str, str]], res.Response]]] = {}
        self.verbose = verbose
        self.open_root = open_root
        self.debug = debug
        self.static_resources:Set[str] = set()
        self.static_folders:Set[Path] = set()
        self.error_page_path = error_page_path

    from .routehandler.router import _handle_route

    def set_static(self, static_resources:Set[str]):
        self.static_resources = static_resources

    def set_static_folders(self, static_folders:Set[Path]):
        self.static_folders = static_folders

    def add_static(self, static_resource:str):
        self.static_resources.add(static_resource)

    def add_static_folder(self, static_folder:Path):
        self.static_folders.add(static_folder)

    def route(self, route:str):
        """Decorator that sets a route to the decorated function."""
        def wrapper(func):
            self.routes[Route(route)] = func
            #print(self.routes)
        return wrapper

    def set_route(self, route:str, func):
        """Used to set routes from external file without decorator."""
        self.routes[Route(route)] = func

    def set_all_routes(self, routes:Dict[str, Union[Callable[[Dict[str, str], Dict[str, Union[int, str]]], res.Response], Callable[[Dict[str, str]], res.Response]]]):
        """Used to set all routes from external file without decorator."""
        for key, val in routes.items():
            self.routes[Route(key)] = val
        

    def run(self):
        """Runs the server."""
        self.server_runtime_handler()

    def server_runtime_handler(self):
        # Create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.server_socket.listen(1)
        if self.verbose:
            print(f"Twig Server Version: {VERSION}")
        print(f'{TermCol.OKGREEN}STARTED{TermCol.ENDC} - http://localhost:{self.SERVER_PORT}/')
        if self.open_root:
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
        try:
            # Parse HTTP headers
            headers = request.split('\n')
            main_req_params = headers[0].split()
            reqpath = main_req_params[1]
            reqpath = reqpath[1:]
            request_headers = self.parse_headers(headers[1:])
            
            request_print = request if self.verbose else headers[0]
            print(f'   {TermCol.OKCYAN}REQUEST{TermCol.ENDC} - {TermCol.WARNING}{request_print}{TermCol.ENDC}\n     {TermCol.FAIL}FROM{TermCol.ENDC} {TermCol.OKGREEN}{client_address[0]}{TermCol.ENDC}')
            print(f'     {TermCol.FAIL}PATH{TermCol.ENDC} {TermCol.OKGREEN}"/{reqpath}"{TermCol.ENDC}')
            
            response = ""
            if reqpath in self.static_resources or all(
                os.path.abspath(reqpath).startswith(os.path.abspath(s_p)+os.sep) 
                for s_p in self.static_folders
                ) if len(self.static_folders) != 0 else False:
                fl = open(reqpath, "rb")
                flContent = fl.read()
                fl.close()
                extension:str = reqpath.split(".")[1]

                response = res.Response(flContent, ext_content_type(extension)).generate()
            else:
                response = self._handle_route(reqpath, request_headers)
        except FileNotFoundError as e:
            if self.debug:
                print(e)
            errfile = ""
            if self.error_page_path != "":
                errfile = open(self.error_page_path)
            else:
                errfile = open(os.path.join(os.path.dirname(__file__), '404.html'))
            ErrContent = errfile.read()
            errfile.close()
            response = f'HTTP/1.1 404 NOT FOUND\n\n{ErrContent}'.encode()
        
        except KeyError as e:
            if self.debug:
                print(f" ERROR - The requested page or file route \"{reqpath}\" does not exist/is not defined.\n\nExisting Static Paths:\n{self.static_resources}\n\nExisting Static Folders:\n{self.static_folders}\n\nIf this is a static resource for your site (such as .png, .css, etc.), please use the add_static member function to add it to the static files you wish to serve.  If you wish to add all resources within a folder as static resources, please use the add_static_folder function.")
                print(e)
            errfile = ""
            if self.error_page_path != "":
                errfile = open(self.error_page_path)
            else:
                errfile = open(os.path.join(os.path.dirname(__file__), '404.html'))
            ErrContent = errfile.read()
            errfile.close()
            response = f'HTTP/1.1 404 NOT FOUND\n\n{ErrContent}'.encode()
        
        client_connection.sendall(response)
        
        #finish the request
        client_connection.close()

    def exit(self):
        # Close socket
        self.server_socket.close()