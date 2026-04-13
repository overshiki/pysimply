"""
Gaussian Mixture Model (GMM) Example

This example implements Bayesian inference for clustering using
a Gaussian Mixture Model with variational inference.

Model specification:
    K: Number of mixture components (fixed)
    pi ~ Dirichlet([alpha, ..., alpha])  # Mixture weights
    
    For each component k:
        mu[k] ~ Normal(0, 10)
        sigma[k] ~ Gamma(1, 1)
    
    For each data point i:
        z[i] ~ Categorical(pi)          # Latent assignment
        x[i] ~ Normal(mu[z[i]], sigma[z[i]])  # Observed data

The guide uses mean-field approximation with independent
variational distributions for global and local variables.
"""

import sys
import os

# Allow importing `simply` from the parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from simply.trace import make_tracer
from pyro_dsl import sample, param, plate, Normal, Gamma, Categorical, Delta

# Create an isolated tracer for this module
trace, GMM_TRACE = make_tracer()


@trace
def gmm_model(data, K=3):
    """
    Gaussian Mixture Model with latent assignments.
    
    This model clusters data into K Gaussian components by introducing
    latent categorical variables z[i] for each data point.
    
    Args:
        data: Observed data points (array of shape [n])
        K: Number of mixture components (default 3)
    
    Returns:
        Number of data points processed
    """
    # Global mixture weights (simplified uniform for this example)
    # In full version: pi = sample("pi", Dirichlet([1.0] * K))
    pi_weights = [1.0 / K] * K
    
    # Component parameters (global)
    for k in plate("components", K):
        sample("mu_{}".format(k), Normal(0.0, 10.0))
        sample("sigma_{}".format(k), Gamma(1.0, 1.0))
    
    # Local variables (per data point)
    for i in plate("data", len(data)):
        # Latent assignment: which component generated this point?
        z = sample("z_{}".format(i), Categorical(pi_weights))
        
        # Lookup component parameters based on assignment
        # Note: In real Pyro, would use Vindex or similar for indexing
        # Here we demonstrate the structure with explicit lookups
        mu = sample("mu_{}".format(z), Normal(0.0, 10.0))
        sigma = sample("sigma_{}".format(z), Gamma(1.0, 1.0))
        
        # Observation
        sample("obs_{}".format(i), Normal(mu, sigma), obs=data[i])
    
    return len(data)


@trace
def gmm_guide(data, K=3):
    """
    Variational Guide for GMM.
    
    Uses mean-field factorization:
    - Global parameters: independent Normals for each mu[k], sigma[k]
    - Local parameters: Categorical for each z[i]
    
    Args:
        data: Observed data points
        K: Number of mixture components
    
    Returns:
        Number of data points
    """
    # Variational parameters for component means
    for k in range(K):
        mu_loc = param("mu_{}_loc".format(k), 0.0)
        mu_scale = param("mu_{}_scale".format(k), 5.0)
        sample("mu_{}".format(k), Normal(mu_loc, mu_scale))
    
    # Variational parameters for component scales
    for k in range(K):
        sigma_loc = param("sigma_{}_loc".format(k), 1.0)
        sigma_scale = param("sigma_{}_scale".format(k), 0.5)
        sample("sigma_{}".format(k), Normal(sigma_loc, sigma_scale))
    
    # Variational parameters for local assignments
    # Each z[i] has a Categorical posterior over K components
    for i in plate("data", len(data)):
        # Simplified: use uniform assignment probabilities
        # In practice, would learn these from data
        assignment_probs = [1.0 / K] * K
        sample("z_{}".format(i), Categorical(assignment_probs))
    
    return len(data)


@trace
def gmm_collapsed_model(data, K=3):
    """
    Collapsed GMM (marginalizing out latent assignments).
    
    Instead of explicit z[i] variables, computes the marginal
    likelihood directly as a mixture.
    
    Mathematical model:
        p(x[i]) = sum_k pi[k] * Normal(x[i] | mu[k], sigma[k])
    
    This demonstrates a more efficient formulation when the
    latent assignments are not of direct interest.
    
    Args:
        data: Observed data points
        K: Number of components
    
    Returns:
        Number of data points
    """
    # Component parameters
    for k in plate("components", K):
        sample("mu_{}".format(k), Normal(0.0, 10.0))
        sample("sigma_{}".format(k), Gamma(1.0, 1.0))
    
    # Marginal likelihood for each data point
    # (simplified - real implementation would compute log-sum-exp)
    for i in plate("data", len(data)):
        # Placeholder for mixture observation
        # In real Pyro, would use Mixture or explicit log-sum-exp
        sample("obs_{}".format(i), Normal(0.0, 1.0), obs=data[i])
    
    return len(data)


@trace
def gmm_collapsed_guide(data, K=3):
    """
    Guide for collapsed GMM.
    
    Only needs to approximate posteriors over global parameters
    (mu[k], sigma[k]), since local variables are marginalized.
    
    Args:
        data: Observed data points
        K: Number of components
    
    Returns:
        Number of data points
    """
    # Variational parameters for component means
    for k in range(K):
        mu_loc = param("mu_{}_loc".format(k), 0.0)
        mu_scale = param("mu_{}_scale".format(k), 5.0)
        sample("mu_{}".format(k), Normal(mu_loc, mu_scale))
    
    # Variational parameters for component scales
    for k in range(K):
        sigma_loc = param("sigma_{}_loc".format(k), 1.0)
        sigma_scale = param("sigma_{}_scale".format(k), 0.5)
        sample("sigma_{}".format(k), Normal(sigma_loc, sigma_scale))
    
    # Empty plate for structure matching
    for i in plate("data", len(data)):
        pass
    
    return len(data)


@trace
def simple_clustering(data, K=2):
    """
    Simplified clustering model for demonstration.
    
    A minimal example showing the basic pattern of:
    - Global parameters (component centers)
    - Observations assigned to components
    
    Args:
        data: Data points to cluster
        K: Number of clusters
    
    Returns:
        Cluster centers (simplified)
    """
    # Global cluster centers
    for k in range(K):
        sample("center_{}".format(k), Normal(0.0, 5.0))
    
    # Assign each point to nearest center (simplified)
    for i in plate("data", len(data)):
        # For simplicity, assign all to center_0
        center = sample("center_0", Normal(0.0, 5.0))
        sample("obs_{}".format(i), Normal(center, 1.0), obs=data[i])
    
    return K


@trace
def simple_clustering_guide(data, K=2):
    """
    Guide for simple clustering.
    
    Args:
        data: Data points
        K: Number of clusters
    
    Returns:
        Variational parameters
    """
    for k in range(K):
        center_loc = param("center_{}_loc".format(k), 0.0)
        center_scale = param("center_{}_scale".format(k), 2.0)
        sample("center_{}".format(k), Normal(center_loc, center_scale))
    
    for i in plate("data", len(data)):
        pass
    
    return K
