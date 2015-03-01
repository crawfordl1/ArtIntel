'''
Created on Jan 29, 2015

@author: Wastedyu6

TOPIC: Basic Gaussian Function defined
'''
from math import *

class MyClass(object):
    
    def f(mu, sigma2, x):
        return 1/sqrt(2.*pi*sigma2) * exp(-.5*(x-mu)**2 / sigma2)

    print f(10.,4.,10.)