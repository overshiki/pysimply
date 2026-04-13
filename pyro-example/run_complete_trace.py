#!/usr/bin/env python3
"""
Runner for complete entry-point based DSL with internal function tracing.

This demonstrates the architecture where:
- Entry points (@trace_cap) capture AST + external parameters
- Internal functions (@trace) capture AST only  
- PROGRAM_TRACE contains ALL functions for Haskell compilation
"""
import json
import os
import subprocess
import sys
import argparse

# Ensure parent directory is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the model with complete tracing
from bayesian_model import (
    main, guide_main, predict_main,
    PROGRAM_TRACE, get_run_info
)

HSIMPLY_DIR = os.path.join(os.path.dirname(__file__), "..", "hsimply")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output", "bayesian_complete")


def find_hsimply_exe():
    """Find the hsimply-exe executable path."""
    possible_paths = [
        os.path.join(HSIMPLY_DIR, "dist-newstyle", "build", "x86_64-linux", "ghc-9.6.7", "hsimply-0.1.0.0", "x", "hsimply-exe", "build", "hsimply-exe", "hsimply-exe"),
        os.path.join(HSIMPLY_DIR, "dist-newstyle", "build", "x86_64-linux", "ghc-9.4.8", "hsimply-0.1.0.0", "x", "hsimply-exe", "build", "hsimply-exe", "hsimply-exe"),
    ]
    
    for path in possible_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    
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
    """Invoke hsimply-exe directly."""
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


def categorize_functions():
    """Categorize traced functions by type (entry point vs internal)."""
    entry_points = []
    internal_functions = []
    
    for name in PROGRAM_TRACE:
        # Check if there's a params file (indicates trace_cap)
        params_file = os.path.join(OUTPUT_DIR, f"{name}_params.json")
        if os.path.exists(params_file):
            entry_points.append(name)
        else:
            internal_functions.append(name)
    
    return entry_points, internal_functions


def main_runner():
    parser = argparse.ArgumentParser(
        description='Run complete entry-point DSL with internal function tracing'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Print full Haskell output'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Complete Entry-Point DSL Pipeline")
    print("(with internal function tracing)")
    print("=" * 70)
    
    # ========================================================================
    # Phase 1: Import-Time Capture
    # ========================================================================
    print("\n" + "-" * 70)
    print("Phase 1: Import-Time Capture (all @trace and @trace_cap)")
    print("-" * 70)
    
    print(f"\n  Total functions in PROGRAM_TRACE: {len(PROGRAM_TRACE)}")
    print(f"  Functions: {list(PROGRAM_TRACE.keys())}")
    print(f"\n  Note: After execution, functions with _params.json are entry points (@trace_cap)")
    print(f"        Functions without _params.json are internal (@trace)")
    
    # ========================================================================
    # Phase 2: Execute Entry Points
    # ========================================================================
    print("\n" + "-" * 70)
    print("Phase 2: Execute Entry Points (triggers parameter capture)")
    print("-" * 70)
    
    # Example 1: Main model
    print("\n[Example 1] main() - Bayesian Linear Regression")
    print("-" * 50)
    
    training_data = {
        "x": [1.0, 2.0, 3.0, 4.0, 5.0],
        "y": [2.1, 3.9, 5.8, 8.1, 10.2]
    }
    model_config = {"prior_scale": 1.0, "model_name": "simple_linear"}
    inference_hp = {"algorithm": "SVI", "n_iterations": 1000, "learning_rate": 0.01}
    
    print(f"  Input data: {len(training_data['x'])} observations")
    result = main(training_data, model_config, inference_hp)
    
    print(f"  Result: {result['params']}")
    
    run_info = get_run_info()
    print(f"  Output: {run_info['output_dir']}")
    
    # Example 2: Guide
    print("\n[Example 2] guide_main() - Variational Guide")
    print("-" * 50)
    
    guide_result = guide_main(training_data, model_config, inference_hp)
    print(f"  Variational params: {list(guide_result['variational_params'].keys())}")
    
    # Example 3: Prediction
    print("\n[Example 3] predict_main() - Prediction")
    print("-" * 50)
    
    model_params = result['params']
    new_data = [6.0, 7.0, 8.0]
    
    pred_result = predict_main(model_params, new_data, model_config)
    print(f"  Predictions for {new_data}: {pred_result['predictions']}")
    
    # ========================================================================
    # Phase 3: Verify Output
    # ========================================================================
    print("\n" + "-" * 70)
    print("Phase 3: Output Verification")
    print("-" * 70)
    
    print(f"\n  Output directory: {OUTPUT_DIR}")
    print("\n  Files generated:")
    
    all_files = sorted(os.listdir(OUTPUT_DIR))
    
    # Categorize files (after execution when params files exist)
    entry_points, internal_functions = categorize_functions()
    
    ast_files = [f for f in all_files if f.endswith('.json') and not f.endswith('_params.json') and f != 'manifest.json']
    params_files = [f for f in all_files if f.endswith('_params.json')]
    
    print("\n    AST files (all functions):")
    for f in ast_files:
        size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
        func_name = f.replace('.json', '')
        func_type = "[ENTRY]" if func_name in entry_points else "[internal]"
        print(f"      {func_type} {f} ({size} bytes)")
    
    print("\n    Parameter files (entry points only):")
    for f in params_files:
        size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
        print(f"      {f} ({size} bytes)")
    
    # ========================================================================
    # Phase 4: Haskell Parsing
    # ========================================================================
    print("\n" + "-" * 70)
    print("Phase 4: Haskell AST Parsing")
    print("-" * 70)
    
    print(f"\n  Entry points: {entry_points}")
    for name in entry_points:
        ast_path = os.path.join(OUTPUT_DIR, f"{name}.json")
        if os.path.exists(ast_path):
            result = run_hsimply(ast_path)
            status = "✓" if not result.startswith("ERROR") else "✗"
            print(f"    {status} {name}.json")
            if args.verbose and not result.startswith("ERROR"):
                first_line = result.split('\n')[0] if result else "No output"
                print(f"       -> {first_line}")
    
    print(f"\n  Internal functions: {internal_functions}")
    for name in internal_functions:
        ast_path = os.path.join(OUTPUT_DIR, f"{name}.json")
        if os.path.exists(ast_path):
            result = run_hsimply(ast_path)
            status = "✓" if not result.startswith("ERROR") else "✗"
            print(f"    {status} {name}.json")
    
    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    print("\n  Architecture:")
    print("    ┌─────────────────────────────────────────────┐")
    print("    │  Entry Point (main)  [@trace_cap]           │")
    print("    │  - Captures AST                             │")
    print("    │  - Serializes external parameters           │")
    print("    └──────────────────┬──────────────────────────┘")
    print("                       │ calls")
    print("         ┌─────────────┼─────────────┐")
    print("         ▼             ▼             ▼")
    print("    ┌─────────┐  ┌─────────┐  ┌─────────┐")
    print("    │Internal │  │Internal │  │Internal │")
    print("    │Function │  │Function │  │Function │")
    print("    │[@trace] │  │[@trace] │  │[@trace] │")
    print("    └─────────┘  └─────────┘  └─────────┘")
    
    print("\n  Key insight:")
    print("    - Entry point receives EXTERNAL data (captured to params.json)")
    print("    - Internal functions receive INTERNAL data (from computation flow)")
    print("    - Haskell gets COMPLETE program (all ASTs) for compilation")
    
    print("\n  For Haskell compilation:")
    print("    1. Load all AST files → Complete program structure")
    print("    2. Load entry point params → External data")
    print("    3. Compile/interpret with concrete parameters")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main_runner()
