'''
Created on Jan 28, 2015

@author: Wastedyu6

TOPIC: Sense Multiple Colors via Sense() w/ NON-UNIFORM Probability Distribution
'''

'''### GLOBALLY DEFINED VARIABLES ###
pExact - Probability Robot Moves to Correct location
pOvershoot - Probability Robot Over-shoots expected Location
pUndershoot - Probability Robot Under-shoots expected Location
'''
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1    
class MyClass(object):
    
    '''### CLASS VARIABLES ###
    p - Input Probability (non-Uniform)
    '''    
    p = [0,1,0,0,0]
    
    
    '''### MOVE() FUNCTION ###
    -Purpose: Measurement Update of Robot "moving" RIGHT between grid-cells
    -Input: 
        -List (p) - UNIFORM Probability Distribution
        -Motion Number (U) - Number of Grid-cells the Robot is moving
            -If U is a + number, Shift RIGHT
            -If U is a - number, Shift LEFT
            -If U is equal to zero; Stay-put
    -Output: 
        -List (q) - New Probability Distribution of Robot AFTER the Move has occurred
            i.e. What is the new Probability of finding desired colors based on where the Robot THINKS it is now?
    '''
    def move(p, U):
        q = []
        for i in range(len(p)):
            m = pExact * (p[(i - U) % (len(p))])
            m = m + pOvershoot * (p[(i - U - 1) % (len(p))])    #Subtract an extra element location for Overshooting target
            m = m + pOvershoot * (p[(i - U + 1) % (len(p))])    #Add an extra element location for Overshooting target
            q.append(m)       
        return q
    print move(p, 1)