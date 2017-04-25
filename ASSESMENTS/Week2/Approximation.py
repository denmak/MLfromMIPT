import numpy as np
import scipy as sc
import re
from numpy.linalg import norm
import matplotlib.pyplot as plt



def fn(x):
	return np.sin(x / 5.0) * np.exp(x / 10.0) + 5 * np.exp(-x / 2)

x=1.0
f0= fn(x)
print f0
x=15
f1= fn(x)
print f1

xs = np.linespace(1,15,10)
plt.plot(xs,fn(xs))

#-----------------------------------------------------------------------------------------------




