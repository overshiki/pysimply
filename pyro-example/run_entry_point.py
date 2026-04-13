#!/usr/bin/env python3
"""
Runner for entry-point based DSL examples.

This script demonstrates how to use the new trace_and_capture system:
1. Import the entry-point module
2. Call the main function with parameters
3. Verify that both AST and parameters were captured
4. Run the Haskell parser on the captured files
"""
import json
import os
import subprocess
import sys
import argparse

# Ensure parent directory is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the entry-point model
from bayesian_model import (
    main, guide_main, predict_main,
    PROGRAM_TRACE as ENTRY_TRACE, get_run_info
)

HSIMPLY_DIR = os.path.join(os.path.dirname(__file__), "..", "hsimply")


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


def print_json_file(path, max_lines=30):
    """Print a JSON file with truncation."""
    if not os.path.exists(path):
        print(f"  File not found: {path}")
        return
    
    with open(path, 'r') as f:
        lines = f.readlines()
    
    print(f"  ({len(lines)} lines)")
    for i, line in enumerate(lines[:max_lines]):
        print(f"    {line.rstrip()}")
    
    if len(lines) > max_lines:
        print(f"    ... ({len(lines) - max_lines} more lines)")


def verify_capture(output_dir, entry_name):
    """Verify that all expected files were created."""
    expected_files = {
        "ast": f"{entry_name}.json",
        "params": f"{entry_name}_params.json",
        "manifest": "manifest.json"
    }
    
    results = {}
    print(f"\n  Verifying output in {output_dir}:")
    
    for key, filename in expected_files.items():
        path = os.path.join(output_dir, filename)
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        results[key] = {"exists": exists, "path": path, "size": size}
        status = "✓" if exists else "✗"
        print(f"    {status} {filename}: {size} bytes")
    
    return results


def show_params_summary(params_path):
    """Show a summary of captured parameters."""
    with open(params_path, 'r') as f:
        data = json.load(f)
    
    print(f"\n  Parameter Summary:")
    print(f"    Function: {data['invocation']['function']}")
    print(f"    Module: {data['invocation']['module']}")
    print(f"    Timestamp: {data['invocation']['timestamp']}")
    
    if 'args' in data:
        print(f"    Positional args: {len(data['args'])}")
        for i, arg in enumerate(data['args']):
            print(f"      [{i}] type={arg.get('type', 'unknown')}")
    
    if 'kwargs' in data:
        print(f"    Keyword args: {len(data['kwargs'])}")


def main_runner():
    parser = argparse.ArgumentParser(
        description='Run entry-point based DSL examples'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Print full output'
    )
    parser.add_argument(
        '--show-files',
        action='store_true',
        help='Show contents of generated files'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Entry-Point Based DSL Pipeline")
    print("=" * 70)
    
    # ========================================================================
    # Example 1: Main Model Entry Point
    # ========================================================================
    print("\n" + "=" * 70)
    print("Example 1: Bayesian Linear Regression (main)")
    print("=" * 70)
    
    # Define external data (from Python world)
    training_data = {
        "x": [1.0, 2.0, 3.0, 4.0, 5.0],
        "y": [2.1, 3.9, 5.8, 8.1, 10.2]
    }
    
    model_config = {
        "prior_scale": 1.0,
        "model_name": "simple_linear"
    }
    
    inference_hp = {
        "algorithm": "SVI",
        "n_iterations": 1000,
        "learning_rate": 0.01
    }
    
    print("\n  Calling main() with parameters:")
    print(f"    Data: {len(training_data['x'])} observations")
    print(f"    Config: {model_config}")
    print(f"    Hyperparams: {inference_hp}")
    
    # Call the entry point - this triggers capture
    result = main(training_data, model_config, inference_hp)
    
    print(f"\n  Result:")
    print(f"    Sampled params: {result['params']}")
    print(f"    Data summary: {result['data_summary']}")
    
    # Get run info
    run_info = get_run_info()
    print(f"\n  Capture Info:")
    print(f"    Output dir: {run_info['output_dir']}")
    print(f"    AST file: {os.path.basename(run_info['ast_file'])}")
    print(f"    Params file: {os.path.basename(run_info['params_file'])}")
    
    # Verify files
    verify_results = verify_capture(run_info['output_dir'], 'main')
    
    # Show parameter summary
    if verify_results['params']['exists']:
        show_params_summary(verify_results['params']['path'])
    
    # Parse with Haskell
    if verify_results['ast']['exists']:
        print(f"\n  Parsing AST with hsimply-exe...")
        haskell_output = run_hsimply(verify_results['ast']['path'])
        
        if args.verbose:
            print(f"\n    Haskell output:")
            for line in haskell_output.split('\n')[:20]:
                print(f"      {line}")
        else:
            first_line = haskell_output.split('\n')[0] if haskell_output else "No output"
            print(f"    {first_line}")
    
    # Show file contents if requested
    if args.show_files:
        print("\n  --- Generated Files ---")
        for key in ['ast', 'params', 'manifest']:
            if verify_results[key]['exists']:
                print(f"\n  {os.path.basename(verify_results[key]['path'])}:")
                print_json_file(verify_results[key]['path'])
    
    # ========================================================================
    # Example 2: Guide Entry Point
    # ========================================================================
    print("\n" + "=" * 70)
    print("Example 2: Variational Guide (guide_main)")
    print("=" * 70)
    
    guide_result = guide_main(training_data, model_config, inference_hp)
    
    print(f"\n  Guide result:")
    print(f"    Variational params: {list(guide_result['variational_params'].keys())}")
    
    run_info_guide = get_run_info()
    verify_capture(run_info_guide['output_dir'], 'guide_main')
    
    # ========================================================================
    # Example 3: Prediction Entry Point
    # ========================================================================
    print("\n" + "=" * 70)
    print("Example 3: Prediction (predict_main)")
    print("=" * 70)
    
    # Use the params from the main run
    model_params = result['params']
    new_data = [6.0, 7.0, 8.0]
    
    print(f"\n  Predicting for: {new_data}")
    print(f"  Using params: {model_params}")
    
    predict_result = predict_main(model_params, new_data, model_config)
    
    print(f"\n  Predictions:")
    for i, (x, pred, unc) in enumerate(zip(
        predict_result['inputs'],
        predict_result['predictions'],
        predict_result['uncertainties']
    )):
        print(f"    x={x:.1f} -> y={pred:.2f} ± {unc:.2f}")
    
    run_info_pred = get_run_info()
    verify_capture(run_info_pred['output_dir'], 'predict_main')
    
    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    print("\n  Entry points executed:")
    print("    1. main() - Model definition with priors and likelihood")
    print("    2. guide_main() - Variational guide")
    print("    3. predict_main() - Prediction with trained model")
    
    print("\n  Captured traces:")
    for name in ENTRY_TRACE:
        print(f"    - {name}")
    
    print("\n  Output structure:")
    output_base = os.path.join(os.path.dirname(__file__), "output", "bayesian_run")
    print(f"    {output_base}/")
    for f in sorted(os.listdir(output_base)):
        size = os.path.getsize(os.path.join(output_base, f))
        print(f"      {f} ({size} bytes)")
    
    print("\n" + "=" * 70)
    print("Pipeline completed!")
    print("=" * 70)
    print(f"\n  Next steps:")
    print(f"    - Examine output files in: {output_base}")
    print(f"    - Load main.json + main_params.json in Haskell")
    print(f"    - Execute the AST with the concrete parameters")


if __name__ == "__main__":
    main_runner()
