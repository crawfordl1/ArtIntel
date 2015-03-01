'''
Created on Jan 29, 2015

@author: Wastedyu6

TOPIC: Calculate POSTERIOR Distribution provided Motion Gaussian Function
'''
from math import *

class MyClass(object):
    
    '''### PREDICT() FUNCTION ###
    -Purpose: Calculate POSTERIOR Distribution given the Posterior and Motion Probabilities
    -Input: 
        -priorM - Mean of PRIOR Probability Distribution
        -priorV -Variance of PRIOR Probability Distribution
        -motionM - Mean of MOTION Distribution
        -motionV- Variance of MOTION Distribution
    -Output: 
        -postM - Mean of POSTERIOR Probability Distribution
        -postV - Variance of POSTERIOR Probability Distribution
    '''
    def predict(priorM, priorV, motionM, motionV):
        postM = priorM + motionM
        postV = priorV + motionV
        return [postM, postV]

    print predict(10., 4., 12., 4.)