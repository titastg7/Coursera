# build-in Modules
import sys
locations = sys.path
print(locations)
for i in locations :
    print(i)

import calendar

print (calendar.leapdays(2000,2050))
print (calendar.isleap(2036))

import numpy

# Importing entire module
#import math

#print("Importing the math module")
#print(math.sqrt(9))

# Importing only required function from module
from math import sqrt

print("Importing only required from math module")
print(sqrt(9))

# Importing module and using alias
import math as m

print("Importing math module and using alias")
print(m.cos(0))


# Importing only required function and d using alias
from math import factorial as f, log10, sqrt

print("Using alias for methods")
print(f(5))

x = log10(50)
print(x)

# import all methods for a module
# from math import *


# Reload, reload modules multiple times

from importlib import reload
import sample

reload(sample)
reload(sample)
reload(sample)
