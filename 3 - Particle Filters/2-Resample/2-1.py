'''
Created on Feb 4, 2015

@author: Wastedyu6

TOPIC: Resample Random Particles in determine new / more accurate locations
'''

from math import *
import random


'''### GLOBALLY DEFINED VARIABLES ###
landmarks - Preset locations the Robot is determinging its distance from in order to determine its own Location
world_size - Cyclic "world" the Robot is bound to
'''
landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0

'''### START ROBOT CLASS DEFINITION ###
    Below code implements the Robot Class in order to be utilized in Particle Filter
    '''
class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise    = 0.0;
        self.sense_noise   = 0.0;
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
    
    
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
    
    
    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z
    
    
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'         
        
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        
        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        
        # set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
    
    def Gaussian(self, mu, sigma, x):
        
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    
    def measurement_prob(self, measurement):
        
        # calculates how likely a measurement should be
        
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob
    
    
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))



def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))

'''### BEGIN DEFINING ROBOT AND PARTICLES ###
Initialize a Robot at Random and have it Sense where it was randomly placed in the World
'''
myRobot = robot()
myRobot = myRobot.move(0.1, 5.)
Z = myRobot.sense()

'''
-PURPOSE: Create Particles
Initialize N amount of Particles and place them into List p
'''
N = 1000             #1,000 random particles
p1 = []              #Initialize List to store each particle (created as its own Robot)
for i in range(N):
    particle = robot()                      #Create new Robot object
    particle.set_noise(0.05, 0.05, 5.)      #Noise MUST be set for Measurement() to calculate. ALL measurements are APPORXIMATIONS - Thus, Noise
    p1.append(particle)                     #Put Robot in LIst p

'''
-PURPOSE: Make changes to existing Particles
-Create second "placeholder" List p2 in order to apply changes to the original particles
-Once every particle has been moved, make List p = p2
'''
p2 = []              #Placeholder List
for j in range(N):
    p2.append(p1[j].move(0.1, 5.0))  #Apply Movement of Robots in List p1 to empty List p2 
p = p2

'''
-PURPOSE: Calculate Weight (Accuracy) of each Particle
'''
w = []
for k in range(N):
    w.append(p1[k].measurement_prob(Z))

'''
-PURPOSE: Resample Particles for a more Accurate reading of Particle Locations
-PROCEDURE: Sample N new Particles by sampling the Particle List proportional to the Wieght List
'''
p3 = []
beta = 0.0      #Variable defined to compare to each Particle
index = int(random.random() * N)                    #Set Indew to random Particle
for i in range(N):
    beta = beta + random.random() * 2.0 * max(w)    #Add Random Weight to Beta variable
    '''
    If the current Weight does not "reach Beta in Resampling Wheel" i.e. be equal or larger
    Then subtract that Weight value from beta and Increment the Index by One
    Thus, when new Weight value has been added, Beta must be smaller than the new Weight
        --->Weight Index (List w) is now the same as the Particle Index (List p)
    '''
    while w[index] < beta:          #If Particle index if less than Beta variable
        beta = beta - w[index]      #Subtract Beta from index in order to
        index = (index + 1) % N
    p3.append(p[index])
p = p3
print p