from functools import singledispatch
from .abstract import *
from .expr import *
from .extra import *
from .parse_base import *
import ast

@parse.register
def _(c: ast.Load):
    print("Load")
    return Load()

@parse.register
def _(c: ast.Store):
    print("Store")
    return Store()

@parse.register
def _(c: ast.Del):
    print("Del")
    return Del()

@parse.register
def _(c: ast.And):
    print("And")
    return And()

@parse.register
def _(c: ast.Or):
    print("Or")
    return Or()

@parse.register
def _(c: ast.Add):
    print("Add")
    return Add()

@parse.register
def _(c: ast.Sub):
    print("Sub")
    return Sub()

@parse.register
def _(c: ast.Mult):
    print("Mult")
    return Mult()

@parse.register
def _(c: ast.MatMult):
    print("MatMult")
    return MatMult()

@parse.register
def _(c: ast.Div):
    print("Div")
    return Div()

@parse.register
def _(c: ast.Mod):
    print("Mod")
    return Mod()

@parse.register
def _(c: ast.Pow):
    print("Pow")
    return Pow()

@parse.register
def _(c: ast.LShift):
    print("LShift")
    return LShift()

@parse.register
def _(c: ast.RShift):
    print("RShift")
    return RShift()

@parse.register
def _(c: ast.BitOr):
    print("BitOr")
    return BitOr()

@parse.register
def _(c: ast.BitXor):
    print("BitXor")
    return BitXor()

@parse.register
def _(c: ast.BitAnd):
    print("BitAnd")
    return BitAnd()

@parse.register
def _(c: ast.FloorDiv):
    print("FloorDiv")
    return FloorDiv()

@parse.register
def _(c: ast.Invert):
    print("Invert")
    return Invert()

@parse.register
def _(c: ast.Not):
    print("Not")
    return Not()

@parse.register
def _(c: ast.UAdd):
    print("UAdd")
    return UAdd()

@parse.register
def _(c: ast.USub):
    print("USub")
    return USub()

@parse.register
def _(c: ast.Eq):
    print("Eq")
    return Eq()

@parse.register
def _(c: ast.NotEq):
    print("NotEq")
    return NotEq()

@parse.register
def _(c: ast.Lt):
    print("Lt")
    return Lt()

@parse.register
def _(c: ast.LtE):
    print("LtE")
    return LtE()

@parse.register
def _(c: ast.Gt):
    print("Gt")
    return Gt()

@parse.register
def _(c: ast.GtE):
    print("GtE")
    return GtE()

@parse.register
def _(c: ast.Is):
    print("Is")
    return Is()

@parse.register
def _(c: ast.IsNot):
    print("IsNot")
    return IsNot()

@parse.register
def _(c: ast.In):
    print("In")
    return In()

@parse.register
def _(c: ast.NotIn):
    print("NotIn")
    return NotIn()


@parse.register
def _(c: ast.arg):
    print("arg")
    return Arg(c.arg)

@parse.register
def _(c: ast.arguments):
    print("arguments")
    args = list(map(parse, c.args))
    return Arguments(args)

@parse.register
def _(c: ast.keyword):
    print("keyword")
    return Keywords(c.arg, parse(c.value))

@parse.register
def _(c: ast.alias):
    print("Alias")
    name = Identifier(c.name)
    if c.asname is None:
        asname = None 
    else:
        asname = Identifier(c.asname)
    return Alias(name, asname)