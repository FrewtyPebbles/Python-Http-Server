from typing import Dict
from Twig.types import ContentType
from Twig.util import utf8len

def read(path:str):
    fl = open(path)
    flc = fl.read()
    fl.close()
    return flc

class Response:

    def __init__(self, ContentType:ContentType = ContentType.html, Content:str = "", headers: Dict[str, str] = {}) -> None:
        self.ContentType = ContentType
        self.Content = Content
        self.headers = headers

    def generate_headers(self) -> str:
        ret_head = ""
        for key, val in self.headers:
            ret_head += f"{key}: {val}\n"
        return ret_head
    
    def generate(self) -> str:
        response_headers = "HTTP/1.1 200 OK\n"
        response_headers += f"Content-Length: {utf8len(self.Content)}\n"
        response_headers += self.ContentType

        return self.generate_headers() + response_headers + "\n" + self.Content

    def __repr__(self) -> str:
        response_headers = "HTTP/1.1 200 OK\n"
        response_headers += f"Content-Length: {utf8len(self.Content)}\n"
        response_headers += self.ContentType
        
        return self.generate_headers() + response_headers + "\n" + self.Content
