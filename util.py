from sklearn.preprocessing import FunctionTransformer
from scipy.stats import skew
import numpy as np
import pandas as pd

def log_transform(x):
  x = x.copy()
  for column in range(x.shape[1]):
    if abs(skew(x[:,column])) > 1:
      x[:,column] = np.log1p(x[:,column])
  return x
log_transformer = FunctionTransformer(log_transform)

def output_pollution_source(x):
    mapping = {
        0: 'Vehicular',
        1: 'Industrial',
        2: 'Agricultural',
        3: 'Burning',
        4: 'Natural'
    }
    if isinstance(x, np.ndarray):
        return [mapping[i] for i in x]
    else:
        return mapping[x]

