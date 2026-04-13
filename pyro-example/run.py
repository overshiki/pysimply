#!/usr/bin/env python3
"""
End-to-end pipeline for Bayesian inference examples.

This script demonstrates the full pipeline:
  1. Import traced models (ASTs captured by @trace)
  2. Serialize each captured AST to JSON
  3. Invoke `hsimply-exe` to parse the JSON into Haskell AST
  4. Run the Python stubs to show the DSL is executable

Supported examples:
  - Bayesian Linear Regression (1D and multi-feature)
  - Gaussian Mixture Model (with and without latent assignments)
  - Simple Clustering (minimal demonstration)
"""
import json
import os
import subprocess
import sys
import argparse

# Ensure parent directory is on path so `simply` can be imported by models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import models - each module has its own isolated trace dictionary
from model_regression import (
    model, guide,
    model_multi_feature, guide_multi_feature,
    REGRESSION_TRACE
)
from model_gmm import (
    gmm_model, gmm_guide,
    gmm_collapsed_model, gmm_collapsed_guide,
    simple_clustering, simple_clustering_guide,
    GMM_TRACE
)

# Each trace dictionary is isolated - they are distinct objects, not shared
# This is the key benefit of using make_tracer() instead of global GLOBAL_TRACE
print(f"  REGRESSION_TRACE id: {id(REGRESSION_TRACE)}, size: {len(REGRESSION_TRACE)}")
print(f"  GMM_TRACE id: {id(GMM_TRACE)}, size: {len(GMM_TRACE)}")
print(f"  Are they the same object? {REGRESSION_TRACE is GMM_TRACE}")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
HSIMPLY_DIR = os.path.join(os.path.dirname(__file__), "..", "hsimply")


def write_json(name, stmt, indent=2):
    """Write a simply AST statement to JSON file.
    
    Args:
        name: Base name for the output file
        stmt: Simply AST statement to serialize
        indent: JSON indentation level
    
    Returns:
        Path to the written file
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{name}.json")
    with open(path, "w") as f:
        # hsimply expects a Module, which is a JSON array of Stmts
        json.dump([stmt.json], f, indent=indent)
    print(f"  Wrote AST -> {path}")
    return path


def find_hsimply_exe():
    """Find the hsimply-exe executable path."""
    # Try common build paths first
    possible_paths = [
        os.path.join(HSIMPLY_DIR, "dist-newstyle", "build", "x86_64-linux", "ghc-9.6.7", "hsimply-0.1.0.0", "x", "hsimply-exe", "build", "hsimply-exe", "hsimply-exe"),
        os.path.join(HSIMPLY_DIR, "dist-newstyle", "build", "x86_64-linux", "ghc-9.4.8", "hsimply-0.1.0.0", "x", "hsimply-exe", "build", "hsimply-exe", "hsimply-exe"),
    ]
    
    for path in possible_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    
    # Fallback: try to find dynamically
    try:
        result = subprocess.run(
            ["find", os.path.join(HSIMPLY_DIR, "dist-newstyle"), "-name", "hsimply-exe", "-type", "f"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split('\n')[0]
    except Exception:
        pass
    
    return None


def run_hsimply(json_path):
    """Invoke hsimply-exe directly.
    
    Args:
        json_path: Path to the JSON file to parse
    
    Returns:
        stdout from hsimply-exe as string
    """
    exe_path = find_hsimply_exe()
    
    if exe_path is None:
        return "ERROR: hsimply-exe not found. Run 'cabal build' in hsimply/ directory."
    
    result = subprocess.run(
        [exe_path, json_path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return f"ERROR: {result.stderr}"
    return result.stdout.strip()


def test_python_stubs():
    """Run Python stubs to demonstrate they are executable."""
    print("\n" + "=" * 60)
    print("Python Stubs Execution (demonstrating valid Python)")
    print("=" * 60)
    
    # Linear regression example
    print("\n--- Bayesian Linear Regression (1D) ---")
    X = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [2.1, 3.9, 6.2, 7.8, 10.5]
    w, b, sigma = model(X, y)
    print(f"  Model returned: w={w:.2f}, b={b:.2f}, sigma={sigma:.2f}")
    w_loc, b_loc, sigma_loc = guide(X, y)
    print(f"  Guide returned: w_loc={w_loc:.2f}, b_loc={b_loc:.2f}, sigma_loc={sigma_loc:.2f}")
    
    # Multi-feature regression
    print("\n--- Bayesian Linear Regression (Multi-feature) ---")
    X_multi = [[1.0, 0.5], [2.0, 1.0], [3.0, 1.5]]
    y_multi = [1.5, 3.0, 4.5]
    n, b_multi, sigma_multi = model_multi_feature(X_multi, y_multi)
    print(f"  Model returned: n_features={n}, b={b_multi:.2f}, sigma={sigma_multi:.2f}")
    n, b_loc, sigma_loc = guide_multi_feature(X_multi, y_multi)
    print(f"  Guide returned: n_features={n}, b_loc={b_loc:.2f}, sigma_loc={sigma_loc:.2f}")
    
    # GMM example
    print("\n--- Gaussian Mixture Model ---")
    data = [-1.0, -0.5, 0.0, 5.0, 5.5, 6.0]
    n_data = gmm_model(data, K=2)
    print(f"  GMM model processed {n_data} data points")
    n_guide = gmm_guide(data, K=2)
    print(f"  GMM guide processed {n_guide} data points")
    
    # Simple clustering
    print("\n--- Simple Clustering ---")
    n_clusters = simple_clustering(data, K=2)
    print(f"  Simple clustering with K={n_clusters}")
    simple_clustering_guide(data, K=2)
    print("  Guide execution completed")


def process_model(name, stmt, verbose=False):
    """Process a single model through the pipeline.
    
    Args:
        name: Model name for output
        stmt: Simply AST statement
        verbose: Whether to print full Haskell output
    """
    print(f"\n{'=' * 60}")
    print(f"Processing: {name}")
    print('=' * 60)
    
    # Write JSON
    json_path = write_json(name, stmt)
    
    # Parse with Haskell
    print(f"  Parsing with hsimply-exe...")
    haskell_output = run_hsimply(json_path)
    
    if verbose:
        print(f"\n  Haskell AST output:")
        print(f"  {'-' * 50}")
        for line in haskell_output.split('\n'):
            print(f"  {line}")
        print(f"  {'-' * 50}")
    else:
        # Just show success/failure and first line
        if haskell_output.startswith("ERROR:"):
            print(f"  Failed: {haskell_output}")
        else:
            first_line = haskell_output.split('\n')[0] if haskell_output else "No output"
            print(f"  Success: {first_line}")
    
    return json_path


def main():
    parser = argparse.ArgumentParser(
        description='Run Bayesian inference examples through the simply pipeline'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Print full Haskell AST output'
    )
    parser.add_argument(
        '--model', '-m',
        choices=['regression', 'gmm', 'all'],
        default='all',
        help='Which model set to run (default: all)'
    )
    parser.add_argument(
        '--no-python',
        action='store_true',
        help='Skip Python stub execution'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("pysimply → JSON → hsimply Pipeline")
    print("Bayesian Inference Examples")
    print("=" * 60)
    
    # Build the combined trace from isolated trace dictionaries
    # This is now a meaningful merge because REGRESSION_TRACE and GMM_TRACE
    # are distinct objects created by separate make_tracer() calls
    ALL_TRACES = {}
    
    if args.model in ['regression', 'all']:
        ALL_TRACES.update(REGRESSION_TRACE)
        print(f"\n  Added {len(REGRESSION_TRACE)} regression models")
    
    if args.model in ['gmm', 'all']:
        ALL_TRACES.update(GMM_TRACE)
        print(f"  Added {len(GMM_TRACE)} GMM models")
    
    # Process each model
    print(f"\nTotal models to process: {len(ALL_TRACES)}")
    
    json_paths = {}
    for name, stmt in ALL_TRACES.items():
        json_paths[name] = process_model(name, stmt, verbose=args.verbose)
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Processed {len(json_paths)} models")
    print(f"Output directory: {OUTPUT_DIR}")
    for name in json_paths:
        print(f"  - {name}.json")
    
    # Run Python stubs
    if not args.no_python:
        test_python_stubs()
    
    print("\n" + "=" * 60)
    print("Pipeline completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
