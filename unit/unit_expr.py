from simply.parse_expr import *
import ast 

s = """
x = 1
"""
c = ast.parse(s)
name = c.body[0].targets[0]
print(parse(name))


s = """
True
"""
c = ast.parse(s)
expr = c.body[0].value
print(parse(expr))


s = """
True and False
"""
c = ast.parse(s)
expr = c.body[0].value
print(parse(expr))


s = """
1 + 1
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(parse(expr))


s = """
lambda x: x + 1
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(parse(expr))


s = """
not x
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(parse(expr))

s = """
10 if True else False
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(parse(expr))


s = """
random(10, v=100)
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(parse(expr))


s = """
np.random
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(parse(expr))


s = """
np.random.randn(10)
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(parse(expr))


s = """
x > 10
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(parse(expr))