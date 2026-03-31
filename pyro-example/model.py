import sys
import os

# Allow importing `simply` from the parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from simply.trace import trace, GLOBAL_TRACE
from pyro_dsl import sample, param, plate, Normal, Bernoulli


@trace
def model(data):
    alpha = sample("alpha", Normal(0.0, 1.0))
    beta = param("beta", 0.0)

    for i in plate("data", len(data)):
        mean = alpha * data[i] + beta
        sample("obs_{}".format(i), Normal(mean, 1.0), obs=data[i])

    return alpha + beta


@trace
def guide(data):
    alpha_loc = param("alpha_loc", 0.0)
    alpha_scale = param("alpha_scale", 1.0)
    sample("alpha", Normal(alpha_loc, alpha_scale))

    for i in plate("data", len(data)):
        pass

    return alpha_loc
