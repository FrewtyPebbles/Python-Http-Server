#from .. import Server
from .route import Route, RouteParamType, RouteParameter

def _handle_route(self, reqpath:str, request_headers):
    path = tuple(int(ind) if ind.isdigit() else ind for ind in reqpath.split("?")[0].split("/"))
    route_key = Route("")
    for key in self.routes.keys():
        if key.parameters == path:
            #this is the correct route
            route_key = key
            break

    route_parameters = {}
    for pn, param in enumerate(route_key.parameters):
        if type(param) == RouteParameter:
            if param.type == RouteParamType.integer:
                route_parameters[param.name] = int(path[pn])
            elif param.type == RouteParamType.string:
                route_parameters[param.name] = path[pn]
    
    if route_parameters == {}:
        return self.routes[route_key](request_headers).generate()
    else:
        return self.routes[route_key](request_headers, route_parameters).generate()