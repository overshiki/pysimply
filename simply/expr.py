from .abstract import *
from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class BoolOp(AbsExpr):
    op: AbsBoolOp
    values: List[AbsExpr]

    @property
    def sexp(self):
        return ("BoolOp", 
                self.op.sexp, 
                sexp_of_list(self.values))

@dataclass
class NamedExpr(AbsExpr):
    target: AbsExpr
    value: AbsExpr

    @property
    def sexp(self):
        return ("NamedExpr",
                self.target.sexp,
                self.value.sexp)

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

@dataclass
class UnaryOp(AbsExpr):
    op: AbsUnaryOp
    operand: AbsExpr

    @property
    def sexp(self):
        return ("UnaryOp",
                self.op.sexp,
                self.operand.sexp)


@dataclass
class Lambda(AbsExpr):
    args: AbsArguments
    body: AbsExpr

    @property
    def sexp(self):
        return ("Lambda",
                self.args.sexp,
                self.body.sexp)

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

@dataclass
class ADict(AbsExpr):
    keys: List[AbsExpr]
    values: List[AbsExpr]

    @property
    def sexp(self):
        return ("Dict",
                sexp_of_list(self.keys),
                sexp_of_list(self.values))

@dataclass
class Set(AbsExpr):
    elts: List[AbsExpr]

    @property
    def sexp(self):
        return ("Set", sexp_of_list(self.elts))

@dataclass
class ListComp(AbsExpr):
    elt: AbsExpr
    generators: List[AbsComprehension]

    @property
    def sexp(self):
        return ("ListComp",
                self.elt.sexp,
                sexp_of_list(self.generators))

@dataclass
class SetComp(AbsExpr):
    elt: AbsExpr
    generators: List[AbsComprehension]

    @property
    def sexp(self):
        return ("SetComp",
                self.elt.sexp,
                sexp_of_list(self.generators))

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

@dataclass
class GeneratorExp(AbsExpr):
    elt: AbsExpr
    generators: List[AbsComprehension]

    @property
    def sexp(self):
        return ("GeneratorExp",
                self.elt.sexp,
                sexp_of_list(self.generators))

@dataclass
class Await(AbsExpr):
    value: AbsExpr

    @property
    def sexp(self):
        return ("Await", self.value.sexp)

@dataclass
class Yield(AbsExpr):
    value: Optional[AbsExpr]

    @property
    def sexp(self):
        return ("Yield", sexp_of_optional(self.value))

@dataclass
class YieldFrom(AbsExpr):
    value: AbsExpr

    @property
    def sexp(self):
        return ("YieldFrom", self.value.sexp)

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

@dataclass
class JoinedStr(AbsExpr):
    values: List[AbsExpr]

    @property
    def sexp(self):
        return ("JoinedStr", sexp_of_list(self.values))

@dataclass
class Constant(AbsExpr):
    value: Any 
    kind: Optional[str]

    @property
    def sexp(self):
        return ("Constant", self.value, self.kind)

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

@dataclass
class Starred(AbsExpr):
    value: AbsExpr
    ctx: AbsExprContext

    @property
    def sexp(self):
        return ("Starred",
                self.value.sexp,
                self.ctx.sexp)

@dataclass
class Name(AbsExpr):
    id: AbsIdentifier
    ctx: AbsExprContext

    @property
    def sexp(self):
        return ("Name",
                self.id.sexp,
                self.ctx.sexp)

@dataclass
class AList(AbsExpr):
    elts: List[AbsExpr]
    ctx: AbsExprContext

    @property
    def sexp(self):
        return ("List",
                sexp_of_list(self.elts),
                self.ctx.sexp)

@dataclass
class ATuple(AbsExpr):
    elts: List[AbsExpr]
    ctx: AbsExprContext

    @property
    def sexp(self):
        return ("Tuple",
                sexp_of_list(self.elts),
                self.ctx.sexp)

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
