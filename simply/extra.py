from .abstract import *
from dataclasses import dataclass
from typing import List, Optional, Any

class Load(AbsExprContext):
    @property
    def sexp(self):
        return ("Load")

class Store(AbsExprContext):
    @property
    def sexp(self):
        return ("Store")

class Del(AbsExprContext):
    @property
    def sexp(self):
        return ("Del")

class And(AbsBoolOp):
    @property
    def sexp(self):
        return ("And")

class Or(AbsBoolOp):
    @property
    def sexp(self):
        return ("Or")

class Add(AbsOperator):
    @property
    def sexp(self):
        return ("Add")

class Sub(AbsOperator):
    @property
    def sexp(self):
        return ("Sub")

class Mult(AbsOperator):
    @property
    def sexp(self):
        return ("Mult")

class MatMult(AbsOperator):
    @property
    def sexp(self):
        return ("MatMult")

class Div(AbsOperator):
    @property
    def sexp(self):
        return ("Div")

class Mod(AbsOperator):
    @property
    def sexp(self):
        return ("Mod")

class Pow(AbsOperator):
    @property
    def sexp(self):
        return ("Pow")

class LShift(AbsOperator):
    @property
    def sexp(self):
        return ("LShift")

class RShift(AbsOperator):
    @property
    def sexp(self):
        return ("RShift")

class BitOr(AbsOperator):
    @property
    def sexp(self):
        return ("BitOr")

class BitXor(AbsOperator):
    @property
    def sexp(self):
        return ("BitXor")

class BitAnd(AbsOperator):
    @property
    def sexp(self):
        return ("BitAnd")

class FloorDiv(AbsOperator):
    @property
    def sexp(self):
        return ("FloorDiv")

class Invert(AbsUnaryOp):
    @property
    def sexp(self):
        return ("Invert")

class Not(AbsUnaryOp):
    @property
    def sexp(self):
        return ("Not")

class UAdd(AbsUnaryOp):
    @property
    def sexp(self):
        return ("UAdd")

class USub(AbsUnaryOp):   
    @property
    def sexp(self):
        return ("USub")

class Eq(AbsCmpop):
    @property
    def sexp(self):
        return ("Eq")

class NotEq(AbsCmpop):
    @property
    def sexp(self):
        return ("NotEq")

class Lt(AbsCmpop):
    @property
    def sexp(self):
        return ("Lt")

class LtE(AbsCmpop):
    @property
    def sexp(self):
        return ("LtE")

class Gt(AbsCmpop):
    @property
    def sexp(self):
        return ("Gt")

class GtE(AbsCmpop):
    @property
    def sexp(self):
        return ("GtE")

class Is(AbsCmpop):
    @property
    def sexp(self):
        return ("Is")

class IsNot(AbsCmpop):
    @property
    def sexp(self):
        return ("IsNot")

class In(AbsCmpop):
    @property
    def sexp(self):
        return ("In")

class NotIn(AbsCmpop):
    @property
    def sexp(self):
        return ("NotIn")

class Identifier(AbsIdentifier):
    def __init__(self, s):
        self.id = s

    @property
    def sexp(self):
        return ("Identifier", self.id)

@dataclass
class Arg:
    arg: str
    annotation: Optional[AbsExpr]
    type_comment: Optional[str]

    @property
    def sexp(self):
        return ("Arg", 
                self.arg,
                sexp_of_optional(self.annotation),
                self.type_comment)

@dataclass
class Arguments(AbsArguments):
    args: List[Arg]

    @property
    def sexp(self):
        return ("Arguments", sexp_of_list(self.args))

@dataclass
class Keywords(AbsKeyword):
    arg: str 
    value: AbsExpr

    @property
    def sexp(self):
        return ("Keywords", self.arg, self.value.sexp)

@dataclass
class Withitem(AbsWithitem):
    context_expr: AbsExpr
    optional_vars: Optional[AbsExpr]

    @property
    def sexp(self):
        return ("Withitem", 
                self.context_expr.sexp, 
                sexp_of_optional(self.optional_vars))

@dataclass
class MatchCase(AbsMatchCase):
    pattern: AbsPattern
    guard: Optional[AbsExpr]
    body: List[AbsStmt]

    @property
    def sexp(self):
        return ("MatchCase", 
                self.pattern.sexp,
                sexp_of_optional(self.guard),
                sexp_of_list(self.body))

@dataclass 
class Alias(AbsAlias):
    name: AbsIdentifier
    asname: Optional[AbsIdentifier]

    @property
    def sexp(self):
        return ("Alias", 
                self.name.sexp,
                sexp_of_optional(self.asname))