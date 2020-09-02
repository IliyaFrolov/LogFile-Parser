import math
import numpy as np
import matplotlib.pyplot as plt
from Particle import Particle
import copy

class Solarsystem:

    time = 0
    delta = 10000
    Data = []
    time_list = []
    
    KineticEnergy = []
    PotentialEnergy = []
    TotalEnergy = []
    Momentum = []

    x = []
    y = []
    x_1 = []
    y_1 = []
    x_2 = []
    y_2 = []
    x_3 = []
    y_3 = []
    x_4 = []
    y_4 = []
    x_5 = []
    y_5 = []
    x_6 = []
    y_6 = []
    x_7 = []
    y_7 = []
    x_8 = []
    y_8 = []
    x_9 = []
    y_9 = []

    def __init__(self, planets, kinetic_energy, potential_energy, total_energy, momentum, method):

        self.planets = planets
        self.kinetic_energy = kinetic_energy
        self.potential_energy = potential_energy
        self.total_energy = total_energy
        self.momentum = momentum
        self.method = method

    def simulation(self, planets):

        for step in range(1, 10001):
            
            '''Loop used to calculate the acceleration of each body'''

            for first_planet in planets:    

                first_planet.acceleration = 0

                for second_planet in planets:
                    if second_planet != first_planet:
                        
                        vector1 = second_planet.position - first_planet.position
                        vector_mag1 = math.sqrt(np.dot(vector1, vector1))
                        first_planet.acceleration += ((Particle.G*second_planet.mass)/vector_mag1**3)*vector1

            '''Loop used to update the body's position and velocity'''

            for m in planets:
                if self.method == 1:
                    m.update_1(Solarsystem.delta)
                
                elif self.method == 2:
                    m.update_2(Solarsystem.delta)
                
                else:
                    raise ValueError('Method not selected')

            '''Code used to calculate and store kinetic energy, potential energy, momentum and the total energy of the system at each time interval'''    
            
            Solarsystem.time += Solarsystem.delta
            Solarsystem.time_list.append(Solarsystem.time) 
            Solarsystem.PotentialEnergy.append(Solarsystem.pe_solar(self, planets))   
            Solarsystem.KineticEnergy.append(Solarsystem.ke_solar(self, planets))
            Solarsystem.TotalEnergy.append(Solarsystem.energy_conservation(self))
            Solarsystem.Momentum.append(Solarsystem.momentum_solar(self, planets))

            '''Code used to save body data at each time interval'''

            if step %100 == 0:
                item = []
                item.insert(0, Solarsystem.time)

                for f in planets:
                    item.append(copy.deepcopy(f))
                
                Solarsystem.Data.append(item)
            
            '''Appends the body position after each iteration'''          

            Solarsystem.x.append(planets[0].position[0])
            Solarsystem.y.append(planets[0].position[1])
            Solarsystem.x_1.append(planets[1].position[0])
            Solarsystem.y_1.append(planets[1].position[1])
            Solarsystem.x_2.append(planets[2].position[0])
            Solarsystem.y_2.append(planets[2].position[1])
            Solarsystem.x_3.append(planets[3].position[0])
            Solarsystem.y_3.append(planets[3].position[1])
            Solarsystem.x_4.append(planets[4].position[0])
            Solarsystem.y_4.append(planets[4].position[1])
            Solarsystem.x_5.append(planets[5].position[0])
            Solarsystem.y_5.append(planets[5].position[1])
            Solarsystem.x_6.append(planets[6].position[0])
            Solarsystem.y_6.append(planets[6].position[1])
            Solarsystem.x_7.append(planets[7].position[0])
            Solarsystem.y_7.append(planets[7].position[1])
            Solarsystem.x_8.append(planets[8].position[0])
            Solarsystem.y_8.append(planets[8].position[1])
            Solarsystem.x_9.append(planets[9].position[0])
            Solarsystem.y_9.append(planets[9].position[1])

        np.save("planet_data", Solarsystem.Data, allow_pickle=True)    
                       
    def ke_solar(self, planets):
        self.kinetic_energy = 0

        '''Loop used to calculate the sum of the kinetic energy of each body'''

        for body in planets:
            self.kinetic_energy += 0.5*body.mass*np.dot(body.velocity, body.velocity)
        
        return self.kinetic_energy

    def pe_solar(self, planets):
        self.potential_energy = 0

        '''Loop used to calculate the sum of the potential energy of each body'''

        for first_body in planets:
            for second_body in planets:
                if first_body != second_body:
                    vector2 = second_body.position - first_body.position
                    vector_mag2 = np.dot(vector2, vector2)
                    
                    self.potential_energy += -Particle.G*first_body.mass*(second_body.mass/math.sqrt(vector_mag2))
        
        #Potential energy is halved to account for the potential energy between two bodies being calculated twice 

        return self.potential_energy/2
    
    def energy_conservation(self):
        self.total_energy = 0

        '''Sums up the potential and kinetic energy of the system'''

        self.total_energy = self.kinetic_energy + self.potential_energy
        
        return self.total_energy
        
    def momentum_solar(self, planets):
        self.momentum = 0
        momentum_vector = 0

        '''Loop used to calculate the sum of the momentum of each body'''

        for body in planets:
            momentum_vector += body.mass*body.velocity

        '''The magnitude of the momentum is calculated'''    
            
        self.momentum = math.sqrt(np.dot(momentum_vector, momentum_vector))
        
        return self.momentum
    
            
        


