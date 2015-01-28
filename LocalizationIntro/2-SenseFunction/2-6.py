'''
Created on Jan 28, 2015

@author: Wastedyu6

TOPIC: Sense Multiple Colors via Sense() Function
'''

'''### GLOBALLY DEFINED VARIABLES ###
world - Same length as List p. World specifies the color of the Grid-cell (i.e. Element) that the Robot "Senses"
pHit - Probability the Robot Successfully Reads its Target per the Z variable
pMiss - Probability the Robot MisReads its Target per the Z variable
'''
world = ['green', 'red', 'red', 'green', 'green']
pHit = 0.6
pMiss = 0.2

class MyClass(object):
    
    '''### CLASS VARIABLES ###
    p - Input Probability (Uniform) - i.e. Where the Robot Thinks it is before any Measurements are calculated. Everywhere!
    measurements - The Color(s) the Robot is SUPPOSED to find; order of colors found based on colors defined in List  
    '''    
    p = [0.2, 0.2, 0.2, 0.2, 0.2]
    measurements = ['red', 'green']
    
    '''### SENSE() FUNCTION ###
    -Purpose: Measurement Update of Robot "sensing" colors of grid-cells
    -Input: 
        -List (p) - Uniform Probability Distribution
        -Variable (Z) - Ideal Robot Measurement defined as a variable for the Hit Binary Flag to interpret
    -Output: 
        -List (q) - NORMALIZED Distribution (i.e. for all elements based on Sense Measurement: p * (pHit or pMiss)
    '''
    def sense(p, Z):
        #Define Empty List q
        q=[]
        
        #Iterate over all elements in Input Probability p
        for i in range(len(p)):
            #Hit - Binary Flag to indicate if the Measurement read in the current element is the same as Z
                #Red = 1
                #Green = 0
            hit = (Z == world[i])
            q.append(p[i] * (hit * pHit + (1-hit) * pMiss))

        #Calculate Sum of all newly calculated Probabilities in List q    
        s = sum(q)    
            
        #NORMALIZE List q by dividing each new Probability by the Total Sum of those Probabilities    
        for i in range(len(q)):  
            q[i] = q[i]/s
        return q
    
    #For Each Element in Measurements List, determine Normalized Probability and update List p accordingly
    for j in range(len(measurements)):
        p = sense(p, measurements[j])
    print p