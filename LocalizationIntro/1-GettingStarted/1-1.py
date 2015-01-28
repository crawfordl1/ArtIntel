'''
Created on Jan 24, 2015

@author: Wastedyu6

TOPIC: UNIFORM DISTRIBUTION
'''

#Create Probability Vectors (p) of Arbitrary size (N)
#EX: N = 5
class MyClass(object):
    
    def main():
    
        #Initialize Empty List (p) - i.e. Probability vector
        p = []
        n = 5
    
        #Iterate through List p and Append n elements to List p; each of uniform size
        #*Appending values changes the original value in the List
        for i in range(n):
            p.append(1./n)  #"." needed for "floating point" division

            print p
        
    if __name__ == '__main__':
        main()