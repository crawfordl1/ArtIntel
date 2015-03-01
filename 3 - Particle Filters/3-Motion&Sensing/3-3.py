'''
Created on Feb 12, 2015

@author: Wastedyu6

TOPIC: Combine Robot Sensing & Motion based on respective Measurements
'''
# --------------
# USER INSTRUCTIONS
#
# Now you will put everything together.
#
# First make sure that your sense and move functions
# work as expected for the test cases provided at the
# bottom of the previous two programming assignments.
# Once you are satisfied, copy your sense and move
# definitions into the robot class on this page, BUT
# now include noise.
#
# A good way to include noise in the sense step is to
# add Gaussian noise, centered at zero with variance
# of self.bearing_noise to each bearing. You can do this
# with the command random.gauss(0, self.bearing_noise)
#
# In the move step, you should make sure that your
# actual steering angle is chosen from a Gaussian
# distribution of steering angles. This distribution
# should be centered at the intended steering angle
# with variance of self.steering_noise.

from math import *
import random

'''### GLOBALLY DEFINED VARIABLES ###
landmarks - the "world" has 4 landmarks. The robot's initial coordinates are somewhere in the square represented by the landmarks.
world_size - Cyclic "world" the Robot is bound to
*NOTE: Landmark coordinates are given in (y, x) form and NOT in the traditional (x, y) format!
'''
landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks in (y, x) format.
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"

max_steering_angle = pi / 4.0 # You do not need to use this value, but keep in mind the limitations of a real car.
bearing_noise = 0.1 # Noise parameter: should be included in sense function.
steering_noise = 0.1 # Noise parameter: should be included in move function.
distance_noise = 5.0 # Noise parameter: should be included in move function.

tolerance_xy = 15.0 # Tolerance for localization in the x and y directions.
tolerance_orientation = 0.25 # Tolerance for orientation.

class robot:

    #Creates robot and initializes location/orientation 
    def __init__(self, length = 20.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero
        
    def __repr__(self): #allows us to print robot attributes.
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), 
                                                str(self.orientation))
    
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

    # --------
    # measurement_prob
    #    computes the probability of a measurement
    #  

    def measurement_prob(self, measurements):

        # calculate the correct measurement
        predicted_measurements = self.sense(0) # Our sense function took 0 as an argument to switch off noise.


        # compute errors
        error = 1.0
        for i in range(len(measurements)):
            error_bearing = abs(measurements[i] - predicted_measurements[i])
            error_bearing = (error_bearing + pi) % (2.0 * pi) - pi # truncate
            

            # update Gaussian
            error *= (exp(- (error_bearing ** 2) / (self.bearing_noise ** 2) / 2.0) /  
                      sqrt(2.0 * pi * (self.bearing_noise ** 2)))

        return error
    
    def move(self, motion, tolerance = 0.001): # Do not change the name of this function
        
        #Set Motion Vector values
        steeringVector = motion[0]
        distanceVector = motion[1]
        
        #Error Checking for Distance and Steering Values
        if abs(steeringVector) > max_steering_angle:
            raise ValueError, 'Exceeding max steering angle'
        if distanceVector < 0:
            raise ValueError, 'Moving backwards is not valid in the experiment'
        
        #Set new Robot and accompanying Noise ojects
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

    # --------
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
    
'''###GLOBALLY DEFINED HELPER FUNCTIONS FOR ERROR-CHECKING OF PARTICLE FILTER###
*NOTE: Outside of Robot Class
'''

#Extract position from a particle set 
def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi)) 
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]

#Generates the measurements vector
def generate_ground_truth(motions):

    myrobot = robot()
    myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

    Z = []
    T = len(motions)

    for t in range(T):
        myrobot = myrobot.move(motions[t])
        Z.append(myrobot.sense())
    #print 'Robot:    ', myrobot
    return [myrobot, Z]

#Prints the measurements associated with generate_ground_truth
def print_measurements(Z):

    T = len(Z)

    print 'measurements = [[%.8s, %.8s, %.8s, %.8s],' % \
        (str(Z[0][0]), str(Z[0][1]), str(Z[0][2]), str(Z[0][3]))
    for t in range(1,T-1):
        print '                [%.8s, %.8s, %.8s, %.8s],' % \
            (str(Z[t][0]), str(Z[t][1]), str(Z[t][2]), str(Z[t][3]))
    print '                [%.8s, %.8s, %.8s, %.8s]]' % \
        (str(Z[T-1][0]), str(Z[T-1][1]), str(Z[T-1][2]), str(Z[T-1][3]))

'''
Checks to see if particle filter localizes the robot to within the desired 
tolerances of the true position. The tolerances are defined at the top.
'''
def check_output(final_robot, estimated_position):

    error_x = abs(final_robot.x - estimated_position[0])
    error_y = abs(final_robot.y - estimated_position[1])
    error_orientation = abs(final_robot.orientation - estimated_position[2])
    error_orientation = (error_orientation + pi) % (2.0 * pi) - pi
    correct = error_x < tolerance_xy and error_y < tolerance_xy \
              and error_orientation < tolerance_orientation
    return correct



def particle_filter(motions, measurements, N=500): # I know it's tempting, but don't change N!
    '''
    -PURPOSE: Create Particles
    Initialize N amount of Particles and place them into List p
    '''
    p = []
    for i in range(N):
        r = robot()
        r.set_noise(bearing_noise, steering_noise, distance_noise)
        p.append(r)

    '''
    -PURPOSE: Make changes to existing Particles
    -Create second "placeholder" List p2 in order to apply changes to the original particles
    -Once every particle has been moved, make List p = p2
    '''
    for t in range(len(motions)):
    
        # motion update (prediction)
        p2 = []
        for i in range(N):
            p2.append(p[i].move(motions[t]))
        p = p2

        '''
        -PURPOSE: Calculate Weight (Accuracy) of each Particle
        '''
        w = []
        for i in range(N):
            w.append(p[i].measurement_prob(measurements[t]))

        '''
        -PURPOSE: Resample Particles for a more Accurate reading of Particle Locations
        -PROCEDURE: Sample N new Particles by sampling the Particle List proportional to the Wieght List
        '''
        p3 = []
        index = int(random.random() * N)
        beta = 0.0
        mw = max(w)
        for i in range(N):
            beta += random.random() * 2.0 * mw
            
            '''
            If the current Weight does not "reach Beta in Resampling Wheel" i.e. be equal or larger
            Then subtract that Weight value from beta and Increment the Index by One
            Thus, when new Weight value has been added, Beta must be smaller than the new Weight
                --->Weight Index (List w) is now the same as the Particle Index (List p)
            '''
            while beta > w[index]:
                beta -= w[index]
                index = (index + 1) % N
            p3.append(p[index])
        p = p3
    
    return get_position(p)
 
## --------
## TEST CASES:
## 
##1) Calling the particle_filter function with the following
##    motions and measurements should return a [x,y,orientation]
##    vector near [x=93.476 y=75.186 orient=5.2664], that is, the
##    robot's true location.
##
##motions = [[2. * pi / 10, 20.] for row in range(8)]
##measurements = [[4.746936, 3.859782, 3.045217, 2.045506],
##                [3.510067, 2.916300, 2.146394, 1.598332],
##                [2.972469, 2.407489, 1.588474, 1.611094],
##                [1.906178, 1.193329, 0.619356, 0.807930],
##                [1.352825, 0.662233, 0.144927, 0.799090],
##                [0.856150, 0.214590, 5.651497, 1.062401],
##                [0.194460, 5.660382, 4.761072, 2.471682],
##                [5.717342, 4.736780, 3.909599, 2.342536]]
##
##print particle_filter(motions, measurements)

## 2) You can generate your own test cases by generating
##    measurements using the generate_ground_truth function.
##    It will print the robot's last location when calling it.
##
##
number_of_iterations = 6
motions = [[2. * pi / 20, 12.] for row in range(number_of_iterations)]

x = generate_ground_truth(motions)
final_robot = x[0]
measurements = x[1]
estimated_position = particle_filter(motions, measurements)
print_measurements(measurements)
print 'Ground truth:    ', final_robot
print 'Particle filter: ', estimated_position
print 'Code check:      ', check_output(final_robot, estimated_position)

