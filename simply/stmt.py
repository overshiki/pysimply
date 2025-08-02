from .abstract import *
from dataclasses import dataclass
from typing import List, Optional, Any
import ast

@dataclass
class FunctionDef(AbsStmt):
    name: AbsIdentifier
    args: AbsArguments
    body: List[AbsStmt]
    decorator_list: List[AbsExpr]
    returns: Optional[AbsExpr]
    # type_comment: Optional[str]
    # type_params: List[AbsTypeParam]

    @property
    def sexp(self):
        return ("FunctionDef",
                self.name.sexp,
                self.args.sexp,
                sexp_of_list(self.body),
                sexp_of_list(self.decorator_list),
                sexp_of_optional(self.returns))

    @property
    def ast(self):
        body = ast_of_list(self.body)
        decorator_list = ast_of_list(self.decorator_list)
        returns = ast_of_optional(self.returns)
        return ast.FunctionDef(
                      self.name.ast, 
                      self.args.ast,
                      body, 
                      decorator_list, 
                      returns)


@dataclass
class AsyncFunctionDef(AbsStmt):
    name: AbsIdentifier
    args: AbsArguments
    body: List[AbsStmt]
    decorator_list: List[AbsExpr]
    returns: Optional[AbsExpr]
    # type_comment: Optional[str]
    # type_params: List[AbsTypeParam]

    @property
    def sexp(self):
        return ("AsyncFunctionDef",
                self.name.sexp,
                self.args.sexp,
                sexp_of_list(self.body),
                sexp_of_list(self.decorator_list),
                sexp_of_optional(self.returns))  

    @property
    def ast(self):
        body = ast_of_list(self.body)
        decorator_list = ast_of_list(self.decorator_list)
        returns = ast_of_optional(self.returns)
        return ast.AsyncFunctionDef(
                      self.name.ast, 
                      self.args.ast,
                      body, 
                      decorator_list, 
                      returns)

@dataclass
class ClassDef(AbsStmt):
    name: AbsIdentifier
    bases: List[AbsExpr]
    keywords: List[AbsKeyword]
    body: List[AbsStmt]
    decorator_list: List[AbsExpr]
    type_params: List[AbsTypeParam]

    @property
    def sexp(self):
        return ("ClassDef",
                self.name.sexp,
                sexp_of_list(self.bases),
                sexp_of_list(self.keywords),
                sexp_of_list(self.body),
                sexp_of_list(self.decorator_list),
                sexp_of_list(self.type_params))

    @property
    def ast(self):
        return ast.ClassDef(
            self.name.ast,
            ast_of_list(self.bases),
            ast_of_list(self.keywords),
            ast_of_list(self.body),
            ast_of_list(self.decorator_list),
            ast_of_list(self.type_params))

@dataclass
class Return(AbsStmt):
    value: Optional[AbsExpr]

    @property
    def sexp(self):
        return ("Return",
                sexp_of_optional(self.value))

    @property
    def ast(self):
        return ast.Return(ast_of_optional(self.value))

@dataclass
class Delete(AbsStmt):
    targets: List[AbsExpr]

    @property
    def sexp(self):
        return ("Delete", sexp_of_list(self.targets))

    @property
    def ast(self):
        return ast.Delete(ast_of_list(self.targets))

@dataclass
class Assign(AbsStmt):
    targets: List[AbsExpr]
    value: AbsExpr
    type_comment: Optional[str]

    @property
    def sexp(self):
        return ("Assign", 
                sexp_of_list(self.targets),
                self.value.sexp,
                self.type_comment)

    @property
    def ast(self):
        return ast.Assign(
            ast_of_list(self.targets), 
            self.value.ast, 
            self.type_comment)

@dataclass
class TypeAlias(AbsStmt):
    name: AbsExpr
    type_params: List[AbsTypeParam]
    value: AbsExpr

    @property
    def sexp(self):
        return ("TypeAlias",
                self.name.sexp,
                sexp_of_list(self.type_params),
                self.value.sexp)

    @property
    def ast(self):
        return ast.TypeAlias(
            self.name.ast, 
            ast_of_list(self.type_params), 
            self.value.ast)

@dataclass
class AugAssign(AbsStmt):
    target: AbsExpr 
    op: AbsOperator
    value: AbsExpr 

    @property
    def sexp(self):
        return ("AugAssign",
                self.target.sexp,
                self.op.sexp,
                self.value.sexp)

    @property
    def ast(self):
        return ast.AugAssign(self.target.ast, self.op.ast, self.value.ast)

@dataclass
class AnnAssign(AbsStmt):
    target: AbsExpr 
    annotation: AbsExpr 
    value: Optional[AbsExpr]
    simple: int 

    @property
    def sexp(self):
        return ("AnnAssign",
                self.target.sexp,
                self.annotation.sexp,
                sexp_of_optional(self.value),
                self.simple)

    @property
    def ast(self):
        return ast.AnnAssign(
            self.target.ast, 
            self.annotation.ast, 
            ast_of_optional(self.value), 
            self.simple)

@dataclass
class For(AbsStmt):
    target: AbsExpr
    iter: AbsExpr
    body: List[AbsStmt]
    orelse: List[AbsStmt]
    type_comment: Optional[str]

    @property
    def sexp(self):
        return ("For",
                self.target.sexp,
                self.iter.sexp,
                sexp_of_list(self.body),
                sexp_of_list(self.orelse),
                self.type_comment)

    @property
    def ast(self):
        return ast.For(
            self.target.ast, 
            self.iter.ast, 
            ast_of_list(self.body), 
            ast_of_list(self.orelse), 
            self.type_comment)

@dataclass
class AsyncFor(AbsStmt):
    target: AbsExpr
    iter: AbsExpr
    body: List[AbsStmt]
    orelse: List[AbsStmt]
    type_comment: Optional[str]

    @property
    def sexp(self):
        return ("AsyncFor",
                self.target.sexp,
                self.iter.sexp,
                sexp_of_list(self.body),
                sexp_of_list(self.orelse),
                self.type_comment)

    @property
    def ast(self):
        return ast.AsyncFor(
            self.target.ast, 
            self.iter.ast, 
            ast_of_list(self.body), 
            ast_of_list(self.orelse), 
            self.type_comment)

@dataclass
class While(AbsStmt):
    test: AbsExpr
    body: List[AbsStmt]
    orelse: List[AbsStmt]

    @property
    def sexp(self):
        return ("While",
                self.test.sexp,
                sexp_of_list(self.body),
                sexp_of_list(self.orelse))

    @property
    def ast(self):
        return ast.While(
            self.test.ast, 
            ast_of_list(self.body), 
            ast_of_list(self.orelse))

@dataclass
class If(AbsStmt):
    test: AbsExpr
    body: List[AbsStmt]
    orelse: List[AbsStmt]

    @property
    def sexp(self):
        return ("If",
                self.test.sexp,
                sexp_of_list(self.body),
                sexp_of_list(self.orelse))

    @property
    def ast(self):
        return ast.If(
            self.test.ast, 
            ast_of_list(self.body), 
            ast_of_list(self.orelse))

@dataclass
class With(AbsStmt):
    items: List[AbsWithitem]
    body: List[AbsStmt]
    type_comment: Optional[str]

    @property
    def sexp(self):
        return ("With",
                sexp_of_list(self.items),
                sexp_of_list(self.body),
                self.type_comment)

    @property
    def ast(self):
        return ast.With(
            ast_of_list(self.items), 
            ast_of_list(self.body), 
            self.type_comment)

@dataclass
class AsyncWith(AbsStmt):
    items: List[AbsWithitem]
    body: List[AbsStmt]
    type_comment: Optional[str]

    @property
    def sexp(self):
        return ("AsyncWith",
                sexp_of_list(self.items),
                sexp_of_list(self.body),
                self.type_comment)

    @property
    def ast(self):
        return ast.AsyncWith(
            ast_of_list(self.items), 
            ast_of_list(self.body), 
            self.type_comment)

@dataclass
class Match(AbsStmt):
    subject: AbsExpr
    cases: List[AbsMatchCase]

    @property
    def sexp(self):
        return ("Match",
                self.subject.sexp,
                sexp_of_list(self.cases))

    @property
    def ast(self):
        return ast.Match(
            self.subject.ast, 
            ast_of_list(self.cases))

@dataclass
class Raise(AbsStmt):
    exc: Optional[AbsExpr]
    cause: Optional[AbsExpr]

    @property
    def sexp(self):
        return ("Raise",
                sexp_of_optional(self.exc),
                sexp_of_optional(self.cause))

    @property
    def ast(self):
        return ast.Raise(
            ast_of_optional(self.exc), 
            ast_of_optional(self.cause))

@dataclass
class Try(AbsStmt):
    body: List[AbsStmt]
    handlers: List[AbsExcepthandler]
    orelse: List[AbsStmt]
    finalbody: List[AbsStmt]

    @property
    def sexp(self):
        return ("Try",
                sexp_of_list(self.body),
                sexp_of_list(self.handlers),
                sexp_of_list(self.orelse),
                sexp_of_list(self.finalbody))

    @property
    def ast(self):
        return ast.Try(
            ast_of_list(self.body), 
            ast_of_list(self.handlers), 
            ast_of_list(self.orelse), 
            ast_of_list(self.finalbody))

@dataclass
class TryStar(AbsStmt):
    body: List[AbsStmt]
    handlers: List[AbsExcepthandler]
    orelse: List[AbsStmt]
    finalbody: List[AbsStmt]

    @property
    def sexp(self):
        return ("TryStar",
                sexp_of_list(self.body),
                sexp_of_list(self.handlers),
                sexp_of_list(self.orelse),
                sexp_of_list(self.finalbody))

    @property
    def ast(self):
        return ast.TryStar(
            ast_of_list(self.body), 
            ast_of_list(self.handlers), 
            ast_of_list(self.orelse), 
            ast_of_list(self.finalbody))

@dataclass
class Assert(AbsStmt):
    test: AbsExpr
    msg: Optional[AbsExpr]

    @property
    def sexp(self):
        return ("Assert",
                self.test.sexp,
                sexp_of_optional(self.msg))

    @property
    def ast(self):
        return ast.Assert(
            self.test.ast, 
            ast_of_optional(self.msg))

@dataclass
class Import(AbsStmt):
    names: AbsAlias

    @property
    def sexp(self):
        return ("Import", self.names.sexp)

    @property
    def ast(self):
        return ast.Import(ast_of_list(self.names))

@dataclass
class ImportFrom(AbsStmt):
    module: Optional[AbsIdentifier]
    names: List[AbsAlias]
    level: Optional[int]

    @property
    def sexp(self):
        return ("ImportFrom",
                sexp_of_optional(self.module),
                sexp_of_list(self.names),
                self.level)

    @property
    def ast(self):
        return ast.ImportFrom(
            ast_of_optional(self.module), 
            ast_of_list(self.names), 
            self.level)

@dataclass
class Global(AbsStmt):
    names: List[AbsIdentifier]

    @property
    def sexp(self):
        return ("Global", sexp_of_list(self.names))

    @property
    def ast(self):
        return ast.Global(ast_of_list(self.names))

@dataclass
class Nonlocal(AbsStmt):
    names: List[AbsIdentifier]

    @property
    def sexp(self):
        return ("Global", sexp_of_list(self.names))

    @property
    def ast(self):
        return ast.Nonlocal(ast_of_list(self.names))

@dataclass
class Expr(AbsStmt):
    value: AbsExpr

    @property
    def sexp(self):
        return ("Expr", self.value.sexp)

    @property
    def ast(self):
        return ast.Expr(self.value.ast)

class Pass(AbsStmt):

    @property
    def sexp(self):
        return ("Pass")

    @property
    def ast(self):
        return ast.Pass()

class Break(AbsStmt):

    @property
    def sexp(self):
        return ("Break")

    @property
    def ast(self):
        return ast.Break()

class Continue(AbsStmt):

    @property
    def sexp(self):
        return ("Continue")

    @property
    def ast(self):
        return ast.Continue()