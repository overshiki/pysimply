from functools import singledispatch
from .abstract import *
from .expr import *
from .extra import *
import ast

@singledispatch
def parse(c):
    raise ValueError("{} not supported yet".format(type(c)))



