'''
Created on Mar 1, 2015

@author: Wastedyu6

TOPIC: PDI Controller parameters optimized by determining the best environment parameters to be inputed
*Note: Robot CONVERGES to Goal Location (SMOOTHED PATH)
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
        -Tau3 = Differentially & inversely proportional to Y-Axis
    -Output: 
        -Current Robot location and accompanying Steering Angle after P-Controller application
'''
def run(tau, printflag = False):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)  #---> If Y = 1; then Tau = 0.1 (Inversely Proportional)
    speed = 1.0                 # motion distance is equal to speed (we assume time = 1)
    error = 0.0                 #
    N = 100
    myrobot.set_steering_drift(10.0 / 180.0 * pi) # 10 degree bias applied to Move() function
    
    '''
    -crosstrack_error = Distance from current Y-Axis Robot location to Goal Y-Axis Trajectory
    '''
    crosstrack_error = myrobot.y    #Initialize
    crosstrack_sum =   0.0
    
    for i in range(N * 2):  #100 Robot "steps"
        crosstrack_difference = myrobot.y - crosstrack_error    #Differential between Current Location and Goal Location
        crosstrack_error = myrobot.y                            #Reset current Cross Error
        crosstrack_sum = crosstrack_sum + crosstrack_error      #Calculate Sum of all Crosstrack Errors                          
                 
        steer1 = - tau[0] * crosstrack_error      #Approach trajectory
        steer2 = tau[1] * crosstrack_difference   #Robot corrects itself according to Trajectory as the Cross Error gets smaller
        steer3 = tau[2] * crosstrack_sum
        steeringDif = (steer1 - steer2- steer3) / speed           #Steering Angle based on distance away from Trajectory Path
        myrobot = myrobot.move(steeringDif, speed)
        
        if i >= N:
            error = error + (crosstrack_error **2)
        if printflag:
            print myrobot, steeringDif
            
'''### TWIDDLE() FUNCTION ###
    -Purpose: Optimize Parameters to measure the MOST ACUURATE Cross Track Error According to Goal Location
    -Input: 
        -Tolerance level to compare calculated errors to
    -Output: 
        -Most Accurate Parameters values to input into PDI Controller
'''        
def twiddle(tolerance = 0.001):
    
    n_tau = 3                               #Number of Parameters in PDI Controller
    d_tau = [1.0 for row in range(n_tau)]   #Initialize Delta Parameters to 1; This is the List of Potential Changes to be made to actual Parameters
    tau = [0.0 for row in range(n_tau)]     #Initialize with Empty Parameters
    
    best_error = run(tau)   #Current Best Error without Parameter (tau) OPTIMIZATION
    n = 0           #Counter
    error = 0.0     #Re-Calculated Error to be compared to previously calculated  Best Error
    
    '''
    -While Sum of Delta Tau is greater than Tolerance, keep finding more ACCURATE parameters for PDI Controller
    --Looping through LIST Tau
    '''
    while sum(d_tau) > tolerance:
        for i in range(len(tau)):
            tau[i] = tau[i] + d_tau[i]  #Increment current Tau parameters with current Delta Tau values
            error = run(tau)
            #If Error is more accurate (LESS), increment Delta Tau to Widen Parameters Search
            if error < best_error:
                best_error = error          #Update newest more ACCURATE error to Best Error
                d_tau[i] = (d_tau[i] * 1.1) #"Widen" Search Area - The Larger the Value, The more ACCURATE THE ERROR
            #However, if new Error not as Accurate than best Error
            else:
                tau[i] = tau[i] - (2.0 * d_tau[i])  #Subtracted TWICE b/c it was added in Line 184 already. Needs to be subtracted altogether
                error = run(tau)                    #Recalculate old Error Value to compare again to Best Error
                
                #AGAIN, If Error is more accurate (LESS), increment Delta Tau to Widen Parameters Search
                if error < best_error:
                    best_error = error
                    d_tau[i] = (d_tau[i] * 1.1)
                #If a BETTER Error is not found, Decrease Search Area and try again
                else:
                    tau[i] += d_tau[i]          #Reset Parameters back to original Values (Line 184)
                    d_tau[i]= (d_tau[i] * 0.9)  #Decrease Search Area
        n = n + 1   #Increase Counter
    return run(tau)

'''
Optimize Parameter Values for the PDI Controller and Calculate the Cross Tracking Error according to the Robots Location and its Goal Location
'''
tau = twiddle()
error = run(tau, True)