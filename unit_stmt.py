from simply.parse_expr import *
import ast

s = """
x = 1
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
# print(parse(c))

s = """
def x(a: int, b: float, c: "Int", d: Ret) -> Ret:
    return x + 1 
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
# print(parse(c))