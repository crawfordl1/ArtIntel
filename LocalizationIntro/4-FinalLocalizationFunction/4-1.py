'''
Created on Jan 28, 2015

@author: Wastedyu6

TOPIC: Sense Multiple Colors via Sense() Function and Move() Accordingly
'''

'''### GLOBALLY DEFINED VARIABLES ###
world - Same length as List p. World specifies the color of the Grid-cell (i.e. Element) that the Robot "Senses"
pHit - Probability the Robot Successfully Reads its Target per the Z variable
pMiss - Probability the Robot MisReads its Target per the Z variable
pExact - Probability Robot Moves to Correct location
pOvershoot - Probability Robot Over-shoots expected Location
pUndershoot - Probability Robot Under-shoots expected Location
'''
world = ['green', 'red', 'red', 'green', 'green']
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1 
 
class MyClass(object):
    
    '''### CLASS VARIABLES ###
    p - Input Probability (Uniform)
    Motions - How many times and which direction the Robot is defined to Move
        --> This Example is: 
        1.) Move Right and Sense Red
        2.) Move Right AGAIN and Sense Green
    Measurements - Robot First senses Red and THEN Green  
    '''    
    p = [0.2,0.2,0.2,0.2,0.2]
    motions = [1,1]
    measurements = ['red', 'green']
    
    '''### SENSE() FUNCTION ###
    -Purpose: Measurement Update of Robot "sensing" colors of grid-cells
    -Input: 
        -List (p) - Uniform Probability Distribution
        -Variable (Z) - Desired Robot Measurement
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
    
    '''
    -Purpose: For Each Element in Measurements List, determine Normalized Probability and update List p accordingly
    -Sense first, Move second. 
        -As the Robot Senses it GAINS more accurate information about its environment
        -As the Robot Moves, it it LOSES information about its current environment
    '''
    for j in range(len(measurements)):
        p = sense(p, measurements[j])
        p = move(p, motions[j])
    print p