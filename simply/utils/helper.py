import ast

s = """
def a(x: int, y: float, z: Cont, i: "II") -> Ret:
    return x
"""
c = ast.parse(s)
print(ast.dump(c))
print("\n")

# Module(body=[FunctionDef(name='a', args=arguments(posonlyargs=[], args=[arg(arg='x', annotation=Name(id='int', ctx=Load())), arg(arg='y', annotation=Name(id='float', ctx=Load())), arg(arg='z', annotation=Name(id='Cont', ctx=Load())), arg(arg='i', annotation=Constant(value='II'))], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Return(value=Name(id='x', ctx=Load()))], decorator_list=[], returns=Name(id='Ret', ctx=Load()))], type_ignores=[])


s = """
x = 1
"""
c = ast.parse(s)
print(ast.dump(c))
name = c.body[0].targets[0]
print(ast.dump(name))
print("\n")
assign = c.body[0]
print(ast.dump(assign))
print("\n")


s = """
True and False
"""
c = ast.parse(s)
print(ast.dump(c))
# Module(body=[Expr(value=BoolOp(op=And(), values=[Constant(value=True), Constant(value=False)]))], type_ignores=[])
bop = c.body[0].value
print(ast.dump(bop))
print("\n")


s = """
True
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(ast.dump(expr))
print("\n")


s = """
1 + 1
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(ast.dump(expr))
print("\n")


s = """
lambda x: x + 1
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(ast.dump(expr))
print("\n")


s = """
not x
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(ast.dump(expr))
print("\n")

s = """
10 if True else False
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(ast.dump(expr))
print("\n")


s = """
random(10, v=100)
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(ast.dump(expr))
print("\n")


s = """
np.random
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(ast.dump(expr))
print("\n")


s = """
np.random.randn(10)
"""
c = ast.parse(s)
print(ast.dump(c))
expr = c.body[0].value
print(ast.dump(expr))
print("\n")