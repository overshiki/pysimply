
class IsData:
    @property
    def sexp(self):
        '''
        generating sexp repr
        '''
        raise NotImplementedError()
    
    @property
    def json(self):
        '''
        generating json repr
        '''
        print(self.__class__.__name__)
        raise NotImplementedError()

    @property
    def ast(self):
        '''
        generating python-ast
        '''
        raise NotImplementedError()


class AbsStmt(IsData):
    pass

class AbsExpr(IsData):
    pass

class AbsExprContext(IsData):
    @property
    def sexp(self):
        return (self.__class__.__name__)

    @property
    def json(self):
        return self.__class__.__name__

class AbsBoolOp(IsData):
    @property
    def sexp(self):
        return (self.__class__.__name__)

    @property
    def json(self):
        return self.__class__.__name__


class AbsOperator(IsData):
    @property
    def sexp(self):
        return (self.__class__.__name__)

    @property
    def json(self):
        return self.__class__.__name__

class AbsUnaryOp(IsData):
    @property
    def sexp(self):
        return (self.__class__.__name__)

    @property
    def json(self):
        return self.__class__.__name__

class AbsCmpop(IsData):
    @property
    def sexp(self):
        return (self.__class__.__name__)

    @property
    def json(self):
        return self.__class__.__name__

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

def json_of_list(values):
    return list(map(lambda x:x.json, values))

def sexp_of_optional(value):
    if value is None:
        return None
    else:
        return value.sexp

def json_of_optional(value):
    if value is None:
        return None
    else:
        return value.json

def ast_of_list(values):
    return list(map(lambda x:x.ast, values))

def ast_of_optional(value):
    if value is None:
        return None 
    else:
        return value.ast
