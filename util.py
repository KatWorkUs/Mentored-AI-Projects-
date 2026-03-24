from sklearn.preprocessing import FunctionTransformer
from scipy.stats import skew
import numpy as np

def severity_label(mag, sig):
    if mag >= 8.5 or (mag >= 8.0 and sig > 2000):
        return "Catastrophic"
    elif mag >= 7.5 or sig > 1500:
        return "Extreme"
    elif mag >= 6.9:
        return "Major"
    else:
        return "Moderate"
    
def log_transform1(x):
  x = x.copy()
  for column in range(x.shape[1]):
    if abs(skew(x[:,column])) > 1:
      x[:,column] = np.log1p(x[:,column])
  return x
log_transformer = FunctionTransformer(log_transform1)

