#!/usr/bin/env python3
"""
End-to-end pipeline:
  1. Import the traced model/guide (AST is captured by `@trace`).
  2. Serialize each captured AST to JSON.
  3. Invoke `hsimply-exe` to parse the JSON into Haskell AST.
  4. Run the Python stubs to show the DSL is executable.
"""
import json
import os
import subprocess
import sys

# Ensure parent directory is on path so `simply` can be imported by model.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model import model, guide, GLOBAL_TRACE

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
HSIMPLY_DIR = os.path.join(os.path.dirname(__file__), "..", "hsimply")


def write_json(name, stmt):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{name}.json")
    with open(path, "w") as f:
        # hsimply expects a Module, which is a JSON array of Stmts
        json.dump([stmt.json], f, indent=2)
    print(f"Wrote AST for '{name}' -> {path}")
    return path


def run_hsimply(json_path):
    """Invoke hsimply-exe via `cabal run` so the path is stable across GHC versions."""
    result = subprocess.run(
        ["cabal", "run", "hsimply-exe", "--", json_path],
        cwd=HSIMPLY_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"hsimply-exe failed on {json_path}:")
        print(result.stderr)
        sys.exit(1)
    return result.stdout


def main():
    # 1. ASTs are already captured inside GLOBAL_TRACE by importing model.py
    # 2. Write JSON files
    json_paths = {}
    for name, stmt in GLOBAL_TRACE.items():
        json_paths[name] = write_json(name, stmt)

    # 3. Run hsimply-exe on each JSON file
    for name, path in json_paths.items():
        print(f"\n=== Haskell parse of '{name}' ===")
        print(run_hsimply(path).strip())

    # 4. Run the Python stubs (they are no-ops, but executable)
    print("\n=== Running Python stubs ===")
    dummy_data = [1.0, 2.0, 3.0]
    print(f"model({dummy_data}) = {model(dummy_data)}")
    print(f"guide({dummy_data}) = {guide(dummy_data)}")


if __name__ == "__main__":
    main()
