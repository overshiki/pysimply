{-# LANGUAGE DeriveGeneric #-}
module Simply.AST where

import qualified Data.Aeson as A

-- | A module is a list of statements.
newtype Module = Module { moduleBody :: [Stmt] }
  deriving (Show, Eq)

data Stmt
  = FunctionDef Identifier Arguments [Stmt] [Expr] (Maybe Expr)
  | AsyncFunctionDef Identifier Arguments [Stmt] [Expr] (Maybe Expr)
  | ClassDef Identifier [Expr] [Keyword] [Stmt] [Expr] [TypeParam]
  | Return (Maybe Expr)
  | Delete [Expr]
  | Assign [Expr] Expr (Maybe String)
  | TypeAlias Expr [TypeParam] Expr
  | AugAssign Expr Operator Expr
  | AnnAssign Expr Expr (Maybe Expr) Int
  | For Expr Expr [Stmt] [Stmt] (Maybe String)
  | AsyncFor Expr Expr [Stmt] [Stmt] (Maybe String)
  | While Expr [Stmt] [Stmt]
  | If Expr [Stmt] [Stmt]
  | With [Withitem] [Stmt] (Maybe String)
  | AsyncWith [Withitem] [Stmt] (Maybe String)
  | Match Expr [MatchCase]
  | Raise (Maybe Expr) (Maybe Expr)
  | Try [Stmt] [ExceptHandler] [Stmt] [Stmt]
  | TryStar [Stmt] [ExceptHandler] [Stmt] [Stmt]
  | Assert Expr (Maybe Expr)
  | Import [Alias]
  | ImportFrom (Maybe Identifier) [Alias] (Maybe Int)
  | Global [Identifier]
  | Nonlocal [Identifier]
  | Expr Expr
  | Pass
  | Break
  | Continue
  deriving (Show, Eq)

data Expr
  = Name Identifier ExprContext
  | NamedExpr Expr Expr
  | BoolOp BoolOp [Expr]
  | BinOp Expr Operator Expr
  | UnaryOp UnaryOp Expr
  | Lambda Arguments Expr
  | IfExp Expr Expr Expr
  | ADict [Expr] [Expr]
  | Set [Expr]
  | ListComp Expr [Comprehension]
  | SetComp Expr [Comprehension]
  | DictComp Expr Expr [Comprehension]
  | GeneratorExp Expr [Comprehension]
  | Await Expr
  | Yield (Maybe Expr)
  | YieldFrom Expr
  | Compare Expr [CmpOp] [Expr]
  | Call Expr [Expr] [Keyword]
  | FormattedValue Expr Int (Maybe Expr)
  | JoinedStr [Expr]
  | Constant A.Value (Maybe String)
  | Attribute Expr Identifier ExprContext
  | Subscript Expr Expr ExprContext
  | Starred Expr ExprContext
  | AList [Expr] ExprContext
  | ATuple [Expr] ExprContext
  | ASlice (Maybe Expr) (Maybe Expr) (Maybe Expr)
  deriving (Show, Eq)

data ExprContext = Load | Store | Del
  deriving (Show, Eq)

data BoolOp = And | Or
  deriving (Show, Eq)

data Operator
  = Add | Sub | Mult | MatMult | Div | Mod | Pow
  | LShift | RShift | BitOr | BitXor | BitAnd | FloorDiv
  deriving (Show, Eq)

data UnaryOp = Invert | Not | UAdd | USub
  deriving (Show, Eq)

data CmpOp
  = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn
  deriving (Show, Eq)

newtype Identifier = Identifier String
  deriving (Show, Eq)

data Arguments = Arguments [Arg]
  deriving (Show, Eq)

data Arg = Arg String (Maybe Expr) (Maybe String)
  deriving (Show, Eq)

data Keyword = Keywords String Expr
  deriving (Show, Eq)

data Alias = Alias Identifier (Maybe Identifier)
  deriving (Show, Eq)

data Withitem = Withitem Expr (Maybe Expr)
  deriving (Show, Eq)

data MatchCase = MatchCase Pattern (Maybe Expr) [Stmt]
  deriving (Show, Eq)

-- Placeholder types for constructs not yet fully implemented in simply.
data Comprehension = Comprehension
  deriving (Show, Eq)

data ExceptHandler = ExceptHandler
  deriving (Show, Eq)

data Pattern = Pattern
  deriving (Show, Eq)

data TypeParam = TypeParam
  deriving (Show, Eq)
