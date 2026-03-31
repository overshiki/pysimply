"""
Minimal Pyro-like DSL stubs for AST capture.

These classes and functions provide valid Python syntax so that `simply`
can parse model/guide code without requiring the real Pyro / PyTorch stack.
"""

class Distribution:
    pass

class Normal(Distribution):
    def __init__(self, loc, scale):
        self.loc = loc
        self.scale = scale

class Bernoulli(Distribution):
    def __init__(self, probs):
        self.probs = probs

class Categorical(Distribution):
    def __init__(self, probs):
        self.probs = probs

class plate:
    """pyro.plate placeholder — iterable over range(size)."""
    def __init__(self, name, size, subsample_size=None):
        self.name = name
        self.size = size
        self.subsample_size = subsample_size

    def __iter__(self):
        return iter(range(self.size))

def sample(name, fn, obs=None):
    """pyro.sample placeholder — returns a dummy numeric value."""
    return 0.0

def param(name, init_value=None, constraint=None):
    """pyro.param placeholder."""
    return init_value

def module(name, nn_module, update_params=None):
    """pyro.module placeholder."""
    return nn_module
