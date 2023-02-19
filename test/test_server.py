import unittest
from src.TwigWeb.backend.headers import Headers
from src.TwigWeb.backend import Server, ContentType
from src.TwigWeb.backend.response import Response

class ServerTest(unittest.TestCase):
    def test_server(self):
        app = Server("", debug=True, open_root=False)

        @app.route("")
        def index(headers:Headers):
            #this is the index of the app
            return Response("test", ContentType.html)

        @app.route("form")
        def form(headers:Headers):
            #this form redirects to page/2
            return Response("""<form action="/page/2">
  <label for="fname">First name:</label><br>
  <input type="text" id="fname" name="fname" value="John"><br>
  <label for="lname">Last name:</label><br>
  <input type="text" id="lname" name="lname" value="Doe"><br><br>
  <input type="submit" value="Submit">
</form>""")

        @app.route("page/[num]")
        def index(headers:Headers, num):
            # Headers.URL is a dictionary containing all url query parameters/variables.
            # num a dynamic route.
            return Response(f"num: {num} and {headers.URL}", ContentType.html)
        
        @app.route("page")
        def index(headers:Headers):
            return Response(f"page", ContentType.html)
        
        app.run()