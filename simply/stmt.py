from .abstract import *
from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class FunctionDef(AbsStmt):
    name: AbsIdentifier
    args: Arguments
    body: List[AbsStmt]
    decorator_list: List[AbsExpr]
    returns: Optional[AbsExpr]
    type_comment: Optional[str]
    type_params: List[AbsTypeParam]


@dataclass
class AsyncFunctionDef(AbsStmt):
    name: AbsIdentifier
    args: Arguments
    body: List[AbsStmt]
    decorator_list: List[AbsExpr]
    returns: Optional[AbsExpr]
    type_comment: Optional[str]
    type_params: List[AbsTypeParam]

@dataclass
class ClassDef(AbsStmt):
    name: AbsIdentifier
    bases: List[AbsExpr]
    keywords: List[AbsKeyword]
    body: List[AbsStmt]
    decorator_list: List[AbsExpr]
    type_params: List[AbsTypeParam]

@dataclass
class Return(AbsStmt):
    value: Optional[AbsExpr]

@dataclass
class Delete(AbsStmt):
    targets: List[AbsExpr]

@dataclass
class Assign(AbsStmt):
    targets: List[AbsExpr]
    value: AbsExpr
    type_comment: Optional[str]

@dataclass
class TypeAlias(AbsStmt):
    name: AbsExpr
    type_params: List[AbsTypeParam]
    value: AbsExpr

@dataclass
class AugAssign(AbsStmt):
    target: AbsExpr 
    op: AbsOperator
    value: AbsExpr 

@dataclass
class AnnAssign(AbsStmt):
    target: AbsExpr 
    annotation: AbsExpr 
    value: Optional[AbsExpr]
    simple: int 

@dataclass
class For(AbsStmt):
    target: AbsExpr
    iter: AbsExpr
    body: List[AbsStmt]
    orelse: List[AbsStmt]
    type_comment: Optional[str]

@dataclass
class AsyncFor(AbsStmt):
    target: AbsExpr
    iter: AbsExpr
    body: List[AbsStmt]
    orelse: List[AbsStmt]
    type_comment: Optional[str]

@dataclass
class While(AbsStmt):
    test: AbsExpr
    body: List[AbsStmt]
    orelse: List[AbsStmt]

@dataclass
class If(AbsStmt):
    test: AbsExpr
    body: List[AbsStmt]
    orelse: List[AbsStmt]

@dataclass
class With(AbsStmt):
    items: List[AbsWithitem]
    body: List[AbsStmt]
    type_comment: Optional[str]

@dataclass
class AsyncWith(AbsStmt):
    items: List[AbsWithitem]
    body: List[AbsStmt]
    type_comment: Optional[str]

@dataclass
class Match(AbsStmt):
    subject: AbsExpr
    cases: List[AbsMatchCase]

@dataclass
class Raise(AbsStmt):
    exc: Optional[AbsExpr]
    cause: Optional[AbsExpr]

@dataclass
class Try(AbsStmt):
    body: List[AbsStmt]
    handlers: List[AbsExcepthandler]
    orelse: List[AbsStmt]
    finalbody: List[AbsStmt]

@dataclass
class TryStar(AbsStmt):
    body: List[AbsStmt]
    handlers: List[AbsExcepthandler]
    orelse: List[AbsStmt]
    finalbody: List[AbsStmt]

@dataclass
class Assert(AbsStmt):
    test: AbsExpr
    msg: Optional[AbsExpr]

@dataclass
class Import(AbsStmt):
    names: AbsAlias

@dataclass
class ImportFrom(AbsStmt):
    module: Optional[AbsIdentifier]
    names: List[AbsAlias]
    level: Optional[int]

@dataclass
class Global(AbsStmt):
    names: List[AbsIdentifier]

@dataclass
class Nonlocal(AbsStmt):
    names: List[AbsIdentifier]

@dataclass
class Expr(AbsStmt):
    value: AbsExpr

class Pass(AbsStmt):
    pass 

class Break(AbsStmt):
    pass 

class Continue(AbsStmt):
    pass 