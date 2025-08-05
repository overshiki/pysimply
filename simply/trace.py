from typing import Callable, TypeVar
import inspect
import ast

def ast_of_source(s: str):
    c = ast.parse(s)
    return c

def ast_transformer(c):
    return c

T = TypeVar("T", bound=Callable)

def trace(func: T) -> T:
    lines, lineno = inspect.getsourcelines(func)
    source = inspect.cleandoc("".join(lines)).removeprefix("@trace\n")
    c = ast_of_source(source)
    c = ast_transformer(c)
    func_name = c.body[0].name
    obj = compile(c, filename="<ast>", mode="exec")
    exec(obj)
    return locals()[func_name]
