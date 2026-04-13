"""
Bayesian Linear Regression Example

This example demonstrates a complete Bayesian inference workflow using
Variational Inference (VI). The model represents:

    y = w * x + b + epsilon,  epsilon ~ Normal(0, sigma)

with priors:
    w ~ Normal(0, 1)
    b ~ Normal(0, 1)  
    sigma ~ Gamma(1, 1)

The guide uses mean-field variational approximation with independent
Normal distributions for each latent variable.
"""

import sys
import os

# Allow importing `simply` from the parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from simply.trace import make_tracer
from pyro_dsl import sample, param, plate, Normal, Gamma

# Create an isolated tracer for this module
trace, REGRESSION_TRACE = make_tracer()


@trace
def model(X, y):
    """
    Bayesian Linear Regression Model (1D for simplicity).
    
    Mathematical model:
        w ~ Normal(0, 1)                    # Prior on weight
        b ~ Normal(0, 1)                    # Prior on bias
        sigma ~ Gamma(1, 1)                 # Prior on noise
        
        For each observation i:
            y[i] ~ Normal(X[i] * w + b, sigma)   # Likelihood
    
    Args:
        X: Input features (1D array of shape [n])
        y: Target values (array of shape [n])
    
    Returns:
        Tuple of (w, b, sigma) - the latent variables
    """
    # Sample from priors
    w = sample("w", Normal(0.0, 1.0))
    b = sample("b", Normal(0.0, 1.0))
    sigma = sample("sigma", Gamma(1.0, 1.0))
    
    # Likelihood: observe data
    for i in plate("data", len(y)):
        mean = X[i] * w + b
        sample("obs_{}".format(i), Normal(mean, sigma), obs=y[i])
    
    return w, b, sigma


@trace
def guide(X, y):
    """
    Variational Guide for Bayesian Linear Regression.
    
    Uses mean-field approximation where each latent variable
    has its own independent variational distribution:
    
        q(w) = Normal(w_loc, w_scale)
        q(b) = Normal(b_loc, b_scale)  
        q(sigma) = Normal(sigma_loc, sigma_scale)  # simplified
    
    Args:
        X: Input features (not used in guide, kept for API consistency)
        y: Target values (not used in guide, kept for API consistency)
    
    Returns:
        Tuple of variational parameters (w_loc, b_loc, sigma_loc)
    """
    # Variational parameters for weight w
    w_loc = param("w_loc", 0.0)
    w_scale = param("w_scale", 1.0)
    sample("w", Normal(w_loc, w_scale))
    
    # Variational parameters for bias b
    b_loc = param("b_loc", 0.0)
    b_scale = param("b_scale", 1.0)
    sample("b", Normal(b_loc, b_scale))
    
    # Variational parameters for noise sigma
    # In practice, would use Softplus transform for positivity
    sigma_loc = param("sigma_loc", 1.0)
    sigma_scale = param("sigma_scale", 0.5)
    sample("sigma", Normal(sigma_loc, sigma_scale))
    
    # Empty plate to match model structure (required for SVI)
    for i in plate("data", len(y)):
        pass
    
    return w_loc, b_loc, sigma_loc


@trace
def model_multi_feature(X, y):
    """
    Multi-feature Bayesian Linear Regression.
    
    Extends the 1D case to handle multiple input features.
    
    Mathematical model:
        w[j] ~ Normal(0, 1) for each feature j
        b ~ Normal(0, 1)
        sigma ~ Gamma(1, 1)
        
        For each observation i:
            y[i] ~ Normal(sum_j X[i,j] * w[j] + b, sigma)
    
    Args:
        X: Input features (2D array of shape [n, d])
        y: Target values (array of shape [n])
    
    Returns:
        Tuple of (weights, bias, sigma)
    """
    n_features = len(X[0]) if len(X) > 0 else 0
    
    # Sample weights for each feature
    for j in range(n_features):
        sample("w_{}".format(j), Normal(0.0, 1.0))
    
    # Sample bias and noise
    b = sample("b", Normal(0.0, 1.0))
    sigma = sample("sigma", Gamma(1.0, 1.0))
    
    # Likelihood
    for i in plate("data", len(y)):
        # Linear combination: X[i] @ w + b
        linear = b
        for j in range(n_features):
            linear = linear + X[i][j] * sample("w_{}".format(j), Normal(0.0, 1.0))
        sample("obs_{}".format(i), Normal(linear, sigma), obs=y[i])
    
    return n_features, b, sigma


@trace
def guide_multi_feature(X, y):
    """
    Variational Guide for multi-feature regression.
    
    Args:
        X: Input features
        y: Target values
    
    Returns:
        Variational parameters
    """
    n_features = len(X[0]) if len(X) > 0 else 0
    
    # Variational parameters for each weight
    for j in range(n_features):
        w_loc = param("w_{}_loc".format(j), 0.0)
        w_scale = param("w_{}_scale".format(j), 1.0)
        sample("w_{}".format(j), Normal(w_loc, w_scale))
    
    # Bias variational parameters
    b_loc = param("b_loc", 0.0)
    b_scale = param("b_scale", 1.0)
    sample("b", Normal(b_loc, b_scale))
    
    # Sigma variational parameters
    sigma_loc = param("sigma_loc", 1.0)
    sigma_scale = param("sigma_scale", 0.5)
    sample("sigma", Normal(sigma_loc, sigma_scale))
    
    # Match plate structure
    for i in plate("data", len(y)):
        pass
    
    return n_features, b_loc, sigma_loc
