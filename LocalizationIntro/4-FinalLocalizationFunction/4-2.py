'''
Created on Jan 28, 2015

@author: Wastedyu6

TOPIC: In a 2D World, Sense Multiple Colors via Sense() Function and Move() Accordingly
'''

'''### GLOBALLY DEFINED VARIABLES ###
world - Same length as List p. World specifies the color of the Grid-cell (i.e. Element) that the Robot "Senses"
p_Move - Probability Move() function is executed correctly
sensor_right - Probability Sense() measurement is correct
'''
p_move = 0.8
sensor_right = 0.7
world = [['red', 'green', 'green',   'red', 'red'],
        ['red',   'red', 'green',   'red', 'red'],
        ['red',   'red', 'green', 'green', 'red'],
        ['red',   'red',   'red',   'red', 'red']]

class MyClass(object):
    '''### CLASS VARIABLES ###
    Motions - How many times and which direction the Robot is defined to Move
    Measurements - Order of Which the Robot senses the Colors  
    '''    
    motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
    measurements = ['green', 'green', 'green' ,'green', 'green']
    
    '''### SHOW() FUNCTION ###
    -Purpose: Iterate through 2 Dimensional List in order to print Final Result
    -Input: 
        -List (p)
    -Output: 
        -List (p)
    '''
    def show(p):
        for i in range(len(p)):
            print p[i]
    
    #Initialize Probability Table by Counting how many Grid-cells are in the World
    total = 0.0
    for i in range(len(world)):
        total = total + len(world[i])
    print("Total number of Grid-Cells in the Robot World:")
    print(total)
    print("")
        
    #Create initial Uniform Distribution - Calculates probabilities based on TOTAL Grid-cells existing in World matrix
    #In this Example, before the Robot has moved, each Grid-cell has a (1/20) be the the location the Robot it Thinks it is on
    p = [[total for row in range(len(world[0]))] for col in range(len(world))]
    
    '''### SENSE() FUNCTION ###
    -Purpose: Measurement Update of Robot "sensing" colors of grid-cells
        -*Note: Functions allow for the calculation of any arbitrary, non-specified Input
    -Input: 
        -List (p) - Uniform Probability Distribution
        -Global Variable (Z) - Desired Robot Measurement
    -Output: 
        -List (q) - NON-NORMALIZED Distribution (i.e. for all elements based on Senese Measurement: p * pHit or pMiss)
    '''
    def sense(p, world, measurement):
        #Construct empty Posterior Distribution Matrix (Same size as p)
        q = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
        s = 0.0
        
        #Iterate all Rows
        for rows in range(len(p)):
            #Iterate all Columns
            for columns in range(len(p[rows])):
                hit = (measurement == world[rows][columns])    #Does Measurement Match the Color the Robot is Sensing?
                
                #Calculate Non-Normalized Posterior Distributions
                q[rows][columns] = p[rows][columns] * (hit * sensor_right + (1-hit) * (1.0 - sensor_right))
                s = s + q[rows][columns]    #Sum of non-Normalized Distribution after the Robot has Sensed
                '''
                If Hit is False (0) Then we can calculate the Probability of the Sensor's INACCURACY
                    --> (0 * sensor_right + (1-0) * (1 - sensor_right))
                    --> (0 + (1 - 0.3))
                If Hit is True (1) Then we can calculate the Probability of the Sensor's ACCURACY
                    --> (1 * sensor_right + (1-1) * (1 - sensor_right))
                    --> (1 * 0.7 + 0)
            '''
                
        #Normalize by dividing by Sum of Non-Normalized Posterior Distributions
        for rows in range(len(q)):
            for columns in range(len(p[rows])):
                q[rows][columns] = q[rows][columns] / s
        return q
    
    '''### MOVE() FUNCTION ###
    -Purpose: Measurement Update of Robot "moving" RIGHT between grid-cells
    -Input: 
        -List (p) - Probability Distribution
        -Motion Number (U) - Number of Grid-cells the Robot is moving. Motion Direction examples below:
            -[0,0]  - No Movement
            -[0,1]  - Move Right
            -[0,-1] - Move Left
            -[1,0]  - Move Down
            -[-1,0] - Move Up
    -Output: 
        -List (q) - New Probability Distribution of Robot AFTER the Move has occurred
            i.e. What is the new Probability of finding desired colors based on where the Robot THINKS it is now?
    '''
    def move(p, motion):
        #Construct empty Posterior Distribution Matrix (Same size as p)
        q = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
        
        for rows in range(len(p)):
            for columns in range(len(p[rows])):
                #Determine Cells that the Robot previously moved from
                q[rows][columns] = (p_move * p[(rows - motion[0]) % len(p)][(columns - motion[1]) % len(p[rows])]) + ((1.0-p_move) * p[rows][columns])
                '''
                Explanation for Addition of line: ((1.0-p_move) * p[rows][columns])
                -->Provides the Probability of if the Robot did not move. Thus Multiply current position by Probability of Staying in Position
                '''
        return q
    
    #Determine new Probability Distributions (Where the Robot Thinks it is) based on measurements from Move & Sense functions
    for k in range(len(measurements)):
        p = move(p, motions[k])  
        p = sense(p, world, measurements[k])
    #Print Final Probability Calculation of where the Robot Thinks it is!    
    show(p)