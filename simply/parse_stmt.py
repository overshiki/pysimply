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

@parse.register
def _(c: ast.If):
    test = parse(c.test)
    body = list(map(parse, c.body))
    orelse = list(map(parse, c.orelse))
    return If(test, body, orelse)

@parse.register
def _(c: ast.While):
    test = parse(c.test)
    body = list(map(parse, c.body))
    orelse = list(map(parse, c.orelse))
    return While(test, body, orelse)

@parse.register
def _(c: ast.For):
    target = parse(c.target)
    iter = parse(c.iter)
    body = list(map(parse, c.body))
    orelse = list(map(parse, c.orelse))
    return For(target, iter, body, orelse, c.type_comment)

@parse.register
def _(c: ast.Assign):
    targets = list(map(parse, c.targets))
    value = parse(c.value)
    return Assign(targets, value, c.type_comment)

@parse.register
def _(c: ast.Delete):
    targets = list(map(parse, c.targets))
    return Delete(targets)

@parse.register
def _(c: ast.Return):
    return Return(parse(c.value))

@parse.register
def _(c: ast.FunctionDef):
    name = Identifier(c.name)
    args = parse(c.args)
    body = list(map(parse, c.body))
    decorator_list = list(map(parse, c.decorator_list))
    returns = parse(c.returns)
    # type_comment = c.type_comment
    # type_params = list(map(parse, c.type_params))
    return FunctionDef(name, args, body, 
        decorator_list, returns)
