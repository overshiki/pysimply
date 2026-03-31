{-# LANGUAGE OverloadedStrings #-}
module Main where

import qualified Data.Aeson as A
import qualified Data.ByteString.Lazy.Char8 as BSL
import Simply.AST
import Simply.JSON ()

main :: IO ()
main = do
  putStrLn "Running hsimply tests..."
  testExpr
  testStmt
  testModule
  putStrLn "All tests passed!"

assertRoundTrip :: (Show a, Eq a, A.ToJSON a, A.FromJSON a) => a -> IO ()
assertRoundTrip val = do
  let encoded = A.encode val
  case A.eitherDecode encoded of
    Left err -> error $ "Round-trip failed: " ++ err ++ "\nJSON: " ++ BSL.unpack encoded
    Right decoded
      | decoded == val -> return ()
      | otherwise -> error $ "Round-trip mismatch:\noriginal: " ++ show val ++ "\ndecoded:  " ++ show decoded

assertParse :: A.FromJSON a => BSL.ByteString -> IO a
assertParse json =
  case A.eitherDecode json of
    Left err -> error $ "Parse failed: " ++ err ++ "\nJSON: " ++ BSL.unpack json
    Right val -> return val

testExpr :: IO ()
testExpr = do
  putStrLn "  Testing expressions..."

  -- Name
  let nameX = Name (Identifier "x") Load
  assertRoundTrip nameX

  -- Constant
  let const1 = Constant (A.Number 1) Nothing
  assertRoundTrip const1

  -- BoolOp
  let boolOp = BoolOp And [Constant (A.Bool True) Nothing, Constant (A.Bool False) Nothing]
  assertRoundTrip boolOp

  -- BinOp
  let binOp = BinOp (Constant (A.Number 1) Nothing) Add (Constant (A.Number 1) Nothing)
  assertRoundTrip binOp

  -- UnaryOp
  let unaryOp = UnaryOp Not (Name (Identifier "x") Load)
  assertRoundTrip unaryOp

  -- Lambda
  let lambda = Lambda (Arguments [Arg "x" Nothing Nothing]) (BinOp (Name (Identifier "x") Load) Add (Constant (A.Number 1) Nothing))
  assertRoundTrip lambda

  -- IfExp
  let ifExp = IfExp (Constant (A.Bool True) Nothing) (Constant (A.Number 10) Nothing) (Constant (A.Bool False) Nothing)
  assertRoundTrip ifExp

  -- Call
  let call = Call (Name (Identifier "random") Load) [Constant (A.Number 10) Nothing] [Keywords "v" (Constant (A.Number 100) Nothing)]
  assertRoundTrip call

  -- Attribute
  let attr = Attribute (Name (Identifier "np") Load) (Identifier "random") Load
  assertRoundTrip attr

  -- Compare
  let cmp = Compare (Name (Identifier "x") Load) [Gt] [Constant (A.Number 10) Nothing]
  assertRoundTrip cmp

  -- Test parsing from actual simply JSON
  expr1 <- assertParse "{\"Name\":{\"id\":{\"Identifier\":\"x\"},\"ctx\":\"Load\"}}" :: IO Expr
  print expr1

  expr2 <- assertParse "{\"Constant\":{\"value\":1,\"kind\":null}}" :: IO Expr
  print expr2

  putStrLn "  Expressions OK."

testStmt :: IO ()
testStmt = do
  putStrLn "  Testing statements..."

  -- Pass, Break, Continue
  assertRoundTrip Pass
  assertRoundTrip Break
  assertRoundTrip Continue

  -- Expr stmt
  assertRoundTrip (Expr (Name (Identifier "a") Load))

  -- Return
  assertRoundTrip (Return (Just (Name (Identifier "x") Load)))
  assertRoundTrip (Return Nothing)

  -- Delete
  assertRoundTrip (Delete [Name (Identifier "x") Del])

  -- Assign
  assertRoundTrip (Assign [Name (Identifier "x") Store] (Constant (A.Number 1) Nothing) Nothing)

  -- If
  assertRoundTrip (If (Name (Identifier "x") Load) [Expr (Constant (A.Number 1) Nothing)] [Expr (Constant (A.Number 0) Nothing)])

  -- While
  assertRoundTrip (While (Name (Identifier "x") Load) [Expr (Constant (A.Number 1) Nothing)] [])

  -- For
  assertRoundTrip (For (Name (Identifier "i") Store) (Call (Name (Identifier "range") Load) [Constant (A.Number 10) Nothing] []) [Expr (Constant (A.Number 1) Nothing)] [] Nothing)

  -- Assert
  assertRoundTrip (Assert (Compare (Name (Identifier "x") Load) [Gt] [Constant (A.Number 10) Nothing]) Nothing)

  -- Raise
  assertRoundTrip (Raise (Just (Call (Name (Identifier "ValueError") Load) [] [])) Nothing)

  -- ImportFrom
  assertRoundTrip (ImportFrom (Just (Identifier "numpy")) [Alias (Identifier "abs") Nothing] (Just 0))

  -- Import
  assertRoundTrip (Import [Alias (Identifier "numpy") (Just (Identifier "np"))])

  -- FunctionDef
  let func = FunctionDef
        (Identifier "x")
        (Arguments
          [ Arg "a" (Just (Name (Identifier "int") Load)) Nothing
          , Arg "b" (Just (Name (Identifier "float") Load)) Nothing
          , Arg "c" (Just (Constant (A.String "Int") Nothing)) Nothing
          , Arg "d" (Just (Name (Identifier "Ret") Load)) Nothing
          ])
        [Return (Just (BinOp (Name (Identifier "x") Load) Add (Constant (A.Number 1) Nothing)))]
        []
        (Just (Name (Identifier "Ret") Load))
  assertRoundTrip func

  -- Parse from actual simply JSON
  stmt1 <- assertParse "\"Pass\"" :: IO Stmt
  print stmt1

  stmt2 <- assertParse "{\"Return\":{\"Name\":{\"id\":{\"Identifier\":\"x\"},\"ctx\":\"Load\"}}}" :: IO Stmt
  print stmt2

  stmt3 <- assertParse "{\"Import\":[{\"Alias\":{\"name\":{\"Identifier\":\"numpy\"},\"asname\":{\"Identifier\":\"np\"}}}]}" :: IO Stmt
  print stmt3

  putStrLn "  Statements OK."

testModule :: IO ()
testModule = do
  putStrLn "  Testing module..."
  let modAst = Module [Expr (Name (Identifier "a") Load), Pass]
  assertRoundTrip modAst
  putStrLn "  Module OK."
