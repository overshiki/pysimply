from functools import singledispatch
from .abstract import *
from .expr import *
from .extra import *
from .parse_base import *
from .parse_extra import *
from .parse_expr import *
import ast


@parse.register
def _(c: ast.Assign):
    return Assign()