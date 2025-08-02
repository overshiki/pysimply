from .abstract import *
from dataclasses import dataclass
from typing import List, Optional, Any
import ast

@dataclass
class Name(AbsExpr):
    id: AbsIdentifier
    ctx: AbsExprContext

    @property
    def sexp(self):
        return ("Name",
                self.id.sexp,
                self.ctx.sexp)

    @property
    def ast(self):
        return ast.Name(self.id.ast, self.ctx.ast)

@dataclass
class BoolOp(AbsExpr):
    op: AbsBoolOp
    values: List[AbsExpr]

    @property
    def sexp(self):
        return ("BoolOp", 
                self.op.sexp, 
                sexp_of_list(self.values))

    @property
    def ast(self):
        values = ast_of_list(self.values)
        return ast.BoolOp(self.op.ast, values)

@dataclass
class NamedExpr(AbsExpr):
    target: AbsExpr
    value: AbsExpr

    @property
    def sexp(self):
        return ("NamedExpr",
                self.target.sexp,
                self.value.sexp)

    @property
    def ast(self):
        return ast.NamedExpr(self.target.ast, self.value.ast)

@dataclass
class BinOp(AbsExpr):
    left: AbsExpr
    op: AbsOperator
    right: AbsExpr

    @property
    def sexp(self):
        return ("BinOp",
                self.left.sexp,
                self.op.sexp,
                self.right.sexp)

    @property
    def ast(self):
        return ast.BinOp(self.left.ast, self.op.ast, self.right.ast)

@dataclass
class UnaryOp(AbsExpr):
    op: AbsUnaryOp
    operand: AbsExpr

    @property
    def sexp(self):
        return ("UnaryOp",
                self.op.sexp,
                self.operand.sexp)

    @property
    def ast(self):
        return ast.UnaryOp(self.op.ast, self.operand.ast)

@dataclass
class Lambda(AbsExpr):
    args: AbsArguments
    body: AbsExpr

    @property
    def sexp(self):
        return ("Lambda",
                self.args.sexp,
                self.body.sexp)

    @property
    def ast(self):
        return ast.Lambda(self.args.ast, self.body.ast)

@dataclass
class IfExp(AbsExpr):
    test: AbsExpr
    body: AbsExpr
    orelse: AbsExpr

    @property
    def sexp(self):
        return ("IfExp",
                self.test.sexp,
                self.body.sexp,
                self.orelse.sexp)

    @property
    def ast(self):
        return ast.IfExp(self.test.ast, self.body.ast, self.orelse.ast)

@dataclass
class ADict(AbsExpr):
    keys: List[AbsExpr]
    values: List[AbsExpr]

    @property
    def sexp(self):
        return ("Dict",
                sexp_of_list(self.keys),
                sexp_of_list(self.values))

    @property
    def ast(self):
        keys = ast_of_list(self.keys)
        values = ast_of_list(self.values)
        return ast.Dict(keys, values)

@dataclass
class Set(AbsExpr):
    elts: List[AbsExpr]

    @property
    def sexp(self):
        return ("Set", sexp_of_list(self.elts))

    @property
    def ast(self):
        elts = ast_of_list(self.elts)
        return Set(elts)

@dataclass
class ListComp(AbsExpr):
    elt: AbsExpr
    generators: List[AbsComprehension]

    @property
    def sexp(self):
        return ("ListComp",
                self.elt.sexp,
                sexp_of_list(self.generators))

    @property
    def ast(self):
        generators = ast_of_list(self.generators)
        return ast.ListComp(self.elt.ast, generators)

@dataclass
class SetComp(AbsExpr):
    elt: AbsExpr
    generators: List[AbsComprehension]

    @property
    def sexp(self):
        return ("SetComp",
                self.elt.sexp,
                sexp_of_list(self.generators))

    @property
    def ast(self):
        generators = ast_of_list(self.generators)
        return ast.SetComp(self.elt.ast, generators)

@dataclass
class DictComp(AbsExpr):
    key: AbsExpr
    value: AbsExpr
    generators: List[AbsComprehension]

    @property
    def sexp(self):
        return ("DictComp",
                self.key.sexp,
                self.value.sexp,
                sexp_of_list(self.generators))

    @property
    def ast(self):
        generators = ast_of_list(self.generators)
        return ast.DictComp(self.key.ast, self.value.ast, generators)

@dataclass
class GeneratorExp(AbsExpr):
    elt: AbsExpr
    generators: List[AbsComprehension]

    @property
    def sexp(self):
        return ("GeneratorExp",
                self.elt.sexp,
                sexp_of_list(self.generators))

    @property
    def ast(self):
        generators = ast_of_list(self.generators)
        return ast.GeneratorExp(self.elt.ast, generators)

@dataclass
class Await(AbsExpr):
    value: AbsExpr

    @property
    def sexp(self):
        return ("Await", self.value.sexp)

    @property
    def ast(self):
        return ast.Await(self.value.ast)

@dataclass
class Yield(AbsExpr):
    value: Optional[AbsExpr]

    @property
    def sexp(self):
        return ("Yield", sexp_of_optional(self.value))

    @property
    def ast(self):
        return ast.Yield(ast_of_optional(self.value))

@dataclass
class YieldFrom(AbsExpr):
    value: AbsExpr

    @property
    def sexp(self):
        return ("YieldFrom", self.value.sexp)

    @property
    def ast(self):
        return ast.YieldFrom(self.value.ast)

@dataclass
class Compare(AbsExpr):
    left: AbsExpr 
    ops: List[AbsCmpop]
    comparators: List[AbsExpr]

    @property
    def sexp(self):
        return ("Compare",
                self.left.sexp,
                sexp_of_list(self.ops),
                sexp_of_list(self.comparators))

    @property
    def ast(self):
        ops = ast_of_list(self.ops)
        comparators = ast_of_list(self.comparators)
        return ast.Compare(self.left.ast, ops, comparators)

@dataclass
class Call(AbsExpr):
    func: AbsExpr
    args: List[AbsExpr]
    keywords: List[AbsKeyword]

    @property
    def sexp(self):
        return ("Call",
                self.func.sexp,
                sexp_of_list(self.args),
                sexp_of_list(self.keywords))

    @property
    def ast(self):
        args = ast_of_list(self.args)
        keywords = ast_of_list(self.keywords)
        return ast.Call(self.func.ast, args, keywords)

@dataclass
class FormattedValue(AbsExpr):
    value: AbsExpr
    conversion: int 
    format_spec: Optional[AbsExpr]

    @property
    def sexp(self):
        fs = "None" if self.format_spec is None else self.format_spec.sexp
        return ("FormattedValue",
                self.value.sexp,
                self.conversion,
                fs)

    @property
    def ast(self):
        format_spec = ast_of_optional(self.format_spec)
        return ast.FormattedValue(self.value.ast, self.conversion, format_spec)

@dataclass
class JoinedStr(AbsExpr):
    values: List[AbsExpr]

    @property
    def sexp(self):
        return ("JoinedStr", sexp_of_list(self.values))

    @property
    def ast(self):
        values = ast_of_list(self.values)
        return ast.JoinedStr(values)

@dataclass
class Constant(AbsExpr):
    value: Any 
    kind: Optional[str]

    @property
    def sexp(self):
        return ("Constant", self.value, self.kind)

    @property
    def ast(self):
        return ast.Constant(self.value, self.kind)

@dataclass
class Attribute(AbsExpr):
    value: AbsExpr
    attr: AbsIdentifier
    ctx: AbsExprContext

    @property
    def sexp(self):
        return ("Attribute", 
                self.value.sexp,
                self.attr.sexp,
                self.ctx.sexp)

    @property
    def ast(self):
        return ast.Attribute(self.value.ast, self.attr.ast, self.ctx.ast)

@dataclass
class Subscript(AbsExpr):
    value: AbsExpr
    aslice: AbsExpr
    ctx: AbsExprContext

    @property
    def sexp(self):
        return ("Subscript",
                self.value.sexp,
                self.aslice.sexp,
                self.ctx.sexp)

    @property
    def ast(self):
        return ast.Subscript(self.value.ast, self.aslice.ast, self.ctx.ast)

@dataclass
class Starred(AbsExpr):
    value: AbsExpr
    ctx: AbsExprContext

    @property
    def sexp(self):
        return ("Starred",
                self.value.sexp,
                self.ctx.sexp)

    @property
    def ast(self):
        return ast.Starred(self.value.ast, self.ctx.ast)

@dataclass
class AList(AbsExpr):
    elts: List[AbsExpr]
    ctx: AbsExprContext

    @property
    def sexp(self):
        return ("List",
                sexp_of_list(self.elts),
                self.ctx.sexp)

    @property
    def ast(self):
        elts = ast_of_list(self.elts)
        return ast.List(elts, self.ctx.ast)

@dataclass
class ATuple(AbsExpr):
    elts: List[AbsExpr]
    ctx: AbsExprContext

    @property
    def sexp(self):
        return ("Tuple",
                sexp_of_list(self.elts),
                self.ctx.sexp)

    @property
    def ast(self):
        elts = ast_of_list(self.elts)
        return ast.Tuple(elts, self.ctx.ast)

@dataclass
class ASlice(AbsExpr):
    lower: Optional[AbsExpr]
    upper: Optional[AbsExpr]
    step: Optional[AbsExpr]

    @property
    def sexp(self):
        return ("Slice",
                sexp_of_optional(self.lower),
                sexp_of_optional(self.upper),
                sexp_of_optional(self.step))

    @property
    def ast(self):
        lower = ast_of_optional(self.lower)
        upper = ast_of_optional(self.upper)
        step = ast_of_optional(self.step)
        return ast.Slice(lower, upper, step)