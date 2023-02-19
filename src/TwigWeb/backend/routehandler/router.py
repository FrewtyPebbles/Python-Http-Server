#from .. import Server
from .route import Route, RouteParamType, RouteParameter
from ..headers import Headers


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import Server
else:
    Server = any

def _handle_route(self:Server, reqpath:str, request_headers:Headers):
    path = tuple(int(ind) if ind.isdigit() else ind for ind in reqpath.split("?")[0].split("/"))
    route_key = Route("")
    fail = True
    for key in self.routes.keys():
        if key.parameters == path:
            #this is the correct route
            route_key = key
            fail = False
            break
    
    if fail:
        return self.error_404(reqpath)


    route_parameters = {}
    for pn, param in enumerate(route_key.parameters):
        if type(param) == RouteParameter:
            if param.type == RouteParamType.integer:
                route_parameters[param.name] = int(path[pn])
            elif param.type == RouteParamType.string:
                route_parameters[param.name] = path[pn]
    try:
        if route_parameters == {}:
            return self.routes[route_key](request_headers).generate()
        else:
            return self.routes[route_key](request_headers, **route_parameters).generate()
    except TypeError as e:
        if self.debug:
            print(f"An error has occured when trying to access route ({reqpath})\n\nPerhapse you have the wrong (number of) arguments for this route.\n\nFULL ERROR:\n")
            print(e)
        return self.error_404(reqpath)
    except Exception as e:
        if self.debug:
            print("FULL ERROR:\n")
            print(e)
        else:
            print(e)
        return self.error_404(reqpath)