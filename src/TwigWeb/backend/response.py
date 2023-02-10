import codecs
from typing import Dict
from .types import ContentType
from .util import utf8len

def read(path:str):
    fl = open(path)
    flc = fl.read()
    fl.close()
    return flc

class Response:

    def __init__(self, Content:bytes = b"", ContentType:ContentType = ContentType.html, headers: Dict[str, str] = {}) -> None:
        self.ContentType = ContentType
        self.Content = Content
        self.headers = headers

    def generate_headers(self) -> bytes:
        ret_head = b""
        for key, val in self.headers:
            ret_head += f"{key}: {val}\n".encode()
        return ret_head
    
    def generate(self) -> str:
        response_headers:bytes = b"HTTP/1.1 200 OK\n"
        response_headers += self.ContentType
        response_headers += f"Content-Length: {utf8len(self.Content)}\n".encode()
        if type(self.Content) == str:
            self.Content = self.Content.encode()
        return self.generate_headers() + response_headers + b"\n" + self.Content

    def __repr__(self) -> str:
        return self.generate()
