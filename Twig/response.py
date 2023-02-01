

from Twig.util import utf8len


class Response:

    def __init__(self, ContentType:str, Content:str) -> None:
        self.ContentType = ContentType
        self.Content = Content
    
    def generate(self) -> str:
        response_headers = "HTTP/1.1 200 OK\n"
        response_headers += f"Content-Length: {utf8len(self.Content)}\n"
        if  self.ContentType.lower() == "html":
            response_headers += f"Content-Type: text/html\n"
        elif  self.ContentType.lower() == "json":
            response_headers += f"Content-Type: application/json\n"
        elif  self.ContentType.lower() == "css":
            response_headers += f"Content-Type: text/css\n"
        elif  self.ContentType.lower() == "plain":
            response_headers += f"Content-Type: text/plain\n"
        
        return response_headers + "\n" + self.Content
