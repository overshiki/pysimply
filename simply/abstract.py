
class IsData:
    @property
    def sexp(self):
        raise NotImplementedError()
    
    @property
    def ast(self):
        raise NotImplementedError()

    # @property
    # def json(self):
    #     raise NotImplementedError()

class AbsStmt(IsData):
    pass

class AbsExpr(IsData):
    pass

class AbsExprContext(IsData):
    pass 

class AbsBoolOp(IsData):
    pass 

class AbsOperator(IsData):
    pass 

class AbsUnaryOp(IsData):
    pass 

class AbsCmpop(IsData):
    pass

class AbsComprehension(IsData):
    pass

class AbsExcepthandler(IsData):
    pass

class AbsArguments(IsData):
    pass 

class AbsArg(IsData):
    pass 

class AbsKeyword(IsData):
    pass 

class AbsAlias(IsData):
    pass 

class AbsWithitem(IsData):
    pass 

class AbsMatchCase(IsData):
    pass 

class AbsPattern(IsData):
    pass 

class AbsTypeIgnore(IsData):
    pass 

class AbsTypeParam(IsData):
    pass

class AbsIdentifier(IsData):
    pass

class AbsConstant(IsData):
    pass

class AbsWithitem(IsData):
    pass

def sexp_of_list(values):
    return tuple(map(lambda x:x.sexp, values))

def sexp_of_optional(value):
    if value is None:
        return None
    else:
        return value.sexp