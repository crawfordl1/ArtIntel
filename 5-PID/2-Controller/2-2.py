'''
Created on Mar 1, 2015

@author: Wastedyu6

TOPIC: In a 2D world, apply Proportional Controller to Robot to CONVERGE specified Trajectory
*Note: Robot no longer oscillates over Trajectory but converges to appropriate Goal Location (SMOOTHED PATH)
'''

from math import *
import random


'''### START ROBOT CLASS DEFINITION ###
    -Robot class for implementing PID Controller
'''
class robot:

    # --------
    # init: 
    #    creates robot and initializes location/orientation to 0, 0, 0
    #

    def __init__(self, length = 20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    # --------
    # set: 
    #    sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation) % (2.0 * pi)


    # --------
    # set_noise: 
    #    sets the noise parameters
    #

    def set_noise(self, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # set_steering_drift: 
    #    sets the systematical steering drift parameter
    #

    def set_steering_drift(self, drift):
        self.steering_drift = drift
        
    # --------
    # move: 
    #    steering = front wheel steering angle, limited by max_steering_angle
    #    distance = total distance driven, most be non-negative

    def move(self, steering, distance, 
             tolerance = 0.001, max_steering_angle = pi / 4.0):

        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0


        # make a new copy
        res = robot()
        res.length         = self.length
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = tan(steering2) * distance2 / res.length

        if abs(turn) < tolerance:

            # approximate by straight line motion

            res.x = self.x + (distance2 * cos(self.orientation))
            res.y = self.y + (distance2 * sin(self.orientation))
            res.orientation = (self.orientation + turn) % (2.0 * pi)

        else:

            # approximate bicycle model for motion

            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            res.orientation = (self.orientation + turn) % (2.0 * pi)
            res.x = cx + (sin(res.orientation) * radius)
            res.y = cy - (cos(res.orientation) * radius)

        return res

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)

'''### RUN() FUNCTION ###
    -Purpose: Robot follows Trajectory (y-axis) until it Converges with Goal Trajectory
    --As Robot gets closer to Trajectory, it "counter-steers" in order to not Overshoot (compared to 2-1)
    -Input: 
        -Tau1 = Response Strength of Proportional Controller; inversely proportional to Y-Axis
        -Tau2 = Differentially & inversely proportional to Y-Axis
    -Output: 
        -Current Robot location and accompanying Steering Angle after P-Controller application
'''
def run(tau1, tau2):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0) #---> If Y = 1; then Tau = 0.1 (Inversely Proportional)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    N = 100
    
    '''
    -crosstrack_error = Distance from current Y-Axis Robot location to Goal Y-Axis Trajectory
    '''
    crosstrack_error = myrobot.y    #Initialize
    
    for i in range(N):  #100 Robot "steps"
        crosstrack_difference = myrobot.y - crosstrack_error    #Differential between Current Location and Goal Location
        crosstrack_error = myrobot.y                            #Reset current Cross Error
                 
        steer1 = - tau1 * crosstrack_error      #Approach trajectory
        steer2 = tau2 * crosstrack_difference   #Robot corrects itself according to Trajectory as the Cross Error gets smaller
        steeringDif = (steer1 - steer2) / speed           #Steering Angle based on distance away from Trajectory Path
        myrobot = myrobot.move(steeringDif, speed)
        print myrobot, steeringDif
        
run(0.2, 3.0) 