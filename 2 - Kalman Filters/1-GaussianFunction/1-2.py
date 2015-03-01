'''
Created on Jan 29, 2015

@author: Wastedyu6

TOPIC: Calculate POSTERIOR Distribution provided Measurement Gaussian Function
'''
from math import *

class MyClass(object):
    
    '''### UPDATE() FUNCTION ###
    -Purpose: Calculate POSTERIOR Distribution given the Posterior and Measurement Probabilities
    -Input: 
        -priorM - Mean of PRIOR Probability Distribution
        -priorV -Variance of PRIOR Probability Distribution
        -measureM - Mean of MEASUREMENT Distribution
        -measureV- Variance of MEASUREMENT Distribution
    -Output: 
        -postM - Mean of POSTERIOR Probability Distribution
        -postV - Variance of POSTERIOR Probability Distribution
    '''
    def update(priorM, priorV, measureM, measureV):
        postM = (((measureV * priorM) + (priorV * measureM))/ (priorV + measureV))
        postV = (1 / ((1 / measureV) + (1 / priorV)))
        return [postM, postV]

    print update(10.,8.,13., 2.)