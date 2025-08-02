from .abstract import *
from dataclasses import dataclass
from typing import List, Optional, Any
import ast

class Load(AbsExprContext):
    @property
    def sexp(self):
        return ("Load")

    @property
    def ast(self):
        return ast.Load()

class Store(AbsExprContext):
    @property
    def sexp(self):
        return ("Store")

    @property
    def ast(self):
        return ast.Store()

class Del(AbsExprContext):
    @property
    def sexp(self):
        return ("Del")

    @property
    def ast(self):
        return ast.Del()

class And(AbsBoolOp):
    @property
    def sexp(self):
        return ("And")

    @property
    def ast(self):
        return ast.And()

class Or(AbsBoolOp):
    @property
    def sexp(self):
        return ("Or")

    @property
    def ast(self):
        return ast.Or()

class Add(AbsOperator):
    @property
    def sexp(self):
        return ("Add")

    @property
    def ast(self):
        return ast.Add()

class Sub(AbsOperator):
    @property
    def sexp(self):
        return ("Sub")

    @property
    def ast(self):
        return ast.Sub()

class Mult(AbsOperator):
    @property
    def sexp(self):
        return ("Mult")

    @property
    def ast(self):
        return ast.Mult()

class MatMult(AbsOperator):
    @property
    def sexp(self):
        return ("MatMult")

    @property
    def ast(self):
        return ast.MatMult()

class Div(AbsOperator):
    @property
    def sexp(self):
        return ("Div")

    @property
    def ast(self):
        return ast.Div()

class Mod(AbsOperator):
    @property
    def sexp(self):
        return ("Mod")

    @property
    def ast(self):
        return ast.Mod()

class Pow(AbsOperator):
    @property
    def sexp(self):
        return ("Pow")

    @property
    def ast(self):
        return ast.Pow()

class LShift(AbsOperator):
    @property
    def sexp(self):
        return ("LShift")

    @property
    def ast(self):
        return ast.LShift()

class RShift(AbsOperator):
    @property
    def sexp(self):
        return ("RShift")

    @property
    def ast(self):
        return ast.RShift()

class BitOr(AbsOperator):
    @property
    def sexp(self):
        return ("BitOr")

    @property
    def ast(self):
        return ast.BitOr()

class BitXor(AbsOperator):
    @property
    def sexp(self):
        return ("BitXor")

    @property
    def ast(self):
        return ast.BitXor()

class BitAnd(AbsOperator):
    @property
    def sexp(self):
        return ("BitAnd")

    @property
    def ast(self):
        return ast.BitAnd()

class FloorDiv(AbsOperator):
    @property
    def sexp(self):
        return ("FloorDiv")

    @property
    def ast(self):
        return ast.FloorDiv()

class Invert(AbsUnaryOp):
    @property
    def sexp(self):
        return ("Invert")

    @property
    def ast(self):
        return ast.Invert()

class Not(AbsUnaryOp):
    @property
    def sexp(self):
        return ("Not")

    @property
    def ast(self):
        return ast.Not()

class UAdd(AbsUnaryOp):
    @property
    def sexp(self):
        return ("UAdd")

    @property
    def ast(self):
        return ast.UAdd()

class USub(AbsUnaryOp):   
    @property
    def sexp(self):
        return ("USub")

    @property
    def ast(self):
        return ast.USub()

class Eq(AbsCmpop):
    @property
    def sexp(self):
        return ("Eq")

    @property
    def ast(self):
        return ast.Eq()

class NotEq(AbsCmpop):
    @property
    def sexp(self):
        return ("NotEq")

    @property
    def ast(self):
        return ast.NotEq()

class Lt(AbsCmpop):
    @property
    def sexp(self):
        return ("Lt")

    @property
    def ast(self):
        return ast.Lt()

class LtE(AbsCmpop):
    @property
    def sexp(self):
        return ("LtE")

    @property
    def ast(self):
        return ast.LtE()

class Gt(AbsCmpop):
    @property
    def sexp(self):
        return ("Gt")

    @property
    def ast(self):
        return ast.Gt()

class GtE(AbsCmpop):
    @property
    def sexp(self):
        return ("GtE")

    @property
    def ast(self):
        return ast.GtE()

class Is(AbsCmpop):
    @property
    def sexp(self):
        return ("Is")

    @property
    def ast(self):
        return ast.Is()

class IsNot(AbsCmpop):
    @property
    def sexp(self):
        return ("IsNot")

    @property
    def ast(self):
        return ast.IsNot()

class In(AbsCmpop):
    @property
    def sexp(self):
        return ("In")

    @property
    def ast(self):
        return ast.In()

class NotIn(AbsCmpop):
    @property
    def sexp(self):
        return ("NotIn")

    @property
    def ast(self):
        return ast.NotIn()

class Identifier(AbsIdentifier):
    def __init__(self, s):
        self.id = s

    @property
    def sexp(self):
        return ("Identifier", self.id)

    @property
    def ast(self):
        return self.id

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

    @property
    def ast(self):
        return ast.arg(
            self.arg.ast, 
            ast_of_optional(self.annotation), 
            self.type_comment)

@dataclass
class Arguments(AbsArguments):
    args: List[Arg]

    @property
    def sexp(self):
        return ("Arguments", sexp_of_list(self.args))

    @property
    def ast(self):
        # TODO, support all parameters in ast.arguments
        return ast.arguments(
            [], 
            ast_of_list(self.args), 
            None, 
            [],
            [], 
            None, 
            [])

@dataclass
class Keywords(AbsKeyword):
    arg: str 
    value: AbsExpr

    @property
    def sexp(self):
        return ("Keywords", self.arg, self.value.sexp)

    @property
    def ast(self):
        # TODO, the type-signature of Keywords does not exactly match that of ast.keyword, double check this
        return ast.keyword(
            self.arg,
            self.value.ast)

@dataclass
class Withitem(AbsWithitem):
    context_expr: AbsExpr
    optional_vars: Optional[AbsExpr]

    @property
    def sexp(self):
        return ("Withitem", 
                self.context_expr.sexp, 
                sexp_of_optional(self.optional_vars))

    @property
    def ast(self):
        return ast.withitem(
            self.context_expr.ast, 
            ast_of_optional(self.optional_vars))

@dataclass
class MatchCase(AbsMatchCase):
    pattern: AbsPattern
    guard: Optional[AbsExpr]
    body: List[AbsStmt]

    @property
    def sexp(self):
        return ("MatchCase", 
                # TODO: finish the pattern node
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

    @property
    def ast(self):
        return ast.alias(self.name.ast, ast_of_optional(self.asname))