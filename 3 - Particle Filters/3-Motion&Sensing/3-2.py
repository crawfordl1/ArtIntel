'''
Created on Feb 12, 2015

@author: Wastedyu6

TOPIC: Robot Sensing based on Motion Measurements
'''

from math import *
import random

'''### GLOBALLY DEFINED VARIABLES ###
landmarks - the "world" has 4 landmarks. The robot's initial coordinates are somewhere in the square represented by the landmarks.
world_size - Cyclic "world" the Robot is bound to
*NOTE: Landmark coordinates are given in (y, x) form and NOT in the traditional (x, y) format!
'''
landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]]
world_size = 100.0

class robot:

    #Creates robot and initializes location/orientation 
    def __init__(self, length = 10.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))
    
    #Sets a robot coordinate
    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    #Sets the noise parameters
    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)
    
    #Sense Measurements to determine Bearing
    def sense(self, add_noise = 1):
        Z = []  #Return all 4 Bearings of Landmarks
        
        '''
        For each Landmark, determine the bearing of those landmarks in reference to the Car's current orientation in the World
        -Subtract current orientation to find the landmarks bearing on X & Y plane
        -Accomodate for potential noise
        '''
        for i in range(len(landmarks)):
            #Compute ArcTangent of Bearing
            bearing = atan2(landmarks[i][0] - self.y,
                            landmarks[i][1] - self.x) - self.orientation
            
            if add_noise:
                bearing = bearing + random.gauss(0.0, self.bearing_noise)
            bearing = bearing % (2.0 * pi)  #normalize Bearing
            Z.append(bearing)
        
        return Z
    
'''### BEGIN DEFINING ROBOT AND NOISE ###
Initialize a Robot at Random and have it Move() based on Motion[] input
'''
length = 20.
bearing_noise  = 0.0
steering_noise = 0.0
distance_noise = 0.0

myrobot = robot(length)
myrobot.set(30.0, 20.0, 0.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

print 'Robot:        ', myrobot
print 'Measurements: ', myrobot.sense()