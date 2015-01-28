'''
Created on Jan 26, 2015

@author: Wastedyu6

TOPIC: NORMALIZED Uniform Probability Distribution w/ no Function

*To Normalize, the non-Normalized Distributions are to be divided by
the SUM of the all non-Normalized Distributions. Note that the Sum of these
Normalized values should add to 1. 

This Exercise only calculates the Sum and then the Normalized Distribution.
'''

#Create Probability Vectors (p) of Arbitrary size (N)
#EX: N = 5
class MyClass(object):
    
    #Initialize non-Empty List (p) - UNIFORM DISTRIBUTION
    p=[0.2,0.2,0.2,0.2,0.2]
    normalize = 0
    
    '''### CLASS VARIABLES ###
    pHit - Probability Robot finds the Vector it is looking for
    pMiss - Probability Robot cannot find the Vector it is looking for
    '''
    pHit = 0.6
    pMiss = 0.2

    '''
    Iterate through List p. If element 1 or 2 is found, multiply by the Hit variable. Else, multiply by Miss.
    '''
    for i in range(len(p)):
        if i == 1 or i == 2:
            p[i] = p[i]*pHit
        else:
            p[i] = p[i]*pMiss 
            
    #Add all probabilities in List p. FIRST STEP in Normalization
    sum = sum(p)

    print("The Sum of the non-Normalized Uniform Probability Distribution is as follows:")  
    print sum
    print(" ")  
    
    #Iterate through newly modified List p and divide each element by the Sum; add each of these values together to get 1.0
    for j in range(len(p)):
        normalize = normalize + p[j]/sum
        
    print("The Normalized Probability Distribution is:")
    print normalize