"""
Pyro-like DSL stubs for AST capture.

These classes and functions provide valid Python syntax so that `simply`
can parse model/guide code without requiring the real Pyro / PyTorch stack.

This extended version supports realistic Bayesian inference examples including
Bayesian linear regression and Gaussian mixture models.
"""


class Distribution:
    """Base class for all probability distributions."""
    pass


class Normal(Distribution):
    """Normal (Gaussian) distribution.
    
    Args:
        loc: Mean of the distribution
        scale: Standard deviation (must be positive)
    """
    def __init__(self, loc, scale):
        self.loc = loc
        self.scale = scale


class Bernoulli(Distribution):
    """Bernoulli distribution for binary outcomes.
    
    Args:
        probs: Probability of success (value 1)
    """
    def __init__(self, probs):
        self.probs = probs


class Categorical(Distribution):
    """Categorical distribution over discrete classes.
    
    Args:
        probs: List/array of class probabilities (must sum to 1)
    """
    def __init__(self, probs):
        self.probs = probs


class Gamma(Distribution):
    """Gamma distribution for positive continuous variables.
    
    Commonly used as prior for precision (1/variance) or rate parameters.
    
    Args:
        concentration: Shape parameter (alpha)
        rate: Rate parameter (beta)
    """
    def __init__(self, concentration, rate):
        self.concentration = concentration
        self.rate = rate


class Delta(Distribution):
    """Degenerate distribution at a single point.
    
    Useful for point estimates or deterministic assignments.
    
    Args:
        v: The deterministic value
    """
    def __init__(self, v):
        self.v = v


class Uniform(Distribution):
    """Uniform distribution over a continuous interval.
    
    Args:
        low: Lower bound (inclusive)
        high: Upper bound (exclusive)
    """
    def __init__(self, low, high):
        self.low = low
        self.high = high


class Dirichlet(Distribution):
    """Dirichlet distribution over the simplex.
    
    Commonly used as prior for categorical/multinomial probabilities.
    
    Args:
        concentration: Concentration parameters (alpha vector)
    """
    def __init__(self, concentration):
        self.concentration = concentration


class Exponential(Distribution):
    """Exponential distribution for positive continuous variables.
    
    Args:
        rate: Rate parameter (lambda)
    """
    def __init__(self, rate):
        self.rate = rate


class plate:
    """Context manager for vectorized independent observations.
    
    In Pyro, plates mark conditional independence and enable
    vectorized computation. Here we provide a simple iterable.
    
    Args:
        name: Unique name for this plate context
        size: Number of elements in the plate
        subsample_size: Optional size for subsampling (not implemented)
    """
    def __init__(self, name, size, subsample_size=None):
        self.name = name
        self.size = size
        self.subsample_size = subsample_size

    def __iter__(self):
        return iter(range(self.size))


def sample(name, fn, obs=None):
    """Sample from a distribution or observe data.
    
    This is the core primitive of probabilistic programming.
    In the model: samples from the prior
    In the guide: samples from the variational posterior
    With obs: treats as observed data (likelihood term)
    
    Args:
        name: Unique site name for this sample
        fn: Distribution to sample from
        obs: If provided, this is observed data (not sampled)
    
    Returns:
        A sampled value (or obs if provided)
    """
    if obs is not None:
        return obs
    # Return dummy values based on distribution type
    if isinstance(fn, Normal):
        return fn.loc
    elif isinstance(fn, Gamma):
        return fn.concentration / fn.rate
    elif isinstance(fn, Delta):
        return fn.v
    elif isinstance(fn, Uniform):
        return (fn.low + fn.high) / 2
    elif isinstance(fn, Dirichlet):
        # Return uniform vector
        n = len(fn.concentration)
        return [1.0 / n] * n
    elif isinstance(fn, Exponential):
        return 1.0 / fn.rate
    elif isinstance(fn, Bernoulli):
        return fn.probs > 0.5
    elif isinstance(fn, Categorical):
        return 0  # Return first category
    return 0.0


def param(name, init_value=None, constraint=None):
    """Declare a learnable (optimizable) parameter.
    
    Used in the guide to define variational parameters.
    
    Args:
        name: Unique parameter name
        init_value: Initial value for optimization
        constraint: Optional constraint (e.g., positive, interval)
    
    Returns:
        The current parameter value
    """
    return init_value


def module(name, nn_module, update_params=None):
    """Register a neural network module.
    
    Args:
        name: Unique module name
        nn_module: Neural network module
        update_params: Optional parameter update function
    
    Returns:
        The registered module
    """
    return nn_module


def sample_obs(name, fn, obs):
    """Explicit observation syntax sugar.
    
    Equivalent to sample(name, fn, obs=obs) but makes the
    observation explicit in the code.
    """
    return sample(name, fn, obs=obs)
