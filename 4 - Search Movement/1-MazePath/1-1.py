'''
Created on Feb 18, 2015

@author: Wastedyu6

TOPIC: In a 2D world, find Optimal Path for Robot's Starting Point to End Point
'''

'''### GLOBALLY DEFINED VARIABLES ###
grid - Global Grid Robot can move in
init - Starting point of Robot
goal - End point for Robot
cost - number of moves associated with moving between grid spaces
'''
# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

'''
Grid Format:
   0 = Navigable space
   1 = Occupied space
'''
grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]    #Subtract one b/c grid starts at [0,0]
cost = 1
move = [0, 0]
delta = [[-1, 0], # go up
         [ 0,-1], # go left
         [ 1, 0], # go down
         [ 0, 1]] # go right

#delta_name = ['^', '<', 'v', '>']

'''### SEARCH() FUNCTION ###
    -Purpose: Measurement Update of Robot "sensing" colors of grid-cells
        -*Note: Functions allow for the calculation of any arbitrary, non-specified Input
    -Input: 
        -List (p) - Uniform Probability Distribution
        -Global Variable (Z) - Desired Robot Measurement
    -Output: 
        -List (q) - NON-NORMALIZED Distribution (i.e. for all elements based on Senese Measurement: p * pHit or pMiss)
'''
def search(grid,init,goal,cost):
    g = 0
    
    '''###CLOSED LIST###
    -Purpose: "Checks" off Grid Cells that have been expanded and marked as NOT the Goal Location
    --List is set to the same size as Grid; in order to not modify original Grid
    '''
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid[0]))]
    closed[init[0]][init[1]] = 1
    
    #Set X & Y equal to Zero; as per Starting Point values (init)
    x = init[0]
    y = init[1]
    
    '''###OPEN LIST###
    -Purpose: Place-Holder for new Grid Locations to be "Expanded"
    --List is set to the same size as Grid; in order to not modify original Grid
    '''
    open = [[g, x, y]]
    
    found = False   #True when Goal is found
    resign = False  #True when Open List is Empty and Goal has not been found
    
    #While Goal has NOT been found and the Maze has NOT been proven to be unsolvable
    while found is False and resign is False:
    #Expand grid location with lowest G-Value that was determined
    
        #If Open List is Empty (i.e. no Grid Locations to "Expand")
        if len(open) == 0:
            resign = True
            print 'fail'
        #If Elements exist in Open List (Expandable Items)
        else:
            '''###SORT OPEN LIST
            -Purpose: Remove Element with the Smallest G Value
            '''
            open.sort()         #Sort elements in increasing order
            open.reverse()      #Reverse those elements in decreasing order
            next = open.pop()   #Remove the last element (smallest) in Open List
            
            #Assign Open List values accordingly
            g = next[0]
            x = next[1]
            y = next[2]
            
            #Check if X & Y values from Open list match Goal Values   
            if x == goal[0] and y == goal[1]:
               found = True
               print next
            else:
                for i in range(len(delta)):
                    #Apply movement values to both X & Y
                    newX = x + delta[i][0]
                    newY = y + delta[i][1]
                    
                    #If new X & Y are in the Grid
                    if newX >= 0 and newX < len(grid) and newY >= 0 and newY < len(grid[0]):
                        #If new X & Y are not yet "checked" and there is no obstacle in the way (i.e. a #1)
                        if closed[newX][newY] == 0 and grid[newX][newY] == 0:
                            newG = g + cost                     #Update G-Value
                            open.append([newG, newX, newY])     #Append new Expanded Grid Location in order to Test it
                            closed[newX][newY] = 1              #Mark the old location as "checked"
search(grid,init,goal,cost)