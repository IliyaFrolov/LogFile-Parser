import math
import numpy as np
import matplotlib.pyplot as plt

class Particle:
    
    G = 6.67408E-20
   
    def __init__(self, Position=np.array([0,0,0], dtype=float), Velocity=np.array([0,0,0], dtype=float), Acceleration=np.array([0,-10,0], dtype=float), Name='Ball', Mass=1.0):

        self.position = np.array(Position, dtype = float)
        self.velocity = np.array(Velocity, dtype = float)
        self.acceleration = np.array(Acceleration, dtype = float)
        self.Name = Name
        self.mass = Mass

    def __repr__(self):
        return 'Particle: {0}, Mass: {1:12.3e}, Position: {2}, Velocity: {3}, Acceleration: {4}'.format(self.Name,self.mass,self.position, self.velocity,self.acceleration)    
    
    def update_1(self, deltaT):

            '''This method uses the euler method'''

            self.position = self.position + self.velocity*deltaT
            self.velocity = self.velocity + self.acceleration*deltaT 
    
    def update_2(self, deltaT):

            '''This method uses the euler cromer method'''

            self.velocity = self.velocity + self.acceleration*deltaT 
            self.position = self.position + self.velocity*deltaT

    
    

    





    
        



