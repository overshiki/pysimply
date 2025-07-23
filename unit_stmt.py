from simply.parse_expr import *
from simply.parse_stmt import *
import ast

s = """
continue
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
print(parse(c))

s = """
break
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
print(parse(c))

s = """
pass
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
print(parse(c))

s = """
a
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
print(parse(c))

s = """
from numpy import abs
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
print(parse(c))

s = """
from numpy import abs as nabs
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
print(parse(c))

s = """
import numpy as np
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
print(parse(c))

s = """
assert x
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
print(parse(c))


s = """
raise ValueError()
"""
c = ast.parse(s).body[0]
print(ast.dump(c))
print(parse(c))

# s = """
# x = 1
# """
# c = ast.parse(s).body[0]
# print(ast.dump(c))
# # print(parse(c))

# s = """
# def x(a: int, b: float, c: "Int", d: Ret) -> Ret:
#     return x + 1 
# """
# c = ast.parse(s).body[0]
# print(ast.dump(c))
# # print(parse(c))