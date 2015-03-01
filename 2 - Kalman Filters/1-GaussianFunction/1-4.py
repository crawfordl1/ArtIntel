'''
Created on Jan 29, 2015

@author: Wastedyu6

TOPIC: Calculate POSTERIOR Distribution
'''
from math import *

class MyClass(object):
    
    '''### CLASS VARIABLES ###
    '''
    measurements = [5., 6., 7., 9., 10.]
    motions = [1., 1., 2., 1., 1.]
    mu = 0.
    sig = 10000.
    
    #Measurement Uncertainty (Mu Constant)
    measurement_sig = 4.
    
    #Motion Uncertainty (Variance Constant)
    motions_sig = 2.
    
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
    '''
    -Create initial list as [mu, sig]
    -Iterate through the Measurements and Motions lists with Update() and Predict() respectively
    '''
    for i in range(len(measurements)):
        [mu, sig] = update(mu, sig, measurements[i], measurement_sig)
        print("Update: ", [mu, sig])
        [mu, sig] = predict(mu, sig, motions[i], motions_sig)
        print("Predict: ", [mu, sig])