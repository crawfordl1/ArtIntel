'''
Created on Feb 25, 2015

@author: Wastedyu6

TOPIC: In a 2D world, utilize Smoothing Algorithm to find Optimal Path for Robot's Starting Point to End Point
'''

from copy import deepcopy

'''### GLOBALLY DEFINED VARIABLES ###
Path - Original non-Smooth Path
'''

#Print the non-Smooth Path to compare to Smooth Path
def printpaths(path,newpath):
    for old,new in zip(path,newpath):
        print '['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']'

path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

'''### SMOOTH() FUNCTION ###
    -Purpose: Calculate a new "smooth" path based on the current non-smooth path
    -Input: 
        -Path - Current non-Smooth Path to be used to create Smooth Path
        -Weight_data - static integer multiplied by the original path (Xi) coordinate to minimize Error between Path (Xi) & New Path (Yi)
        -Weight_smooth - static integer multiplied by the new path (Yi) to minimize distance between the new path (Yi) and the next coordinate (Yi+1)
        -Tolerance - small static integer to ensure the smooth path is as accurate as possible
    -Output: 
        -NewPath - the newly calculated Smooth Path
'''
def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):

    # Make a deep copy of path into newpath
    #newpath = deepcopy(path)
    #Create a "deep copy" of the current path inside the Smooth Path that is to be modified.
    newpath = [[0 for row in range(len(path[0]))] for col in range(len(path))]
    for i in range(1, len(path) - 1):
            for j in range(len(path[0])):
                newpath[i][j] = path[i][j]
    
    change = tolerance
    while change >= tolerance:
        change = 0.0
        #Iterate over all Path Entries except for the 1st and Last entries
        for i in range(1, len(path) - 1):
            for j in range(len(path[0])):
                #Store the current Yi value before it is updated
                previous_newpath = newpath[i][j]
                
                #Gradient Descent Formula
                error = newpath[i][j] + weight_data * (path[i][j] - newpath[i][j])
                distance = weight_smooth * (newpath[i + 1][j] + newpath[i - 1][j] - (2* newpath[i][j]))
                newpath[i][j] =  error + distance
                
                #Record how much Yi has changed from Yi+1. If above tolerance, keep computing NewPath values
                change = change + abs(previous_newpath - newpath[i][j])
    return newpath

printpaths(path,smooth(path))