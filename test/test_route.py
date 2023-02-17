
import unittest
from src.TwigWeb.backend.routehandler.route import Route, RouteParameter, RouteParamType
from src.TwigWeb.backend import Server
from src.TwigWeb.backend.response import Response

class Router(unittest.TestCase):

    def test_route_eq(self):
        rp1 = RouteParameter()
        rp1.name = "number"
        rp1.type = RouteParamType.integer

        rp2 = RouteParameter()
        rp2.name = "string"
        rp2.type = RouteParamType.string

        route = Route("api/[number]/(string)")
        #print(route.parameters)

        self.assertEqual(route.parameters, ("api", 120, "abc"))
    
    def test_routehandler_static(self):
        
        app = Server("", open_root= False)

        app.set_all_routes({
            "test/static": lambda headers: Response(f"""test"""),
        })

        self.assertEqual(app._handle_route("test/static", {}), b'HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 4\n\ntest')

    def test_routehandler_int_str(self):
        
        app = Server("", open_root= False)

        app.set_all_routes({
            "test/[number]/(name)": lambda headers, params: Response(f"""your number: {params["number"]}\nyour name: {params["name"]}"""),
        })

        self.assertEqual(app._handle_route("test/1/jeff", {}), b'HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 30\n\nyour number: 1\nyour name: jeff')

    def test_routehandler_int_int(self):
        
        app = Server("", open_root= False)

        app.set_all_routes({
            "test/[number]/[number2]": lambda headers, params: Response(f"""{params["number"]}{params["number2"]}""")
        })

        self.assertEqual(app._handle_route("test/5/2", {}), b'HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 2\n\n52')