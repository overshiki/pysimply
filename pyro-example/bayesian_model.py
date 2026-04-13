"""
Bayesian Linear Regression with Entry-Point Design (Complete Tracing)

This example demonstrates the complete entry-point based DSL architecture:
- Entry points use @trace_cap: capture AST + serialize external parameters
- Internal functions use @trace: capture AST only
- All functions go to PROGRAM_TRACE for Haskell compilation

Model:
    y = w * x + b + ε,  where ε ~ Normal(0, sigma)

Priors:
    w ~ Normal(0, prior_scale)
    b ~ Normal(0, 1)
    sigma ~ Gamma(1, 1)
"""

import sys
import os

# Allow importing `simply` from the parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from simply.trace import trace_and_trace_cap
from pyro_dsl import sample, param, plate, Normal, Gamma

# Create the complete tracer with both @trace_cap and @trace
trace_cap, trace, PROGRAM_TRACE, get_run_info = trace_and_trace_cap(
    output_dir=os.path.join(os.path.dirname(__file__), "output", "bayesian_complete")
)


# ============================================================================
# Internal Functions (use @trace - AST only, no parameter capture)
# These are called from entry points and their inputs come from internal flow
# ============================================================================

@trace
def sample_priors(config):
    """
    Sample model parameters from prior distributions.
    
    Internal function - inputs come from entry point (config),
    not directly from external Python world.
    
    Args:
        config: Dictionary with keys:
            - prior_scale: Scale for weight prior (default: 1.0)
    
    Returns:
        Dictionary with sampled parameters {w, b, sigma}
    """
    prior_scale = config.get("prior_scale", 1.0)
    
    w = sample("w", Normal(0.0, prior_scale))
    b = sample("b", Normal(0.0, 1.0))
    sigma = sample("sigma", Gamma(1.0, 1.0))
    
    return {"w": w, "b": b, "sigma": sigma}


@trace
def linear_predict(x, params):
    """
    Compute linear prediction: y = w * x + b
    
    Internal function - pure computation.
    
    Args:
        x: Input value(s)
        params: Dictionary with 'w' and 'b'
    
    Returns:
        Predicted value
    """
    return x * params["w"] + params["b"]


@trace
def build_likelihood(params, data):
    """
    Build the likelihood by observing data.
    
    Internal function - inputs come from entry point flow.
    
    Args:
        params: Dictionary with {w, b, sigma}
        data: Dictionary with keys:
            - x: List of input values
            - y: List of observed output values
    
    Returns:
        The params dictionary (unchanged)
    """
    x_vals = data["x"]
    y_vals = data["y"]
    sigma = params["sigma"]
    
    for i in plate("observations", len(x_vals)):
        mean = linear_predict(x_vals[i], params)
        sample("y_{}".format(i), Normal(mean, sigma), obs=y_vals[i])
    
    return params


@trace
def setup_variational_guide(config):
    """
    Setup variational parameters for the guide.
    
    Internal function for guide computation.
    
    Args:
        config: Model configuration
    
    Returns:
        Dictionary with variational parameter names and initial values
    """
    # Variational parameters for weight
    w_loc = param("w_loc", 0.0)
    w_scale = param("w_scale", 1.0)
    sample("w", Normal(w_loc, w_scale))
    
    # Variational parameters for bias
    b_loc = param("b_loc", 0.0)
    b_scale = param("b_scale", 1.0)
    sample("b", Normal(b_loc, b_scale))
    
    # Variational parameters for noise
    sigma_loc = param("sigma_loc", 1.0)
    sigma_scale = param("sigma_scale", 0.5)
    sample("sigma", Normal(sigma_loc, sigma_scale))
    
    return {
        "w": {"loc": w_loc, "scale": w_scale},
        "b": {"loc": b_loc, "scale": b_scale},
        "sigma": {"loc": sigma_loc, "scale": sigma_scale}
    }


@trace
def compute_data_summary(data):
    """
    Compute summary statistics of input data.
    
    Internal helper function.
    
    Args:
        data: Dictionary with 'x' and 'y' lists
    
    Returns:
        Dictionary with summary statistics
    """
    x_vals = data["x"]
    y_vals = data["y"]
    
    return {
        "n_observations": len(x_vals),
        "x_mean": sum(x_vals) / len(x_vals) if x_vals else 0,
        "y_mean": sum(y_vals) / len(y_vals) if y_vals else 0,
    }


# ============================================================================
# Entry Point Functions (use @trace_cap - AST + parameter capture)
# These receive external data from Python world
# ============================================================================

@trace_cap
def main(data, config, hyperparams):
    """
    Entry point for Bayesian linear regression.
    
    This is the main entry point - receives external data from Python world.
    When called, it:
    1. Serializes its arguments (data, config, hyperparams) to main_params.json
    2. Captures its AST to main.json
    3. Calls internal functions (sample_priors, build_likelihood, etc.)
    
    Args:
        data: Training data dictionary with:
            - x: List of input values (e.g., [1.0, 2.0, 3.0])
            - y: List of output values (e.g., [2.1, 3.9, 5.8])
        
        config: Model configuration dictionary with:
            - prior_scale: Scale for weight prior (default: 1.0)
            - model_name: Optional name for the model
        
        hyperparams: Inference hyperparameters with:
            - algorithm: Inference algorithm (e.g., "SVI", "NUTS")
            - n_iterations: Number of iterations
            - learning_rate: Learning rate for optimization
    
    Returns:
        Dictionary with:
            - params: Sampled/optimized parameters
            - config: Model configuration
            - hyperparams: Inference hyperparameters
            - data_summary: Summary statistics of input data
    """
    # Validate inputs
    if "x" not in data or "y" not in data:
        raise ValueError("Data must contain 'x' and 'y' keys")
    
    if len(data["x"]) != len(data["y"]):
        raise ValueError("x and y must have same length")
    
    # Set defaults
    config = config or {}
    hyperparams = hyperparams or {}
    
    # Sample from priors (calls internal function)
    params = sample_priors(config)
    
    # Build likelihood (calls internal function)
    build_likelihood(params, data)
    
    # Compute summary (calls internal function)
    data_summary = compute_data_summary(data)
    
    return {
        "params": params,
        "config": config,
        "hyperparams": hyperparams,
        "data_summary": data_summary
    }


@trace_cap
def guide_main(data, config, hyperparams):
    """
    Entry point for the variational guide.
    
    This guide mirrors the model structure but with variational
    distributions instead of priors.
    
    Args:
        data: Training data (same format as main)
        config: Model configuration
        hyperparams: Inference hyperparameters
    
    Returns:
        Dictionary with variational parameters
    """
    config = config or {}
    hyperparams = hyperparams or {}
    
    # Setup variational distributions (calls internal function)
    var_params = setup_variational_guide(config)
    
    # Match model structure (empty plate - just for structure)
    for i in plate("observations", len(data.get("x", []))):
        pass
    
    return {
        "variational_params": var_params,
        "config": config,
        "hyperparams": hyperparams
    }


@trace_cap  
def predict_main(model_params, new_x, config):
    """
    Entry point for prediction with a trained model.
    
    Args:
        model_params: Trained model parameters {w, b, sigma}
        new_x: List of new input values to predict
        config: Model configuration
    
    Returns:
        Dictionary with predictions and uncertainties
    """
    predictions = []
    uncertainties = []
    
    for x in new_x:
        pred = linear_predict(x, model_params)
        predictions.append(pred)
        # Uncertainty comes from sigma
        uncertainties.append(model_params.get("sigma", 1.0))
    
    return {
        "inputs": new_x,
        "predictions": predictions,
        "uncertainties": uncertainties,
        "config": config
    }
