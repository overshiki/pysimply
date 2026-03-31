# pyro-example

An end-to-end demonstration of the **Python `simply` → JSON → Haskell `hsimply`** pipeline using a tiny **Pyro-like** probabilistic programming DSL.

## What it does

1. **DSL (`pyro_dsl.py`)** — Defines stub versions of `pyro.sample`, `pyro.param`, `pyro.plate`, and distributions (`Normal`, `Bernoulli`, `Categorical`). They are no-ops that provide valid Python syntax.
2. **Model (`model.py`)** — Writes `model` and `guide` functions in Pyro style and decorates them with `@trace` from `simply.trace`. This captures their ASTs at import time.
3. **Runner (`run.py`)** — Serializes the captured ASTs to JSON and invokes the `hsimply-exe` executable via `cabal run` to parse them into Haskell data structures.

## DSL Syntax

The `pyro_dsl.py` module provides a minimal subset of [Pyro](https://docs.pyro.ai/) primitives for writing probabilistic models. These are pure-Python stubs that enable AST capture without requiring PyTorch or the full Pyro library.

### Distributions

| Class | Constructor | Description |
|-------|-------------|-------------|
| `Normal` | `Normal(loc, scale)` | Normal (Gaussian) distribution with mean `loc` and standard deviation `scale` |
| `Bernoulli` | `Bernoulli(probs)` | Bernoulli distribution with success probability `probs` |
| `Categorical` | `Categorical(probs)` | Categorical distribution with class probabilities `probs` |

### Effect Handlers

| Function | Signature | Description |
|----------|-----------|-------------|
| `sample` | `sample(name, fn, obs=None)` | Draw a sample from distribution `fn` with unique identifier `name`. If `obs` is provided, the sample is observed (conditioned on data). |
| `param` | `param(name, init_value=None, constraint=None)` | Declare a learnable parameter with name `name` and initial value `init_value`. |
| `plate` | `plate(name, size, subsample_size=None)` | Declare a vectorized plate (independent observations) of size `size`. Returns an iterable over `range(size)`. |
| `module` | `module(name, nn_module, update_params=None)` | Register a neural network module (placeholder). |

### Example Model

```python
from simply.trace import trace
from pyro_dsl import sample, param, plate, Normal

@trace
def model(data):
    # Prior: sample latent variable from standard normal
    alpha = sample("alpha", Normal(0.0, 1.0))
    
    # Learnable parameter
    beta = param("beta", 0.0)
    
    # Observation plate: vectorized over data
    for i in plate("data", len(data)):
        mean = alpha * data[i] + beta
        # Observed sample: conditioned on data[i]
        sample("obs_{}".format(i), Normal(mean, 1.0), obs=data[i])
    
    return alpha + beta

@trace
def guide(data):
    # Variational parameters
    alpha_loc = param("alpha_loc", 0.0)
    alpha_scale = param("alpha_scale", 1.0)
    
    # Approximate posterior for alpha
    sample("alpha", Normal(alpha_loc, alpha_scale))
    
    # Same plate structure as model
    for i in plate("data", len(data)):
        pass  # No additional latent variables per observation
    
    return alpha_loc
```

Key features demonstrated:
- **Latent variables**: `alpha` sampled from a prior in the model and from a variational distribution in the guide.
- **Learnable parameters**: `beta` in the model; `alpha_loc`, `alpha_scale` in the guide.
- **Observations**: The `obs=` keyword conditions the model on observed data.
- **Plates**: `plate("data", len(data))` marks independent observations (i.i.d. data).
- **String formatting**: Dynamic site names like `"obs_{}".format(i)` for plate indexing.

## Files

| File | Description |
|------|-------------|
| `pyro_dsl.py` | Stub implementations of Pyro primitives |
| `model.py` | Example `model` / `guide` with `@trace` |
| `run.py` | Pipeline script: Python AST → JSON → Haskell AST |
| `output/` | Generated JSON files (created automatically) |

## Running

From the **repository root**:

```bash
python pyro-example/run.py
```

Expected output:

```
Wrote AST for 'model' -> pyro-example/output/model.json
Wrote AST for 'guide' -> pyro-example/output/guide.json

=== Haskell parse of 'model' ===
Successfully parsed Module:
Module {moduleBody = [FunctionDef (Identifier "model") ...

=== Haskell parse of 'guide' ===
Successfully parsed Module:
Module {moduleBody = [FunctionDef (Identifier "guide") ...

=== Running Python stubs ===
model([1.0, 2.0, 3.0]) = ...
guide([1.0, 2.0, 3.0]) = ...
```

## Notes

- The DSL stubs do **not** perform inference; they only exist so `simply` can parse the Python source into an AST.
- `simply.trace` recompiles the original function, so calling `model(data)` in Python still works (it just runs the stubs).
- The captured AST includes Pyro primitives (`sample`, `param`, `plate`) as regular Python calls, allowing downstream tools to recognize and transform them.
