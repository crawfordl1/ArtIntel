'''
Created on Jan 26, 2015

@author: Wastedyu6

TOPIC: NON-NORMALIZED Uniform Probability Distribution

*To Normalize, the non-Normalized Distributions are to be divided by
the SUM of the all non-Normalized Distributions.

This Exercise only calculates the Sum.
'''

#Create Probability Vectors (p) of Arbitrary size (N)
#EX: N = 5
class MyClass(object):
    
    #Initialize non-Empty List (p) - UNIFORM DISTRIBUTION
    p=[0.2,0.2,0.2,0.2,0.2]
    
    '''### CLASS VARIABLE S###
    pHit - Probability Robot finds the Vector it is looking for
    pMiss - Probability Robot cannot find the Vector it is looking for
    '''
    pHit = 0.6
    pMiss = 0.2
    
    for i in range(len(p)):
        if i == 1 or i == 2:
            p[i] = p[i]*pHit
        else:
            p[i] = p[i]*pMiss 

    print("The Sum of the non-Normalized Uniform Probability Distribution is as follows:")
    print(" ")
    
    #Add all probabilities in List p. FIRST STEP in Normalization
    print sum(p)
    
    #Secondary method to Sum all elements in List p
    #sum = p[0]+p[1]+p[2]+p[3]+p[4]