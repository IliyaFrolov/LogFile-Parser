Particle.py:

The particle.py file contains the 'particle' class. This class's function is to create bodies which are instances of the class. It also
contains two methods, one for running the Euler method and one for running the Euler-Cromer method. This file does not need to be touched
in order to run the simulation.

solarsystem.py:

This file contains the 'solarsystem' class. This class takes in a list comprised of bodies and outputs a system which is the instance of the
class. It has methods responsible for calculating the acceleration, kinetic, potential and total energy as well as linear momentum of the system.
Withtin the 'simulation' method, the step range can be set by adjusting the second arguemenn of the range function. The time step can also be 
adjusted by changing the value of the global variable defined as 'delta'. 

test.py:

This is the main file used to run the simulation. Within this file you will find a list of bodies at the top, as well as a variable defined as 
'n_bodies'. This variable becomes an instance of the solarsystem class, the last arguement of the variable can be set to either a 1 or a 2. 
A value of 1 will set it so that the simulation runs with the Euler method, and a value of 2 sets it so it runs with the Euler-Cromer method. 
The code below all this plots the simulation as well as the graphs for the analysis.