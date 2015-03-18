'''
Created on Feb 24, 2015

@author: Wastedyu6
'''
# ----------
# User Instructions:
# 
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal. 
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def optimum_policy(grid,goal,cost):
    '''###VALUE LIST###
    -Purpose: Bariers represented as "99"; large enough to not interfere with calculated grid values
    --List is set to the same size as Grid; in order to not modify original Grid
    '''
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    
    '''###POLICY LIST###
    -Purpose: Bariers represented as "99"; large enough to not interfere with calculated grid values
    --List is set to the same size as Grid; in order to not modify original Grid
    '''
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    change = True
    
    '''
    -Purpose: From any Grid location, determine the number of moves required to get to the Goal 
    --Update Value List depending on when the Grid Cell values need to Change
    '''
    while change:
        change = False
        
        #Iterate through all Grid Cells
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                
                #Is the current Grid Cell the Goal? If yes, Change = True
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = '*'
                        change = True
                        
                #If Goal has not been found, move to next Grid Cell and Determine its distance to the GOAL  
                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]
                        
                        '''
                        -Are the new X & Y values actually in the Grid?
                        -Is the new grid location an open grid or a barrier (i.e. 99)
                        --->If Yes, update Value List with the new value in relation to the where the Grid is to the GOAL
                        '''
                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            #New Value after Delta Actions and the Cost of the Step
                            v2 = value[x2][y2] + cost

                            #Is this new Value better? If Yes, update Value List and set Boolean
                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2                #Reassign v2 in order to reuse in Loop
                                policy[x][y] = delta_name[a]

    return policy