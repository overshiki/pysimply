from simply.parse_expr import *
from simply.parse_stmt import *
import ast

s = """
def x(a: int, b: float, c: "Int", d: Ret) -> Ret:
    pass 
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
p = parse(c)
print(p)
print(p.sexp)