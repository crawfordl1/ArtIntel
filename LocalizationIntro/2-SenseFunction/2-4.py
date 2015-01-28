'''
Created on Jan 26, 2015

@author: Wastedyu6

TOPIC: NON-NORMALIZED Uniform Probability Distribution via Sense Function

*This Exercise only calculates the Sum based on the measurement readings in the Sense Function.
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
    Z - The Color the Robot is SUPPOSED to find  
    '''    
    p = [0.2, 0.2, 0.2, 0.2, 0.2]
    Z = 'red'

    '''### SENSE() FUNCTION ###
    -Purpose: Measurement Update of Robot "sensing" colors of grid-cells
    -Input: 
        -List (p) - Uniform Probability Distribution
        -Variable (Z) - Desired Robot Measurement defined as a variable for the Hit Binary Flag to interpret
    -Output: 
        -List (q) - NON-NORMALIZED Distribution (i.e. for all elements based on Sense Measurement: p * (pHit or pMiss)
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
            '''
            If Hit is False (0) Then we can calculate the Probability of MISSING the Grid-Cell
                --> (0 * pHit + (1-0) * pMiss)
                --> (0 + 1 * pMiss)
            If Hit is True (1) Then we can calculate the Probability of HITTING the Grid-Cell
                --> (1 * pHit + (1-1) * pMiss)
                --> (1 * pHit + 0)
            '''   
        return q
    print sense(p,Z)