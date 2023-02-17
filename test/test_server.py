import unittest
from src.TwigWeb.backend import Server, ContentType
from src.TwigWeb.backend.response import Response

class ServerTest(unittest.TestCase):
    def test_server(self):
        app = Server("", debug=True)

        @app.route("")
        def index(headers):
            return Response("test", ContentType.html)
        
        app.run()