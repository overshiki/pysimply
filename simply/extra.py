from .abstract import *
from dataclasses import dataclass
from typing import List, Optional, Any

class Load(AbsExprContext):
    pass 
class Store(AbsExprContext):
    pass 
class Del(AbsExprContext):
    pass 

class And(AbsBoolOp):
    pass 
class Or(AbsBoolOp):
    pass 

class Add(AbsOperator):
    pass
class Sub(AbsOperator):
    pass
class Mult(AbsOperator):
    pass
class MatMult(AbsOperator):
    pass
class Div(AbsOperator):
    pass
class Mod(AbsOperator):
    pass
class Pow(AbsOperator):
    pass
class LShift(AbsOperator):
    pass
class RShift(AbsOperator):
    pass
class BitOr(AbsOperator):
    pass
class BitXor(AbsOperator):
    pass
class BitAnd(AbsOperator):
    pass
class FloorDiv(AbsOperator):
    pass

class Invert(AbsUnaryOp):
    pass
class Not(AbsUnaryOp):
    pass
class UAdd(AbsUnaryOp):
    pass
class USub(AbsUnaryOp):   
    pass

class Eq(AbsCmpop):
    pass
class NotEq(AbsCmpop):
    pass
class Lt(AbsCmpop):
    pass
class LtE(AbsCmpop):
    pass
class Gt(AbsCmpop):
    pass
class GtE(AbsCmpop):
    pass
class Is(AbsCmpop):
    pass
class IsNot(AbsCmpop):
    pass
class In(AbsCmpop):
    pass
class NotIn(AbsCmpop):
    pass

class Identifier(AbsIdentifier):
    def __init__(self, s):
        self.id = s

@dataclass
class Arg:
    arg: str

@dataclass
class Arguments(AbsArguments):
    args: List[Arg]

@dataclass
class Keywords(AbsKeyword):
    arg: str 
    value: AbsExpr

@dataclass
class Withitem(AbsWithitem):
    context_expr: AbsExpr
    optional_vars: Optional[AbsExpr]

@dataclass
class MatchCase(AbsMatchCase):
    pattern: AbsPattern
    guard: Optional[AbsExpr]
    body: List[AbsStmt]

@dataclass 
class Alias(AbsAlias):
    name: AbsIdentifier
    asname: Optional[AbsIdentifier]