# pysimply

A simplified Python AST representation designed for easy manipulation and eDSL implementation.

## Overview

`simply` takes standard Python `ast` nodes and converts them into a small, typed, dataclass-based hierarchy. Each node can be rendered in three ways:

- **S-expression** (`sexp`) — Lisp-like symbolic representation.
- **JSON** (`json`) — Structured output for cross-language consumption.
- **Python AST** (`ast`) — Round-trips back to the standard library `ast` module.

This makes `simply` ideal for capturing the syntax of embedded DSLs written in Python and transporting them to other languages or tools.

## Project Structure

```
.
├── simply/          # Python package — simplified AST types and parser
├── hsimply/         # Haskell package — reads simply JSON into Haskell AST
├── pyro-example/    # End-to-end demo: Pyro-like DSL → JSON → Haskell
└── unit/            # Unit tests for the Python package
```

## Python Package (`simply/`)

The `simply` package provides:

- **Abstract base classes** (`abstract.py`) — `AbsExpr`, `AbsStmt`, `AbsOperator`, etc.
- **Concrete AST nodes** (`expr.py`, `stmt.py`, `extra.py`) — Dataclasses like `Name`, `BinOp`, `FunctionDef`, `Assign`, `Call`, etc.
- **Parser** (`parse_base.py`, `parse_expr.py`, `parse_stmt.py`, `parse_extra.py`) — Single-dispatch functions that convert `ast.AST` nodes into `simply` nodes.
- **Tracing decorator** (`trace.py`) — `@trace` captures the AST of a decorated function at import time without changing its runtime behavior.

### Quick Example

```python
import ast
from simply.parse_stmt import parse

code = "def add(x, y): return x + y"
tree = ast.parse(code)
stmt = parse(tree.body[0])

print(stmt.json)
# {"FunctionDef": {"name": {"Identifier": "add"}, ...}}
```

## Haskell Package (`hsimply/`)

`hsimply` is a Haskell implementation that reads JSON files produced by the Python `simply` package and reconstructs them as native Haskell AST data structures.

- `Simply.AST` — Haskell data types that mirror the Python `simply` hierarchy (`Expr`, `Stmt`, `Identifier`, `Arguments`, etc.).
- `Simply.JSON` — `aeson`-based `FromJSON` / `ToJSON` instances for the tagged-union JSON format used by `simply`.

### Building

```bash
cd hsimply
cabal build
cabal test
```

### Usage

```haskell
import qualified Data.Aeson as A
import qualified Data.ByteString.Lazy as BSL
import Simply.AST
import Simply.JSON ()

main = do
  bs <- BSL.readFile "ast.json"
  print (A.eitherDecode bs :: Either String Module)
```

## End-to-End Demo (`pyro-example/`)

`pyro-example` demonstrates the full pipeline:

1. **Write a Pyro-like model in Python** using stub primitives (`sample`, `param`, `plate`, `Normal`).
2. **Capture the AST** with `@trace` from `simply.trace`.
3. **Serialize to JSON** using `simply`.
4. **Parse in Haskell** using `hsimply-exe` via `cabal run`.

### Running the Demo

```bash
python pyro-example/run.py
```

This will:
- Write `model.json` and `guide.json` to `pyro-example/output/`.
- Invoke `hsimply-exe` to parse each JSON file into a Haskell `Module`.
- Print the resulting Haskell AST.

## Implementation Status

- expr:
  - Name [x]
  - Constant [x]
  - BoolOp [x]
  - NamedExpr []
  - BinOp [x]
  - UnaryOp [x]
  - Lambda [x]
  - IfExp [x]
  - Dict []
  - Set []
  - ListComp []
  - SetComp []
  - DictComp []
  - GeneratorExp []
  - Await []
  - Yield []
  - YieldFrom []
  - Compare [x]
  - Call [x]
  - FormattedValue []
  - JoinedStr []
  - Attribute [x]
  - Subscript [x]
  - Starred []
  - List []
  - Tuple []
  - Slice []
- stmt
  - FunctionDef [x]
  - AsyncFunctionDef []
  - ClassDef []
  - Return [x]
  - Delete [x]
  - Assign [x]
  - TypeAlias []
  - AugAssign []
  - AnnAssign []
  - For [x]
  - AsyncFor []
  - While [x]
  - If [x]
  - With []
  - AsyncWith []
  - Match []
  - Raise [x]
  - Try []
  - TryStar []
  - Assert [x]
  - Import [x]
  - ImportFrom [x]
  - Global []
  - Nonlocal []
  - Expr [x]
  - Pass [x]
  - Break [x]
  - Continue [x]
