from .abstract import *
from dataclasses import dataclass
from typing import List, Optional, Any
import ast

# json and sexp are from base class

class Load(AbsExprContext):
    @property
    def ast(self):
        return ast.Load()

class Store(AbsExprContext):
    @property
    def ast(self):
        return ast.Store()

class Del(AbsExprContext):
    @property
    def ast(self):
        return ast.Del()

class And(AbsBoolOp):
    @property
    def ast(self):
        return ast.And()

class Or(AbsBoolOp):
    @property
    def ast(self):
        return ast.Or()

class Add(AbsOperator):
    @property
    def ast(self):
        return ast.Add()

class Sub(AbsOperator):
    @property
    def ast(self):
        return ast.Sub()

class Mult(AbsOperator):
    @property
    def ast(self):
        return ast.Mult()

class MatMult(AbsOperator):
    @property
    def ast(self):
        return ast.MatMult()

class Div(AbsOperator):
    @property
    def ast(self):
        return ast.Div()

class Mod(AbsOperator):
    @property
    def ast(self):
        return ast.Mod()

class Pow(AbsOperator):
    @property
    def ast(self):
        return ast.Pow()

class LShift(AbsOperator):
    @property
    def ast(self):
        return ast.LShift()

class RShift(AbsOperator):
    @property
    def ast(self):
        return ast.RShift()

class BitOr(AbsOperator):
    @property
    def ast(self):
        return ast.BitOr()

class BitXor(AbsOperator):
    @property
    def ast(self):
        return ast.BitXor()

class BitAnd(AbsOperator):
    @property
    def ast(self):
        return ast.BitAnd()

class FloorDiv(AbsOperator):
    @property
    def ast(self):
        return ast.FloorDiv()

class Invert(AbsUnaryOp):
    @property
    def ast(self):
        return ast.Invert()

class Not(AbsUnaryOp):
    @property
    def ast(self):
        return ast.Not()

class UAdd(AbsUnaryOp):
    @property
    def ast(self):
        return ast.UAdd()

class USub(AbsUnaryOp):   
    @property
    def ast(self):
        return ast.USub()

class Eq(AbsCmpop):
    @property
    def ast(self):
        return ast.Eq()

class NotEq(AbsCmpop):
    @property
    def ast(self):
        return ast.NotEq()

class Lt(AbsCmpop):
    @property
    def ast(self):
        return ast.Lt()

class LtE(AbsCmpop):
    @property
    def ast(self):
        return ast.LtE()

class Gt(AbsCmpop):
    @property
    def ast(self):
        return ast.Gt()

class GtE(AbsCmpop):
    @property
    def ast(self):
        return ast.GtE()

class Is(AbsCmpop):
    @property
    def ast(self):
        return ast.Is()

class IsNot(AbsCmpop):
    @property
    def ast(self):
        return ast.IsNot()

class In(AbsCmpop):
    @property
    def ast(self):
        return ast.In()

class NotIn(AbsCmpop):
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
    def json(self):
        return {"Identifier": self.id}

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
    def json(self):
        return {"Arg": {
            "arg": self.arg,
            "annotation": json_of_optional(self.annotation),
            "type_comment": self.type_comment
        }}

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
    def json(self):
        return {"Arguments": json_of_list(self.args)}

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
    def json(self):
        return {"Keywords": {
            "arg": self.arg,
            "value": self.value.json
        }}

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
    def json(self):
        return {"Withitem": {
            "context_expr": self.context_expr.json,
            "optional_vars": json_of_optional(self.optional_vars)
        }}

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

    @property
    def json(self):
        # TODO: finish the pattern node
        return {"MatchCase": {
            "pattern": self.pattern.json,
            "guard": json_of_optional(self.guard),
            "body": json_of_list(self.body)
        }}

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
    def json(self):
        return {"Alias": {
            "name": self.name.json,
            "asname": json_of_optional(self.asname)
        }}

    @property
    def ast(self):
        return ast.alias(self.name.ast, ast_of_optional(self.asname))