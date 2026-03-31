from typing import Callable, TypeVar
import inspect
import ast
from .parse_base import *
from .parse_expr import *
from .parse_extra import *
from .parse_stmt import *

def ast_of_source(s: str):
    c = ast.parse(s)
    return c

def ast_transformer(c):
    return c

T = TypeVar("T", bound=Callable)

GLOBAL_TRACE = {}

def trace(func: T) -> T:
    lines, lineno = inspect.getsourcelines(func)
    source = inspect.cleandoc("".join(lines)).removeprefix("@trace\n")
    c = ast_of_source(source)
    # c = ast_transformer(c)
    func_name = c.body[0].name
    GLOBAL_TRACE[func_name] = parse(c.body[0]) 
    obj = compile(c, filename="<ast>", mode="exec")
    exec(obj)
    # return locals()[func_name]
    return func
