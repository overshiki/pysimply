from typing import Callable, TypeVar
import inspect
import ast

def ast_of_source(s: str):
    c = ast.parse(s)
    return c

def ast_transformer(c):
    return c

T = TypeVar("T", bound=Callable)
class Trace:
    def trace(self, func: T) -> T:
        lines, lineno = inspect.getsourcelines(func)
        source = inspect.cleandoc("".join(lines)).removeprefix("@trace\n")
        c = ast_of_source(source)
        c = ast_transformer(c)
        return exec(c)