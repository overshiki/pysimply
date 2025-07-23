from functools import singledispatch
from .abstract import *
from .expr import *
from .extra import *
from .stmt import *
from .parse_base import *
from .parse_extra import *
from .parse_expr import *
import ast


@parse.register
def _(c: ast.Continue):
    return Continue()

@parse.register
def _(c: ast.Break):
    return Break()

@parse.register
def _(c: ast.Pass):
    return Pass()

@parse.register
def _(c: ast.Expr):
    return Expr(parse(c.value))

@parse.register
def _(c: ast.ImportFrom):
    if c.module is not None:
        module = Identifier(c.module)
    else:
        module = None 
    names = list(map(parse, c.names))
    return ImportFrom(module, names, c.level)

@parse.register
def _(c: ast.Import):
    names = list(map(parse, c.names))
    return Import(names)

@parse.register
def _(c: ast.Assert):
    test = parse(c.test)
    msg = parse(c.msg)
    # if c.msg is None:
    #     msg = None 
    # else:
    #     msg = parse(c.msg)
    return Assert(test, msg)

@parse.register
def _(c: ast.Raise):
    exc = parse(c.exc)
    cause = parse(c.cause)
    return Raise(exc, cause)