'''
Created on Feb 24, 2015

@author: Wastedyu6
'''
# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# returns two grids. The first grid, value, should 
# contain the computed value of each cell as shown 
# in the video. The second grid, policy, should 
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    
    '''###VALUE LIST###
    -Purpose: Barriers represented as "99"; large enough to not interfere with calculated grid values
    --List is set to the same size as Grid; in order to not modify original Grid
    '''
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    
    '''###Policy LIST###
    -Purpose: non-Barriers represented as 'spaces'; a blank grid to update as movement values are determined
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
                        policy[x][y] = '*'  #Set GOAL = * in the POLICY LIST

                        change = True
                #If Goal has not been found, move to next Grid Cell and Determine its distance to the GOAL   
                elif grid[x][y] == 0:
                    for a in range(len(delta)):     #Iterate through all Delta Actions and add to X & Y appropriately
                        v2 = cost_step
                        
                        #Iterate through all different Action outcomes (this List is -1, 0 and 1)
                        for i in range(-1, 2):
                            a2 = (a + i) % len(delta)   #Set Action Outcome to adjacent Grid cell action in Action List
                            x2 = x + delta[a2][0]
                            y2 = y + delta[a2][1]
                            
                            if i == 0:
                                p2 = success_prob
                            else:   #i.e. if -1, 1 or 2
                                p2 = (1 - success_prob) / 2.0   #Divide by two to make up difference of other possible outcomes
                                
                            '''
                            -Are the new X & Y values actually in the Grid?
                            -Is the new grid location an open grid or a barrier (i.e. 99)
                            --->If Yes, update Value List with the new value in relation to the where the Grid is to the GOAL
                            '''    
                            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                                #New Value after Delta Actions multiplied by the Success Probability previously calculated
                                v2 += p2 * value[x2][y2]
                            else:   #Barrier Hit! Penalty
                                v2 += p2 * collision_cost 
                        #Is this new Value better? If Yes, update Value List and set Boolean
                        if v2 < value[x][y]:
                            change = True
                            value[x][y] = v2                #Reassign v2 in order to reuse in Loop
                            policy[x][y] = delta_name[a]    #Update POLICY LIST for reuse
    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1] # Goal is in top right corner
cost_step = 1
collision_cost = 100
success_prob = 0.5

value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
# [57.9029, 40.2784, 26.0665,  0.0000]
# [47.0547, 36.5722, 29.9937, 27.2698]
# [53.1715, 42.0228, 37.7755, 45.0916]
# [77.5858, 1000.00, 1000.00, 73.5458]
#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']