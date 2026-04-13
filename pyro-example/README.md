# pyro-example: Bayesian Inference with pysimply

A complete end-to-end demonstration of the **Python `simply` → JSON → Haskell `hsimply`** pipeline for Bayesian inference.

## Overview

This example implements realistic Bayesian inference workflows using a Pyro-like probabilistic programming DSL. The captured ASTs can be transported to other languages (demonstrated with Haskell) for analysis, optimization, or code generation.

## Examples

### 1. Bayesian Linear Regression (`model_regression.py`)

A complete Variational Inference (VI) workflow for linear regression:

```
y = w * x + b + ε,  where ε ~ Normal(0, σ)

Priors:
  w ~ Normal(0, 1)
  b ~ Normal(0, 1)
  σ ~ Gamma(1, 1)
```

**Key Features:**
- **Model** (`model`): Defines priors and likelihood with observations
- **Guide** (`guide`): Mean-field variational approximation with learnable parameters
- **Multi-feature extension** (`model_multi_feature`): Handles multiple input features

### 2. Gaussian Mixture Model (`model_gmm.py`)

Clustering with a Bayesian GMM:

```
For each component k:
  μ[k] ~ Normal(0, 10)
  σ[k] ~ Gamma(1, 1)

For each data point i:
  z[i] ~ Categorical(π)           # Latent assignment
  x[i] ~ Normal(μ[z[i]], σ[z[i]]) # Observation
```

**Key Features:**
- **Standard GMM** (`gmm_model`/`gmm_guide`): With explicit latent assignments
- **Collapsed GMM** (`gmm_collapsed_model`): Marginalizing out local variables
- **Simple Clustering** (`simple_clustering`): Minimal demonstration

## DSL (`pyro_dsl.py`)

Extended Pyro-like primitives:

### Distributions

| Class | Constructor | Description |
|-------|-------------|-------------|
| `Normal` | `Normal(loc, scale)` | Gaussian distribution |
| `Gamma` | `Gamma(concentration, rate)` | For positive variables (e.g., precision) |
| `Delta` | `Delta(v)` | Degenerate distribution at point |
| `Uniform` | `Uniform(low, high)` | Uniform continuous distribution |
| `Dirichlet` | `Dirichlet(concentration)` | Distribution over simplex |
| `Exponential` | `Exponential(rate)` | For positive continuous variables |
| `Bernoulli` | `Bernoulli(probs)` | Binary outcomes |
| `Categorical` | `Categorical(probs)` | Discrete categories |

### Effect Handlers

| Function | Signature | Description |
|----------|-----------|-------------|
| `sample` | `sample(name, fn, obs=None)` | Sample from distribution or observe data |
| `param` | `param(name, init_value=None, constraint=None)` | Learnable variational parameter |
| `plate` | `plate(name, size)` | Vectorized independent observations |

## Running the Examples

### Prerequisites

The Haskell `hsimply-exe` executable must be built:

```bash
cd hsimply
cabal build
```

### Run All Examples

From the repository root:

```bash
python pyro-example/run.py
```

### Run Specific Examples

```bash
# Only regression examples
python pyro-example/run.py --model regression

# Only GMM examples
python pyro-example/run.py --model gmm
```

### Verbose Output

To see the full Haskell AST output:

```bash
python pyro-example/run.py --verbose
```

### Skip Python Execution

To skip running the Python stubs (faster):

```bash
python pyro-example/run.py --no-python
```

## Sample Output

```
============================================================
pysimply → JSON → hsimply Pipeline
Bayesian Inference Examples
============================================================

Captured 10 functions via @trace

============================================================
Processing: model
============================================================
  Wrote AST -> pyro-example/output/model.json
  Parsing with hsimply-exe...
  Success: Successfully parsed Module:

============================================================
Processing: guide
============================================================
  Wrote AST -> pyro-example/output/guide.json
  Parsing with hsimply-exe...
  Success: Successfully parsed Module:

... (more models)

============================================================
Summary
============================================================
Processed 10 models
Output directory: pyro-example/output
  - model.json
  - guide.json
  - model_multi_feature.json
  - guide_multi_feature.json
  - gmm_model.json
  - gmm_guide.json
  - gmm_collapsed_model.json
  - gmm_collapsed_guide.json
  - simple_clustering.json
  - simple_clustering_guide.json

============================================================
Python Stubs Execution (demonstrating valid Python)
============================================================

--- Bayesian Linear Regression (1D) ---
  Model returned: w=0.00, b=0.00, sigma=1.00
  Guide returned: w_loc=0.00, b_loc=0.00, sigma_loc=1.00

... (more executions)
```

## Pipeline Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Python DSL    │     │      JSON       │     │  Haskell AST    │
│  (@trace capture)│────▶│  (serialization)│────▶│  (hsimply parse)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

1. **Python DSL**: Write probabilistic models using Pyro-like syntax
2. **@trace Decorator**: Captures function ASTs at import time via `simply.trace`
3. **JSON Serialization**: Converts simply AST to tagged-union JSON format
4. **Haskell Parsing**: `hsimply-exe` reconstructs native Haskell AST

## Files

| File | Description |
|------|-------------|
| `pyro_dsl.py` | DSL stub implementations (distributions, sample, param, plate) |
| `model_regression.py` | Bayesian linear regression model + guide |
| `model_gmm.py` | Gaussian Mixture Model examples |
| `run.py` | Pipeline orchestration script |
| `output/` | Generated JSON files (created automatically) |

## Extending the DSL

To add a new distribution:

```python
class Beta(Distribution):
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
```

Then use it in models:

```python
@trace
def my_model(data):
    p = sample("p", Beta(1.0, 1.0))
    # ... rest of model
```

## Key Insights

1. **AST Capture**: The `@trace` decorator captures the decorated function's AST at import time, before any execution
2. **Executable Stubs**: The DSL functions are valid Python that can run (returning dummy values), enabling testing
3. **Round-trip**: The captured AST can be serialized to JSON, parsed in Haskell, and potentially transpiled to other languages
4. **Structure Matters**: Guide functions must match the plate structure of their corresponding models for VI to work

## Mathematical Background

### Variational Inference

VI approximates the posterior `p(z|x)` with a simpler distribution `q(z; λ)` by optimizing:

```
λ* = argmax ELBO(λ)
where ELBO = E_q[log p(x,z)] - E_q[log q(z;λ)]
```

The **model** defines `p(x,z)` (joint distribution), while the **guide** defines `q(z; λ)` (variational approximation).

### Mean-Field Approximation

The default guide uses mean-field factorization:

```
q(z; λ) = ∏_i q_i(z_i; λ_i)
```

Each latent variable has its own independent variational distribution.

## Notes

- The DSL stubs perform **no actual inference**; they only exist to provide valid Python syntax for AST capture
- Real inference would use Pyro/PyroNumPyro with optimizers and loss functions
- The captured AST preserves the probabilistic structure for downstream analysis
