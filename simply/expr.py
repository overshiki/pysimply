from .abstract import *
from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class BoolOp(AbsExpr):
    op: AbsBoolOp
    values: List[AbsExpr]

@dataclass
class NamedExpr(AbsExpr):
    target: AbsExpr
    value: AbsExpr

@dataclass
class BinOp(AbsExpr):
    left: AbsExpr
    op: AbsOperator
    right: AbsExpr

@dataclass
class UnaryOp(AbsExpr):
    op: AbsUnaryOp
    operand: AbsExpr

@dataclass
class Lambda(AbsExpr):
    args: AbsArguments
    body: AbsExpr

@dataclass
class IfExp(AbsExpr):
    test: AbsExpr
    body: AbsExpr
    orelse: AbsExpr

@dataclass
class ADict(AbsExpr):
    keys: List[AbsExpr]
    values: List[AbsExpr]

@dataclass
class Set(AbsExpr):
    elts: List[AbsExpr]

@dataclass
class ListComp(AbsExpr):
    elt: AbsExpr
    generators: List[AbsComprehension]

@dataclass
class SetComp(AbsExpr):
    elt: AbsExpr
    generators: List[AbsComprehension]

@dataclass
class DictComp(AbsExpr):
    key: AbsExpr
    value: AbsExpr
    generators: List[AbsComprehension]

@dataclass
class GeneratorExp(AbsExpr):
    elt: AbsExpr
    generators: List[AbsComprehension]

@dataclass
class Await(AbsExpr):
    value: AbsExpr

@dataclass
class Yield(AbsExpr):
    value: Optional[AbsExpr]

@dataclass
class YieldFrom(AbsExpr):
    value: AbsExpr

@dataclass
class Compare(AbsExpr):
    left: AbsExpr 
    ops: List[AbsCmpop]
    comparators: List[AbsExpr]

@dataclass
class Call(AbsExpr):
    func: AbsExpr
    args: List[AbsExpr]
    keywords: List[AbsKeyword]

@dataclass
class FormattedValue(AbsExpr):
    value: AbsExpr
    conversion: int 
    format_spec: Optional[AbsExpr]

@dataclass
class JoinedStr(AbsExpr):
    values: List[AbsExpr]

@dataclass
class Constant(AbsExpr):
    value: Any 
    kind: Optional[str]

@dataclass
class Attribute(AbsExpr):
    value: AbsExpr
    attr: AbsIdentifier
    ctx: AbsExprContext

@dataclass
class Subscript(AbsExpr):
    value: AbsExpr
    aslice: AbsExpr
    ctx: AbsExprContext

@dataclass
class Starred(AbsExpr):
    value: AbsExpr
    ctx: AbsExprContext

@dataclass
class Name(AbsExpr):
    id: AbsIdentifier
    ctx: AbsExprContext

@dataclass
class AList(AbsExpr):
    elts: List[AbsExpr]
    ctx: AbsExprContext

@dataclass
class ATuple(AbsExpr):
    elts: List[AbsExpr]
    ctx: AbsExprContext

@dataclass
class ASlice(AbsExpr):
    lower: Optional[AbsExpr]
    upper: Optional[AbsExpr]
    step: Optional[AbsExpr]

