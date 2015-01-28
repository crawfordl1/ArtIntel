'''
Created on Jan 26, 2015

@author: Wastedyu6

TOPIC: NON-NORMALIZED Uniform Probability Distribution
'''

#Create Probability Vectors (p) of Arbitrary size (N)
#EX: N = 5
class MyClass(object):
    
    #Initialize non-Empty List (p) - UNIFORM DISTRIBUTION
    p=[0.2,0.2,0.2,0.2,0.2]
    
    '''### CLASS VARIABLES ###
    pHit - Probability Robot finds the Vector it is looking for
    pMiss - Probability Robot cannot find the Vector it is looking for
    '''
    pHit = 0.6
    pMiss = 0.2

    '''
    Since List p has 5 elements (as we defined above), multiply each element
    by its probability to find the Vector it is looking for. In this case,
    Elements p[1] and p[2] are the Vectors that the Robot is looking for.
    
    Thus, there is 60% chance the Robot finds  1 of the 5 elements (20% chance)
    --->EX: 60% * 20%
    '''
    p[0]=p[0]*pMiss
    p[1]=p[1]*pHit
    p[2]=p[2]*pHit
    p[3]=p[3]*pMiss
    p[4]=p[4]*pMiss
    
    '''*Alternative method to Iterate through Lists based on their Element. Required for Large Lists!
    for i in range(len(p)):
        if i == 1 or i == 2:
            p[i] = p[i]*pHit
        else:
            p[i] = p[i]*pMiss
    '''     
            

    print("The Non-Normalized Uniform Probability Distribution is as follows:")
    print(" ")
    print p