{-# LANGUAGE ScopedTypeVariables #-}
module Main where

import qualified Data.Aeson as A
import qualified Data.ByteString.Lazy as BSL
import System.Environment (getArgs)
import System.Exit (die)
import Simply.AST
import Simply.JSON ()

main :: IO ()
main = do
  args <- getArgs
  case args of
    [path] -> do
      bs <- BSL.readFile path
      case A.eitherDecode bs of
        Left err -> die $ "Failed to parse JSON: " ++ err
        Right (modAst :: Module) -> do
          putStrLn "Successfully parsed Module:"
          print modAst
    _ -> do
      putStrLn "Usage: hsimply-exe <json-file>"
      putStrLn ""
      putStrLn "Reads a JSON file containing simply AST and prints the Haskell representation."
