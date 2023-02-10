from __future__ import annotations

"""
routes variables:
    wildcards:
         - `[var_name]` this is for an integer
         - `(var_name)` this is for a string
"""

from enum import Enum
from typing import List, Tuple, Union

class RouteParamType(Enum):
    integer = "int"
    string = "str"
    null = "null"

class RouteParameter:
    def __init__(self) -> None:
        self.name = ""
        self.type = RouteParamType.null

    def __eq__(self, other:Union[str, RouteParameter]) -> bool:
        if type(other) == str:
            return self.type == RouteParamType.string
        if type(other) == int:
            return self.type == RouteParamType.integer
        if type(other) == RouteParameter:
            return other.name == self.name and other.type == self.type
    
    def __hash__(self) -> int:
        return hash((self.name, self.type))
        

class Route:
    def __init__(self, raw:str) -> None:
        self.raw = raw
        # handle raw route and create base and parameters
        self.parameters:Tuple[str | RouteParameter] = ()
        self.dynamic_parameters:Tuple[RouteParameter] = ()
        self._handle_parameters()

    def __eq__(self, other: Tuple[int | str | RouteParameter]) -> bool:
        return self.parameters == other

    def __hash__(self) -> int:
        return hash(self.parameters)

    def _handle_parameters(self):
        current_scope = RouteParamType.null
        current_parameter = RouteParameter()
        param_str_buffer = ""
        base = True
        for chr in self.raw:
            if chr == "[":
                current_scope = RouteParamType.integer
                base = False
            elif chr == "]":
                current_parameter.name = param_str_buffer
                current_parameter.type = RouteParamType.integer
                param_str_buffer = ""
                self.parameters = self.parameters + (current_parameter,)
                self.dynamic_parameters = self.dynamic_parameters + (current_parameter,)
                current_parameter = RouteParameter()
                current_scope = RouteParamType.null
            elif chr == "(":
                current_scope = RouteParamType.string
                base = False
            elif chr == ")":
                current_parameter.name = param_str_buffer
                current_parameter.type = RouteParamType.string
                param_str_buffer = ""
                self.parameters = self.parameters + (current_parameter,)
                self.dynamic_parameters = self.dynamic_parameters + (current_parameter,)
                current_parameter = RouteParameter()
                current_scope = RouteParamType.null
            elif chr == "/":
                if param_str_buffer != "":
                    self.parameters = self.parameters + (param_str_buffer,)
                    param_str_buffer = ""
            else:
                # get param names
                param_str_buffer += chr
        if param_str_buffer != "":
            self.parameters = self.parameters + (param_str_buffer,)