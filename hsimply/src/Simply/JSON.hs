{-# LANGUAGE OverloadedStrings #-}
module Simply.JSON where

import qualified Data.Aeson as A
import qualified Data.Aeson.Types as A
import qualified Data.Aeson.Key as K
import qualified Data.Aeson.KeyMap as KM
import qualified Data.Text as T
import qualified Data.Vector as V
import Simply.AST

-- ---------------------------------------------------------------------------
-- Module
-- ---------------------------------------------------------------------------

instance A.FromJSON Module where
  parseJSON v = Module <$> A.parseJSON v

instance A.ToJSON Module where
  toJSON (Module stmts) = A.toJSON stmts

-- ---------------------------------------------------------------------------
-- Helpers for the tagged-union JSON format used by simply.
-- ---------------------------------------------------------------------------

withSingleKey :: A.Value -> ((T.Text, A.Value) -> A.Parser a) -> A.Parser a
withSingleKey v f = case v of
  A.Object obj ->
    case KM.toList obj of
      [(k, val)] -> f (K.toText k, val)
      _ -> A.typeMismatch "object with exactly one key" v
  _ -> A.typeMismatch "object with exactly one key" v

withText :: A.Value -> (T.Text -> A.Parser a) -> A.Parser a
withText v f = case v of
  A.String t -> f t
  _ -> A.typeMismatch "string" v

parseStringList :: A.Value -> A.Parser [String]
parseStringList = A.withArray "[String]" (mapM (A.withText "String" (return . T.unpack)) . V.toList)

-- ---------------------------------------------------------------------------
-- Identifier
-- ---------------------------------------------------------------------------

instance A.FromJSON Identifier where
  parseJSON v = withSingleKey v $ \(tag, val) ->
    case tag of
      "Identifier" -> Identifier <$> A.parseJSON val
      _ -> fail $ "Unknown Identifier tag: " ++ T.unpack tag

instance A.ToJSON Identifier where
  toJSON (Identifier s) = A.object ["Identifier" A..= s]

-- ---------------------------------------------------------------------------
-- ExprContext
-- ---------------------------------------------------------------------------

instance A.FromJSON ExprContext where
  parseJSON = A.withText "ExprContext" $ \t ->
    case t of
      "Load"  -> return Load
      "Store" -> return Store
      "Del"   -> return Del
      _ -> fail $ "Unknown ExprContext: " ++ T.unpack t

instance A.ToJSON ExprContext where
  toJSON Load  = A.String "Load"
  toJSON Store = A.String "Store"
  toJSON Del   = A.String "Del"

-- ---------------------------------------------------------------------------
-- BoolOp
-- ---------------------------------------------------------------------------

instance A.FromJSON BoolOp where
  parseJSON = A.withText "BoolOp" $ \t ->
    case t of
      "And" -> return And
      "Or"  -> return Or
      _ -> fail $ "Unknown BoolOp: " ++ T.unpack t

instance A.ToJSON BoolOp where
  toJSON And = A.String "And"
  toJSON Or  = A.String "Or"

-- ---------------------------------------------------------------------------
-- Operator
-- ---------------------------------------------------------------------------

instance A.FromJSON Operator where
  parseJSON = A.withText "Operator" $ \t ->
    case t of
      "Add"      -> return Add
      "Sub"      -> return Sub
      "Mult"     -> return Mult
      "MatMult"  -> return MatMult
      "Div"      -> return Div
      "Mod"      -> return Mod
      "Pow"      -> return Pow
      "LShift"   -> return LShift
      "RShift"   -> return RShift
      "BitOr"    -> return BitOr
      "BitXor"   -> return BitXor
      "BitAnd"   -> return BitAnd
      "FloorDiv" -> return FloorDiv
      _ -> fail $ "Unknown Operator: " ++ T.unpack t

instance A.ToJSON Operator where
  toJSON Add      = A.String "Add"
  toJSON Sub      = A.String "Sub"
  toJSON Mult     = A.String "Mult"
  toJSON MatMult  = A.String "MatMult"
  toJSON Div      = A.String "Div"
  toJSON Mod      = A.String "Mod"
  toJSON Pow      = A.String "Pow"
  toJSON LShift   = A.String "LShift"
  toJSON RShift   = A.String "RShift"
  toJSON BitOr    = A.String "BitOr"
  toJSON BitXor   = A.String "BitXor"
  toJSON BitAnd   = A.String "BitAnd"
  toJSON FloorDiv = A.String "FloorDiv"

-- ---------------------------------------------------------------------------
-- UnaryOp
-- ---------------------------------------------------------------------------

instance A.FromJSON UnaryOp where
  parseJSON = A.withText "UnaryOp" $ \t ->
    case t of
      "Invert" -> return Invert
      "Not"    -> return Not
      "UAdd"   -> return UAdd
      "USub"   -> return USub
      _ -> fail $ "Unknown UnaryOp: " ++ T.unpack t

instance A.ToJSON UnaryOp where
  toJSON Invert = A.String "Invert"
  toJSON Not    = A.String "Not"
  toJSON UAdd   = A.String "UAdd"
  toJSON USub   = A.String "USub"

-- ---------------------------------------------------------------------------
-- CmpOp
-- ---------------------------------------------------------------------------

instance A.FromJSON CmpOp where
  parseJSON = A.withText "CmpOp" $ \t ->
    case t of
      "Eq"     -> return Eq
      "NotEq"  -> return NotEq
      "Lt"     -> return Lt
      "LtE"    -> return LtE
      "Gt"     -> return Gt
      "GtE"    -> return GtE
      "Is"     -> return Is
      "IsNot"  -> return IsNot
      "In"     -> return In
      "NotIn"  -> return NotIn
      _ -> fail $ "Unknown CmpOp: " ++ T.unpack t

instance A.ToJSON CmpOp where
  toJSON Eq     = A.String "Eq"
  toJSON NotEq  = A.String "NotEq"
  toJSON Lt     = A.String "Lt"
  toJSON LtE    = A.String "LtE"
  toJSON Gt     = A.String "Gt"
  toJSON GtE    = A.String "GtE"
  toJSON Is     = A.String "Is"
  toJSON IsNot  = A.String "IsNot"
  toJSON In     = A.String "In"
  toJSON NotIn  = A.String "NotIn"

-- ---------------------------------------------------------------------------
-- Expr
-- ---------------------------------------------------------------------------

instance A.FromJSON Expr where
  parseJSON v = withSingleKey v $ \(tag, val) ->
    case tag of
      "Name"        -> A.withObject "Name"        (\o -> Name        <$> o A..: "id"   <*> o A..: "ctx") val
      "NamedExpr"   -> A.withObject "NamedExpr"   (\o -> NamedExpr   <$> o A..: "target" <*> o A..: "value") val
      "BoolOp"      -> A.withObject "BoolOp"      (\o -> BoolOp      <$> o A..: "op"   <*> o A..: "value") val
      "BinOp"       -> A.withObject "BinOp"       (\o -> BinOp       <$> o A..: "left" <*> o A..: "op" <*> o A..: "right") val
      "UnaryOp"     -> A.withObject "UnaryOp"     (\o -> UnaryOp     <$> o A..: "op" <*> o A..: "operand") val
      "Lambda"      -> A.withObject "Lambda"      (\o -> Lambda      <$> o A..: "args" <*> o A..: "body") val
      "IfExp"       -> A.withObject "IfExp"       (\o -> IfExp       <$> o A..: "test" <*> o A..: "body" <*> o A..: "orelse") val
      "Dict"        -> A.withObject "Dict"        (\o -> ADict       <$> o A..: "keys" <*> o A..: "values") val
      "Set"         -> A.parseJSON val >>= return . Set
      "ListComp"    -> A.withObject "ListComp"    (\o -> ListComp    <$> o A..: "elt" <*> o A..: "generators") val
      "SetComp"     -> A.withObject "SetComp"     (\o -> SetComp     <$> o A..: "elt" <*> o A..: "generators") val
      "DictComp"    -> A.withObject "DictComp"    (\o -> DictComp    <$> o A..: "key" <*> o A..: "value" <*> o A..: "generators") val
      "GeneratorExp"-> A.withObject "GeneratorExp"(\o -> GeneratorExp<$> o A..: "elt" <*> o A..: "generators") val
      "Await"       -> Await <$> A.parseJSON val
      "Yield"       -> Yield <$> A.parseJSON val
      "YieldFrom"   -> YieldFrom <$> A.parseJSON val
      "Compare"     -> A.withObject "Compare"     (\o -> Compare     <$> o A..: "left" <*> o A..: "ops" <*> o A..: "comparators") val
      "Call"        -> A.withObject "Call"        (\o -> Call        <$> o A..: "func" <*> o A..: "args" <*> o A..: "keywords") val
      "FormattedValue" -> A.withObject "FormattedValue" (\o -> FormattedValue <$> o A..: "value" <*> o A..: "conversion" <*> o A..: "format_spec") val
      "JoinedStr"   -> JoinedStr <$> A.parseJSON val
      "Constant"    -> A.withObject "Constant"    (\o -> Constant    <$> o A..: "value" <*> o A..: "kind") val
      "Attribute"   -> A.withObject "Attribute"   (\o -> Attribute   <$> o A..: "value" <*> o A..: "attr" <*> o A..: "ctx") val
      "Subscript"   -> A.withObject "Subscript"   (\o -> Subscript   <$> o A..: "value" <*> o A..: "aslice" <*> o A..: "ctx") val
      "Starred"     -> A.withObject "Starred"     (\o -> Starred     <$> o A..: "value" <*> o A..: "ctx") val
      "List"        -> A.withObject "List"        (\o -> AList       <$> o A..: "elts" <*> o A..: "ctx") val
      "Tuple"       -> A.withObject "Tuple"       (\o -> ATuple      <$> o A..: "elts" <*> o A..: "ctx") val
      "Slice"       -> A.withObject "Slice"       (\o -> ASlice      <$> o A..: "lower" <*> o A..: "upper" <*> o A..: "step") val
      _ -> fail $ "Unknown Expr tag: " ++ T.unpack tag

instance A.ToJSON Expr where
  toJSON (Name ident ctx)     = A.object ["Name"        A..= A.object ["id" A..= ident, "ctx" A..= ctx]]
  toJSON (NamedExpr t v)      = A.object ["NamedExpr"   A..= A.object ["target" A..= t, "value" A..= v]]
  toJSON (BoolOp op vals)     = A.object ["BoolOp"      A..= A.object ["op" A..= op, "value" A..= vals]]
  toJSON (BinOp l op r)       = A.object ["BinOp"       A..= A.object ["left" A..= l, "op" A..= op, "right" A..= r]]
  toJSON (UnaryOp op opnd)    = A.object ["UnaryOp"     A..= A.object ["op" A..= op, "operand" A..= opnd]]
  toJSON (Lambda args body)   = A.object ["Lambda"      A..= A.object ["args" A..= args, "body" A..= body]]
  toJSON (IfExp test body orelse) = A.object ["IfExp"   A..= A.object ["test" A..= test, "body" A..= body, "orelse" A..= orelse]]
  toJSON (ADict keys vals)    = A.object ["Dict"        A..= A.object ["keys" A..= keys, "values" A..= vals]]
  toJSON (Set elts)           = A.object ["Set"         A..= elts]
  toJSON (ListComp elt gens)  = A.object ["ListComp"    A..= A.object ["elt" A..= elt, "generators" A..= gens]]
  toJSON (SetComp elt gens)   = A.object ["SetComp"     A..= A.object ["elt" A..= elt, "generators" A..= gens]]
  toJSON (DictComp k v gens)  = A.object ["DictComp"    A..= A.object ["key" A..= k, "value" A..= v, "generators" A..= gens]]
  toJSON (GeneratorExp elt gens) = A.object ["GeneratorExp" A..= A.object ["elt" A..= elt, "generators" A..= gens]]
  toJSON (Await e)            = A.object ["Await"       A..= e]
  toJSON (Yield e)            = A.object ["Yield"       A..= e]
  toJSON (YieldFrom e)        = A.object ["YieldFrom"   A..= e]
  toJSON (Compare left ops comps) = A.object ["Compare" A..= A.object ["left" A..= left, "ops" A..= ops, "comparators" A..= comps]]
  toJSON (Call func args kw)  = A.object ["Call"        A..= A.object ["func" A..= func, "args" A..= args, "keywords" A..= kw]]
  toJSON (FormattedValue v c fs) = A.object ["FormattedValue" A..= A.object ["value" A..= v, "conversion" A..= c, "format_spec" A..= fs]]
  toJSON (JoinedStr vals)     = A.object ["JoinedStr"   A..= vals]
  toJSON (Constant v k)       = A.object ["Constant"    A..= A.object ["value" A..= v, "kind" A..= k]]
  toJSON (Attribute val attr ctx) = A.object ["Attribute" A..= A.object ["value" A..= val, "attr" A..= attr, "ctx" A..= ctx]]
  toJSON (Subscript val sl ctx) = A.object ["Subscript" A..= A.object ["value" A..= val, "aslice" A..= sl, "ctx" A..= ctx]]
  toJSON (Starred val ctx)    = A.object ["Starred"     A..= A.object ["value" A..= val, "ctx" A..= ctx]]
  toJSON (AList elts ctx)     = A.object ["List"        A..= A.object ["elts" A..= elts, "ctx" A..= ctx]]
  toJSON (ATuple elts ctx)    = A.object ["Tuple"       A..= A.object ["elts" A..= elts, "ctx" A..= ctx]]
  toJSON (ASlice l u s)       = A.object ["Slice"       A..= A.object ["lower" A..= l, "upper" A..= u, "step" A..= s]]

-- ---------------------------------------------------------------------------
-- Stmt
-- ---------------------------------------------------------------------------

instance A.FromJSON Stmt where
  parseJSON v = case v of
    A.String "Pass"     -> return Pass
    A.String "Break"    -> return Break
    A.String "Continue" -> return Continue
    _ -> withSingleKey v $ \(tag, val) ->
      case tag of
        "FunctionDef"     -> A.withObject "FunctionDef"     (\o -> FunctionDef     <$> o A..: "name" <*> o A..: "args" <*> o A..: "body" <*> o A..: "decorator_list" <*> o A..: "returns") val
        "AsyncFunctionDef"-> A.withObject "AsyncFunctionDef"(\o -> AsyncFunctionDef<$> o A..: "name" <*> o A..: "args" <*> o A..: "body" <*> o A..: "decorator_list" <*> o A..: "returns") val
        "ClassDef"        -> A.withObject "ClassDef"        (\o -> ClassDef        <$> o A..: "name" <*> o A..: "bases" <*> o A..: "keywords" <*> o A..: "body" <*> o A..: "decorator_list" <*> o A..: "type_params") val
        "Return"          -> Return <$> A.parseJSON val
        "Delete"          -> Delete <$> A.parseJSON val
        "Assign"          -> A.withObject "Assign"          (\o -> Assign          <$> o A..: "targets" <*> o A..: "value" <*> o A..: "type_comment") val
        "TypeAlias"       -> A.withObject "TypeAlias"       (\o -> TypeAlias       <$> o A..: "name" <*> o A..: "type_params" <*> o A..: "value") val
        "AugAssign"       -> A.withObject "AugAssign"       (\o -> AugAssign       <$> o A..: "target" <*> o A..: "op" <*> o A..: "value") val
        "AnnAssign"       -> A.withObject "AnnAssign"       (\o -> AnnAssign       <$> o A..: "target" <*> o A..: "annotation" <*> o A..: "value" <*> o A..: "simple") val
        "For"             -> A.withObject "For"             (\o -> For             <$> o A..: "target" <*> o A..: "iter" <*> o A..: "body" <*> o A..: "orelse" <*> o A..: "type_comment") val
        "AsyncFor"        -> A.withObject "AsyncFor"        (\o -> AsyncFor        <$> o A..: "target" <*> o A..: "iter" <*> o A..: "body" <*> o A..: "orelse" <*> o A..: "type_comment") val
        "While"           -> A.withObject "While"           (\o -> While           <$> o A..: "test" <*> o A..: "body" <*> o A..: "orelse") val
        "If"              -> A.withObject "If"              (\o -> If              <$> o A..: "test" <*> o A..: "body" <*> o A..: "orelse") val
        "With"            -> A.withObject "With"            (\o -> With            <$> o A..: "items" <*> o A..: "body" <*> o A..: "type_comment") val
        "AsyncWith"       -> A.withObject "AsyncWith"       (\o -> AsyncWith       <$> o A..: "items" <*> o A..: "body" <*> o A..: "type_comment") val
        "Match"           -> A.withObject "Match"           (\o -> Match           <$> o A..: "subject" <*> o A..: "cases") val
        "Raise"           -> A.withObject "Raise"           (\o -> Raise           <$> o A..: "exc" <*> o A..: "cause") val
        "Try"             -> A.withObject "Try"             (\o -> Try             <$> o A..: "body" <*> o A..: "handlers" <*> o A..: "orelse" <*> o A..: "finalbody") val
        "TryStar"         -> A.withObject "TryStar"         (\o -> TryStar         <$> o A..: "body" <*> o A..: "handlers" <*> o A..: "orelse" <*> o A..: "finalbody") val
        "Assert"          -> A.withObject "Assert"          (\o -> Assert          <$> o A..: "test" <*> o A..: "msg") val
        "Import"          -> Import <$> A.parseJSON val
        "ImportFrom"      -> A.withObject "ImportFrom"      (\o -> ImportFrom      <$> o A..: "module" <*> o A..: "names" <*> o A..: "level") val
        "Global"          -> Global <$> A.parseJSON val
        "Nonlocal"        -> Nonlocal <$> A.parseJSON val
        "Expr"            -> Expr <$> A.parseJSON val
        _ -> fail $ "Unknown Stmt tag: " ++ T.unpack tag

instance A.ToJSON Stmt where
  toJSON Pass                 = A.String "Pass"
  toJSON Break                = A.String "Break"
  toJSON Continue             = A.String "Continue"
  toJSON (FunctionDef n a b d r) = A.object ["FunctionDef" A..= A.object ["name" A..= n, "args" A..= a, "body" A..= b, "decorator_list" A..= d, "returns" A..= r]]
  toJSON (AsyncFunctionDef n a b d r) = A.object ["AsyncFunctionDef" A..= A.object ["name" A..= n, "args" A..= a, "body" A..= b, "decorator_list" A..= d, "returns" A..= r]]
  toJSON (ClassDef n bs kw b d tp) = A.object ["ClassDef" A..= A.object ["name" A..= n, "bases" A..= bs, "keywords" A..= kw, "body" A..= b, "decorator_list" A..= d, "type_params" A..= tp]]
  toJSON (Return e)           = A.object ["Return" A..= e]
  toJSON (Delete es)          = A.object ["Delete" A..= es]
  toJSON (Assign ts v tc)     = A.object ["Assign" A..= A.object ["targets" A..= ts, "value" A..= v, "type_comment" A..= tc]]
  toJSON (TypeAlias n tp v)   = A.object ["TypeAlias" A..= A.object ["name" A..= n, "type_params" A..= tp, "value" A..= v]]
  toJSON (AugAssign t op v)   = A.object ["AugAssign" A..= A.object ["target" A..= t, "op" A..= op, "value" A..= v]]
  toJSON (AnnAssign t a v s)  = A.object ["AnnAssign" A..= A.object ["target" A..= t, "annotation" A..= a, "value" A..= v, "simple" A..= s]]
  toJSON (For t i b o tc)     = A.object ["For" A..= A.object ["target" A..= t, "iter" A..= i, "body" A..= b, "orelse" A..= o, "type_comment" A..= tc]]
  toJSON (AsyncFor t i b o tc)= A.object ["AsyncFor" A..= A.object ["target" A..= t, "iter" A..= i, "body" A..= b, "orelse" A..= o, "type_comment" A..= tc]]
  toJSON (While t b o)        = A.object ["While" A..= A.object ["test" A..= t, "body" A..= b, "orelse" A..= o]]
  toJSON (If t b o)           = A.object ["If" A..= A.object ["test" A..= t, "body" A..= b, "orelse" A..= o]]
  toJSON (With is b tc)       = A.object ["With" A..= A.object ["items" A..= is, "body" A..= b, "type_comment" A..= tc]]
  toJSON (AsyncWith is b tc)  = A.object ["AsyncWith" A..= A.object ["items" A..= is, "body" A..= b, "type_comment" A..= tc]]
  toJSON (Match s cs)         = A.object ["Match" A..= A.object ["subject" A..= s, "cases" A..= cs]]
  toJSON (Raise e c)          = A.object ["Raise" A..= A.object ["exc" A..= e, "cause" A..= c]]
  toJSON (Try b h o f)        = A.object ["Try" A..= A.object ["body" A..= b, "handlers" A..= h, "orelse" A..= o, "finalbody" A..= f]]
  toJSON (TryStar b h o f)    = A.object ["TryStar" A..= A.object ["body" A..= b, "handlers" A..= h, "orelse" A..= o, "finalbody" A..= f]]
  toJSON (Assert t m)         = A.object ["Assert" A..= A.object ["test" A..= t, "msg" A..= m]]
  toJSON (Import ns)          = A.object ["Import" A..= ns]
  toJSON (ImportFrom m ns l)  = A.object ["ImportFrom" A..= A.object ["module" A..= m, "names" A..= ns, "level" A..= l]]
  toJSON (Global ns)          = A.object ["Global" A..= ns]
  toJSON (Nonlocal ns)        = A.object ["Nonlocal" A..= ns]
  toJSON (Expr e)             = A.object ["Expr" A..= e]

-- ---------------------------------------------------------------------------
-- Arguments & Arg
-- ---------------------------------------------------------------------------

instance A.FromJSON Arguments where
  parseJSON v = withSingleKey v $ \(tag, val) ->
    case tag of
      "Arguments" -> Arguments <$> A.parseJSON val
      _ -> fail $ "Unknown Arguments tag: " ++ T.unpack tag

instance A.ToJSON Arguments where
  toJSON (Arguments args) = A.object ["Arguments" A..= args]

instance A.FromJSON Arg where
  parseJSON v = withSingleKey v $ \(tag, val) ->
    case tag of
      "Arg" -> A.withObject "Arg" (\o -> Arg <$> o A..: "arg" <*> o A..: "annotation" <*> o A..: "type_comment") val
      _ -> fail $ "Unknown Arg tag: " ++ T.unpack tag

instance A.ToJSON Arg where
  toJSON (Arg a ann tc) = A.object ["Arg" A..= A.object ["arg" A..= a, "annotation" A..= ann, "type_comment" A..= tc]]

-- ---------------------------------------------------------------------------
-- Keyword
-- ---------------------------------------------------------------------------

instance A.FromJSON Keyword where
  parseJSON v = withSingleKey v $ \(tag, val) ->
    case tag of
      "Keywords" -> A.withObject "Keywords" (\o -> Keywords <$> o A..: "arg" <*> o A..: "value") val
      _ -> fail $ "Unknown Keyword tag: " ++ T.unpack tag

instance A.ToJSON Keyword where
  toJSON (Keywords arg val) = A.object ["Keywords" A..= A.object ["arg" A..= arg, "value" A..= val]]

-- ---------------------------------------------------------------------------
-- Alias
-- ---------------------------------------------------------------------------

instance A.FromJSON Alias where
  parseJSON v = withSingleKey v $ \(tag, val) ->
    case tag of
      "Alias" -> A.withObject "Alias" (\o -> Alias <$> o A..: "name" <*> o A..: "asname") val
      _ -> fail $ "Unknown Alias tag: " ++ T.unpack tag

instance A.ToJSON Alias where
  toJSON (Alias n a) = A.object ["Alias" A..= A.object ["name" A..= n, "asname" A..= a]]

-- ---------------------------------------------------------------------------
-- Withitem
-- ---------------------------------------------------------------------------

instance A.FromJSON Withitem where
  parseJSON v = withSingleKey v $ \(tag, val) ->
    case tag of
      "Withitem" -> A.withObject "Withitem" (\o -> Withitem <$> o A..: "context_expr" <*> o A..: "optional_vars") val
      _ -> fail $ "Unknown Withitem tag: " ++ T.unpack tag

instance A.ToJSON Withitem where
  toJSON (Withitem ce ov) = A.object ["Withitem" A..= A.object ["context_expr" A..= ce, "optional_vars" A..= ov]]

-- ---------------------------------------------------------------------------
-- MatchCase
-- ---------------------------------------------------------------------------

instance A.FromJSON MatchCase where
  parseJSON v = withSingleKey v $ \(tag, val) ->
    case tag of
      "MatchCase" -> A.withObject "MatchCase" (\o -> MatchCase <$> o A..: "pattern" <*> o A..: "guard" <*> o A..: "body") val
      _ -> fail $ "Unknown MatchCase tag: " ++ T.unpack tag

instance A.ToJSON MatchCase where
  toJSON (MatchCase p g b) = A.object ["MatchCase" A..= A.object ["pattern" A..= p, "guard" A..= g, "body" A..= b]]

-- ---------------------------------------------------------------------------
-- Placeholder types
-- ---------------------------------------------------------------------------

instance A.FromJSON Comprehension where
  parseJSON _ = return Comprehension

instance A.ToJSON Comprehension where
  toJSON _ = A.object ["Comprehension" A..= A.Null]

instance A.FromJSON ExceptHandler where
  parseJSON _ = return ExceptHandler

instance A.ToJSON ExceptHandler where
  toJSON _ = A.object ["ExceptHandler" A..= A.Null]

instance A.FromJSON Pattern where
  parseJSON _ = return Pattern

instance A.ToJSON Pattern where
  toJSON _ = A.object ["Pattern" A..= A.Null]

instance A.FromJSON TypeParam where
  parseJSON _ = return TypeParam

instance A.ToJSON TypeParam where
  toJSON _ = A.object ["TypeParam" A..= A.Null]
