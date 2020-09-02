from Particle import Particle
from solarsystem import Solarsystem
import math
import numpy as np
import matplotlib.pyplot as plt

Solar_System_Barycenter = Particle(np.array([0,0,0]), np.array([0,0,0]), np.array([0,0,0]), 'Barycenter', 0)

Sun = Particle(np.array([-5.217948483946839E+05,1.122927457583037E+06 ,2.164893775248202E+03]), np.array([-1.460193491074302E-02,-2.756517382683237E-03 ,4.010601089178227E-04]), np.array([0,0,0]),'Sun', 1988500e24  )
Mercury = Particle(np.array([-3.225630319989858E+07,3.843744661155364E+07,5.962470156148816E+06]), np.array([-4.698103732981682E+01,-2.962972815092206E+01, 1.887933415931773E+00]), np.array([0,0,0]),'Mercury', 3.302e23)
Venus = Particle(np.array([6.266377586742614E+07,-8.747972570979783E+07,-4.859843569222413E+06]), np.array([2.826573457861653E+01 ,2.020906859557348E+01,-1.354242909503058E+00]), np.array([0,0,0]),'Venus', 48.685e23)
Earth = Particle(np.array([6.850966054318315E+07,1.316880510298678E+08,-4.336026153817773E+03]), np.array([-2.684376539332143E+01, 1.381778696700259E+01, 4.301792636951518E-04]), np.array([0,0,0]),'Earth', 5.97237e24)
Mars = Particle(np.array([-2.336811620164938E+08,-6.815625038929862E+07,4.271181428871278E+06]), np.array([7.790134385215917E+00,-2.115679943888651E+01,-6.343717441293730E-01]), np.array([0,0,0]),'Mars',  6.4171e23)
Jupiter = Particle(np.array([3.700221560952756E+07,-7.820168895686439E+08,2.415435218444586E+06]), np.array([1.289190521233427E+01,1.240252706800405E+00,-2.935415912257169E-01]), np.array([0,0,0]),'Jupiter',  1898.13e24)
Saturn = Particle(np.array([5.405050362326692E+08,-1.399680194133316E+09,2.820550728889644E+06]), np.array([ 8.477417288330154E+00,3.450549539916355E+00,-3.972549893760313E-01]), np.array([0,0,0]),'Saturn', 5.6834e26)
Uranus = Particle(np.array([ 2.439335598861610E+09,1.686544186789459E+09,-2.533800967612743E+07]), np.array([-3.922805031285065E+00,5.284140851427575E+00, 7.053796736975060E-02]), np.array([0,0,0]),'Uranus', 86.813e24)
Neptune = Particle(np.array([4.370483460001080E+09,-9.684795681276726E+08,-8.077812313342243E+07]), np.array([1.140613451220905E+00, 5.339076558600304E+00,-1.366279308625291E-01]), np.array([0,0,0]),'Neptune', 102.413e24)
Pluto = Particle(np.array([1.924259786274985E+09,-4.694715075935009E+09,-5.424551647992468E+07]), np.array([5.166512500902988E+00,9.243464545862123E-01,-1.581796543438907E+00]), np.array([0,0,0]),'Pluto', 1.307e22) #date correct as of 2019-Nov-25 00:00:00.0000 TDB

bodies = [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]

n_bodies = Solarsystem(bodies, 0, 0, 0, 0, 1)

n_bodies.simulation(bodies)

figure_ke = plt.figure()
plt.plot(Solarsystem.time_list, Solarsystem.KineticEnergy)
plt.title('kinetic energy')
plt.xlabel('Time')
plt.ylabel('Kinetic energy')

figure_pe = plt.figure()
plt.plot(Solarsystem.time_list, Solarsystem.PotentialEnergy)
plt.title('Potential energy')
plt.xlabel('Time')
plt.ylabel('Potential energy')

figure_tot = plt.figure()
plt.plot(Solarsystem.time_list, Solarsystem.TotalEnergy)
plt.title('Total energy')
plt.xlabel('Time')
plt.ylabel('Total energy')
plt.ylim(0, 2*Solarsystem.TotalEnergy[0])
print(Solarsystem.TotalEnergy[0], Solarsystem.TotalEnergy[-1])

figure_mom = plt.figure()
plt.plot(Solarsystem.time_list, Solarsystem.Momentum)
plt.title('Magnitude of the linear momentum')
plt.xlabel('Time')
plt.ylabel('Total magnitude of linear momentum')
plt.ylim(0,2*Solarsystem.Momentum[0])
print(Solarsystem.Momentum[0], Solarsystem.Momentum[-1])

figure_sim = plt.figure()
plt.plot(Solarsystem.x, Solarsystem.y, label='Sun')
plt.plot(Solarsystem.x_1, Solarsystem.y_1, label='Mercury')
plt.plot(Solarsystem.x_2, Solarsystem.y_2, label='Venus') 
plt.plot(Solarsystem.x_3, Solarsystem.y_3, label='Earth')
plt.plot(Solarsystem.x_4, Solarsystem.y_4, label='Mars')
plt.plot(Solarsystem.x_5, Solarsystem.y_5, label='Jupiter')
plt.plot(Solarsystem.x_6, Solarsystem.y_6, label='Saturn')
plt.plot(Solarsystem.x_7, Solarsystem.y_7, label='Uranus')
plt.plot(Solarsystem.x_8, Solarsystem.y_8, label='Neptune')
plt.plot(Solarsystem.x_9, Solarsystem.y_9, label='Pluto')
plt.title('Solarsystem Simulation')
plt.legend()
plt.show()




    






