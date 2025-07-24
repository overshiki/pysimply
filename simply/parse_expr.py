from functools import singledispatch
from .abstract import *
from .expr import *
from .extra import *
from .parse_base import *
from .parse_extra import *
import ast

@parse.register
def _(c: ast.Name):
    print("Name")
    return Name(Identifier(c.id), parse(c.ctx))

@parse.register
def _(c: ast.Constant):
    return Constant(c.value, c.kind)

@parse.register
def _(c: ast.BoolOp):
    values = list(map(parse, c.values))
    return BoolOp(parse(c.op), values)
    
@parse.register
def _(c: ast.BinOp):
    return BinOp(parse(c.left), parse(c.op), parse(c.right))

@parse.register
def _(c: ast.Lambda):
    return Lambda(parse(c.args), parse(c.body))

@parse.register
def _(c: ast.UnaryOp):
    return UnaryOp(parse(c.op), parse(c.operand))

@parse.register
def _(c: ast.IfExp):
    return IfExp(parse(c.test), parse(c.body), parse(c.orelse))

@parse.register
def _(c: ast.Call):
    args = list(map(parse, c.args))
    keywords = list(map(parse, c.keywords))
    return Call(parse(c.func), args, keywords)

@parse.register
def _(c: ast.Attribute):
    return Attribute(parse(c.value), Identifier(c.attr), parse(c.ctx))

@parse.register
def _(c: ast.Compare):
    left = parse(c.left)
    ops = list(map(parse, c.ops))
    comparators = list(map(parse, c.comparators))
    return Compare(left, ops, comparators)