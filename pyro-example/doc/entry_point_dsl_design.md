# Entry-Point Based DSL Design

## Overview

This document describes the architecture for a complete DSL system where:
- **Entry points** use `@trace_cap`: capture AST + serialize external parameters
- **Internal functions** use `@trace`: capture AST only
- **Haskell** receives the complete program (all ASTs) for compilation

## Key Design Principle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Python World                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Entry Point (@trace_cap)        Internal Functions (@trace)                 │
│  ┌─────────────────────┐         ┌──────────────────────────────────────┐   │
│  │ def main(data):     │         │ def sample_priors(config):           │   │
│  │   params = ...      │────────▶│   w = sample("w", Normal(0, 1))      │   │
│  │   build_likelihood  │────────▶│   return params                      │   │
│  │   return result     │         │                                      │   │
│  └─────────────────────┘         │ def build_likelihood(params, data):  │   │
│           │                      │   for i in plate(...):               │   │
│           │                      │     sample(...)                      │   │
│           ▼                      └──────────────────────────────────────┘   │
│  ┌─────────────────────┐                                                    │
│  │ main.json (AST)     │                                                    │
│  │ main_params.json    │  ◄── External data from Python world             │
│  └─────────────────────┘                                                    │
│                                                                              │
│  ┌─────────────────────┐                                                    │
│  │ sample_priors.json  │  ◄── AST only (no external params)               │
│  │ build_likelihood.j  │                                                    │
│  └─────────────────────┘                                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             Haskell World                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Load ALL AST files (complete program structure)                          │
│     ├── main.json                 (entry point)                              │
│     ├── sample_priors.json        (internal)                                 │
│     ├── build_likelihood.json     (internal)                                 │
│     └── ...                                                                  │
│                                                                              │
│  2. Load entry point parameters                                              │
│     └── main_params.json          (external data: data, config, hyperparams) │
│                                                                              │
│  3. Execute/Compile                                                          │
│     └── Run main with concrete parameters                                    │
│         └── Trace through all sample sites                                   │
│             └── Can compile to LLVM/GPU/etc.                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Why Two Decorators?

### `@trace_cap` - For Entry Points

```python
trace_cap, trace, PROGRAM_TRACE, get_run_info = trace_and_trace_cap("./output")

@trace_cap
def main(data, config, hyperparams):
    """
    Entry point receives EXTERNAL data from Python world.
    
    Captures:
    1. AST of this function
    2. Serialized parameters (data, config, hyperparams) to main_params.json
    """
    params = sample_priors(config)  # Call internal function
    build_likelihood(params, data)   # Call internal function
    return params
```

**Characteristics:**
- Receives data from outside the DSL (Python world)
- Parameters are serialized to JSON
- Triggered at runtime (when function is called)
- Creates: `{name}.json` + `{name}_params.json`

### `@trace` - For Internal Functions

```python
@trace
def sample_priors(config):
    """
    Internal function receives INTERNAL data from computation flow.
    
    Captures:
    1. AST of this function
    2. NO parameter serialization (inputs come from other functions)
    """
    w = sample("w", Normal(0.0, 1.0))
    b = sample("b", Normal(0.0, 1.0))
    return {"w": w, "b": b}
```

**Characteristics:**
- Inputs come from other DSL functions (internal flow)
- No external parameters to serialize
- Captured at import time
- Creates: `{name}.json` only

## Complete Example

```python
# bayesian_model.py
from simply.trace import trace_and_trace_cap
from pyro_dsl import sample, param, plate, Normal, Gamma

# Create the tracer system
trace_cap, trace, PROGRAM_TRACE, get_run_info = trace_and_trace_cap(
    output_dir="./output/bayesian_run"
)

# ============================================================================
# Internal Functions (@trace - AST only)
# ============================================================================

@trace
def sample_priors(config):
    """Sample from prior distributions."""
    prior_scale = config.get("prior_scale", 1.0)
    w = sample("w", Normal(0.0, prior_scale))
    b = sample("b", Normal(0.0, 1.0))
    sigma = sample("sigma", Gamma(1.0, 1.0))
    return {"w": w, "b": b, "sigma": sigma}


@trace
def build_likelihood(params, data):
    """Build likelihood by observing data."""
    for i in plate("observations", len(data["x"])):
        mean = params["w"] * data["x"][i] + params["b"]
        sample(f"y_{i}", Normal(mean, params["sigma"]), obs=data["y"][i])


@trace
def compute_summary(data):
    """Compute data summary statistics."""
    return {
        "n": len(data["x"]),
        "x_mean": sum(data["x"]) / len(data["x"])
    }


# ============================================================================
# Entry Point (@trace_cap - AST + parameters)
# ============================================================================

@trace_cap
def main(data, config, hyperparams):
    """
    Main entry point - receives external data from Python world.
    
    When called:
    1. Serializes (data, config, hyperparams) to main_params.json
    2. Captures AST to main.json
    3. Executes with stubs
    """
    # Sample priors (calls internal function)
    params = sample_priors(config)
    
    # Build likelihood (calls internal function)
    build_likelihood(params, data)
    
    # Compute summary (calls internal function)
    summary = compute_summary(data)
    
    return {"params": params, "summary": summary}
```

## Output Files

After calling `main(training_data, model_config, inference_hp)`:

```
./output/bayesian_run/
├── main.json                   # Entry point AST
├── main_params.json            # External parameters
├── sample_priors.json          # Internal function AST
├── build_likelihood.json       # Internal function AST
├── compute_summary.json        # Internal function AST
└── manifest.json               # Metadata
```

### main_params.json Structure

```json
{
  "invocation": {
    "function": "main",
    "module": "bayesian_model",
    "timestamp": "2024-01-15T10:30:00"
  },
  "args": [
    {
      "type": "dict",
      "values": {
        "x": {"type": "list", "length": 100, "element_type": "float", ...},
        "y": {"type": "list", "length": 100, "element_type": "float", ...}
      }
    },
    {
      "type": "dict",
      "values": {"prior_scale": {"type": "float", "value": 1.0}}
    },
    {
      "type": "dict",
      "values": {"algorithm": {"type": "str", "value": "SVI"}}
    }
  ],
  "arg_names": ["data", "config", "hyperparams"],
  "kwargs": {}
}
```

## Data Flow

### In Python (Runtime)

```
Python Data (external)
    │
    ▼
┌─────────────┐
│ main(data)  │  ◄── External data enters here
└──────┬──────┘
       │
       ├──► sample_priors(config)  ◄── Internal flow
       │           └── sample("w", ...)
       │
       └──► build_likelihood(params, data)
                   └── plate(...)
                       └── sample("y_i", ...)
```

### In Haskell (Reconstruction)

```
Load main.json + main_params.json
    │
    ▼
Execute main with concrete data
    │
    ├──► Interpret sample_priors
    │           └── Record sample site "w"
    │
    └──► Interpret build_likelihood
                └── Enter plate context
                    └── Record sample site "y_i" (with obs value)
```

## Usage Pattern

```python
# 1. Import the model (captures all ASTs at import time)
from bayesian_model import main, PROGRAM_TRACE

# 2. Prepare external data (from Python world)
training_data = {"x": [1.0, 2.0, ...], "y": [2.1, 3.9, ...]}
model_config = {"prior_scale": 1.0}
inference_hp = {"algorithm": "SVI"}

# 3. Call entry point (captures parameters + executes)
result = main(training_data, model_config, inference_hp)

# 4. Check what was captured
print(f"Functions: {list(PROGRAM_TRACE.keys())}")
# ['main', 'sample_priors', 'build_likelihood', 'compute_summary']
```

## Benefits

### 1. Complete Program for Compilation

Haskell receives the full program structure:
- All function definitions (ASTs)
- Entry point signatures (parameter types)
- Complete call graph

This enables:
- Static analysis of the entire program
- Optimization passes
- Compilation to LLVM/GPU/etc.

### 2. Clear Data Boundaries

- **External data**: Explicit in entry point params
- **Internal data**: Computed during execution
- No confusion about what comes from where

### 3. Reproducibility

Same program (`*.json` files) + different inputs (`*_params.json`) = different runs:

```
Run 1: main.json + main_params_run1.json → Results A
Run 2: main.json + main_params_run2.json → Results B
```

### 4. Version Control Friendly

- AST files are deterministic (code)
- Param files are data (can be .gitignored)

## API Reference

### `trace_and_trace_cap(output_dir, indent=2)`

Creates a complete tracer system.

**Returns:**
- `trace_cap`: Decorator for entry points
- `trace`: Decorator for internal functions
- `program_trace`: Dict storing all captured ASTs
- `get_run_info`: Function to get last run info

### `trace_cap(func)`

Decorator for entry points.

**Behavior:**
- Captures AST at import time
- On call: serializes parameters + executes
- Creates `{name}.json` and `{name}_params.json`

### `trace(func)`

Decorator for internal functions.

**Behavior:**
- Captures AST at import time
- Creates `{name}.json` only
- No parameter serialization

## Comparison: Old vs New

### Old Design (make_tracer only)

```python
trace, LOCAL_TRACE = make_tracer()

@trace
def main(data): ...

@trace
def helper(x): ...

# All functions treated the same
# No parameter serialization
```

### New Design (trace_and_trace_cap)

```python
trace_cap, trace, PROGRAM_TRACE, _ = trace_and_trace_cap("./output")

@trace_cap
def main(data): ...  # Entry point

@trace
def helper(x): ...   # Internal

# Clear distinction between entry and internal
# Complete program capture for Haskell
```

## Migration Guide

### From `make_tracer()`

**Before:**
```python
from simply.trace import make_tracer
trace, TRACE = make_tracer()

@trace
def main(data): ...

@trace
def helper(x): ...
```

**After:**
```python
from simply.trace import trace_and_trace_cap
trace_cap, trace, TRACE, _ = trace_and_trace_cap("./output")

@trace_cap
def main(data): ...

@trace
def helper(x): ...
```

## Open Questions

1. **Multiple entry points**: Should they share the same output directory?
2. **Incremental capture**: Should internal functions overwrite or append?
3. **Call graph**: Should we explicitly capture the call graph?
4. **Type inference**: Can we infer types from parameter serialization?
