'''
Created on Feb 11, 2015

@author: Wastedyu6

TOPIC: Robot Movement based on Motion Measurements
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
max_steering_angle = pi/4 # You don't need to use this value, but it is good to keep in mind the limitations of a real car.

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
    
    # move:
    #   move along a section of a circular path according to motion
    #
    
    def move(self, motion, tolerance = 0.001): # Do not change the name of this function
        
        #Set Motion Vector values
        steeringVector = motion[0]
        distanceVector = motion[1]
        
        #Error Checking for Distance and Steering Values
        if abs(steeringVector) > max_steering_angle:
            raise ValueError, 'Exceeding max steering angle'
        if distanceVector < 0:
            raise ValueError, 'Moving backwards is not valid in the experiment'
        
        #Set new Robot and accompanying Noise objects
        car = robot()
        car.length = self.length
        car.bearing_noise = self.bearing_noise
        car.steering_noise = self.steering_noise
        car.distance_noise = self.distance_noise
        
        #Set Random noise Values
        #Implementation equal to: steering + gauss(0, self.steering_noise)
        steering = random.gauss(steeringVector, self.steering_noise)
        distance = random.gauss(distanceVector, self.distance_noise)
        
        #Begin Motion Execution
        turn = (distance / car.length) * tan(steering)
        
        #Check if Car is Moving in Straight Line. If so, different calculation
        if abs (turn) < tolerance:
            car.x = self.x + (distance * cos(self.orientation))
            car.y = self.y + (distance * sin(self.orientation))
            car.orientation = (self.orientation + turn) % (2.0 * pi)
        else:   #Robot is Turning (i.e. Turning Angle > 0.001)
            
            #Turning Radius
            radius = distance / turn
            
            #Focal Point that the Car is turning around
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            car.orientation = (self.orientation + turn) % (2.0 * pi)
            
            #Input New Orientation & new CX & CY Values into new Car Location X & Y
            car.x = cx + (sin(car.orientation) * radius)
            car.y = cy - (sin(car.orientation) * radius)
               
        return car
    
'''### BEGIN DEFINING ROBOT AND NOISE ###
Initialize a Robot at Random and have it Move() based on Motion[] input
'''
length = 20.
bearing_noise  = 0.0
steering_noise = 0.0
distance_noise = 0.0

myrobot = robot(length)
myrobot.set(0.0, 0.0, 0.0)
myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

motions = [[0.0, 10.0], [pi / 6.0, 10], [0.0, 20.0]]

T = len(motions)

print 'Robot:    ', myrobot
for t in range(T):
    myrobot = myrobot.move(motions[t])
    print 'Robot:    ', myrobot
