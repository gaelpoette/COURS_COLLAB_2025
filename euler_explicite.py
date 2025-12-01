import numpy as np
from math import * 
from scipy import stats
import matplotlib.pyplot as plt

#paramètres
sigma = 1
# PARAM: Volume
vol = 10.
# PARAM: construction de la liste des temps d'intérêt
temps_final = 30
dt=1
Nt = int(temps_final/dt)
t=[]
t0=0.
for it in range(Nt):
    t.append(t0)
    t0+=dt

#réaction : "e^-+ A+ B -> K + L"

#initialisation de la concentration
c_e =  np.zeros(len(t))
c_A =  np.zeros(len(t))
c_B =  np.zeros(len(t))
c_K =  np.zeros(len(t))
c_Z =  np.zeros(len(t))

c_e[0]=vol
c_A[0]=vol
c_B[0]=vol


#euler explicite
for n in range(len(t)-1):
    c_e[n+1]= c_e[n] - dt*sigma/(vol**2)*c_e[n]*c_A[n]*c_B[n]
    c_A[n+1]= c_A[n] - dt*sigma/(vol**2)*c_e[n]*c_A[n]*c_B[n]
    c_B[n+1]= c_B[n] - dt*sigma/(vol**2)*c_e[n]*c_A[n]*c_B[n]
    c_K[n+1]= c_K[n] + dt*sigma/(vol**2)*c_e[n]*c_A[n]*c_B[n]
    c_Z[n+1]= c_Z[n] + dt*sigma/(vol**2)*c_e[n]*c_A[n]*c_B[n]
    
 


# Affichage
plt.plot(t, c_e, label='e-')
plt.plot(t, c_A, label='A')
plt.plot(t, c_B, label='B')
plt.plot(t, c_K, label='K')
plt.plot(t, c_Z, label='Z')

plt.xlabel('Temps')
plt.ylabel('Concentrations')
plt.title('Évolution des concentrations')
plt.legend()
plt.show()
