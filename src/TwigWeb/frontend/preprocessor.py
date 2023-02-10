from __future__ import annotations
from typing import Dict, List

class Element:
    def __init__(self, element:str, attributes:Dict[str, str | int | bool], scope:List[Component | Element | str]) -> None:
        self.element = element
        self.attributes = attributes
        self.scope = scope

    def render(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        attr = ""
        for key, val in self.attributes.items():
            attr += f' {key} = "{val}"'
        scope = ""
        for elem in self.scope:
            scope = f"{scope}{elem}"
        return f"<{self.element}{attr}>{scope}</{self.element}>"

class Component:
    def __init__(self, **props) -> None:
        self.props = props
        self.element_cache = ""
    
    def hydrate(self):
        """Class should be inherited and hydrate overwritten."""

    def render(self) -> str:
        return self.hydrate()

    def __repr__(self) -> str:
        return self.render()