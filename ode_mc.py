#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import *
from string import *
import os
import random
import matplotlib.pyplot as plt


random.seed(42)


# importation des paramètres
import json



# ============================================================
# 3. Initialisation de la population PMC
# ============================================================

def init_PMC(Nmc, compos, eta):
    PMC = []
    for _ in range(Nmc):
        w = 1.0 / Nmc
        PMC.append({
            "weight": w,
            "densities": {c: eta[c] for c in compos}
        })
    return PMC



with open("param.json", "r") as f:
    params = json.load(f)

Nmc = params["Nmc"]
vol = params["vol"]
temps_final = params["temps_final"]
dt = params["dt"]
t = params["t"]
list_reac = params["list_reac"]
list_type = params["list_type"]
sig_r_0 = params["sig_r_0"]
sig_r_1 = params["sig_r_1"]
sig_r_2 = params["sig_r_2"]
eta = params["eta"]
list_sigr = {0 : sig_r_0, 1 : sig_r_1, 2 : sig_r_2}
temps=[]

for i, s in list_sigr.items():
    if s < 0:
        print(f"ERREUR : constante de réaction négative pour la réaction {i} : {s}")
        exit(10)

Nt = int(temps_final/dt)

for it in range(Nt):
    temps.append(t)
    t+=dt

print("liste des reactions")
print(list_reac)
if (not(len(list_reac)==len(list_sigr))):
  print("ATTENTION! LES LISTES DOIVENT AVOIR LA MEME TAILLE!")
  exit(1)

# lecture de la liste des compositions des réactions
print("travail sur list_type")
list_type=[]
compos=[]
print(list_reac)
for i in range(len(list_reac)): 
  compos_reac=(list_reac[i].split(' '))
  #print(compos_reac)
  for j in range(len(compos_reac)-1):
    if compos_reac[1] == "=":
        del compos_reac[1] 
        list_type.append("unaire")
    if compos_reac[2] == "=":
        del compos_reac[2] 
        list_type.append("binaire")
    if not(compos_reac[j] in compos):
       compos.append(compos_reac[j])
       #print(compos)
print("liste des especes")
print(compos)

#"conditions initiales en eta codée en dur pour l'instant
if  eta == {} :
    print("Erreur de taille dans la liste des concentrations")
    eta={}
    for c in compos:
        print("Choisir la concentration initiale de ",c, ':')
        eta[c]=float(input( ))

print("conditions initiales des espèces")
print(eta)

h={}
nu={}
for i in range(len(list_reac)):
    print("\n num de reaction = "+str(i)+"")
    reac = list_reac[i]
    compos_reac = (reac.split(' '))
    print(reac, compos_reac)
    # recuperation du vecteur des reactifs
    print("type de reaction: "+list_type[i]+"")

    isnum=0
    if list_type[i] == "binaire":
          h[i] = [compos_reac[0], compos_reac[1]]
    elif list_type[i] == "unaire":
          h[i] = [compos_reac[0]]
    else:
          print("type de reaction non reconnue")
          exit(2)

    #recuperation des vecteurs de coefficients stoechiométriques pour chaque reactions
    nu[i]={}
    #print compos
    for cg in compos:
        nu[i][cg] = 0.
        num = 0
        for c in compos_reac:
          isnum=0
          if list_type[i] == "binaire":
              isnum = (num == 0 or num == 1)
          if list_type[i] == "unaire":
              isnum = (num == 0)
          if c == cg and (isnum): #réactions à 2 réactifs
              nu[i][cg] += -1.
          if c == cg and (not isnum): #réactions à 2 réactifs
              nu[i][cg] +=  1.
          else:
              nu[i][cg] +=  0.
          num+=1
print("\nles listes de réactifs (h) pour chaque reaction")
print(h)
print("les coefficients stoechiométriques (nu) pour chaque reaction")
print(nu)
# population de particules représentant la condition initiale
PMC = init_PMC(Nmc, compos, eta)

#entete du fichier
cmd="\n"+"#temps"+" "
for c in compos:
 cmd+=str(c)+" "

it=0
tps = 0.
cmd+="\n"+str(tps)+" "
for c in compos:
 cmd+=str(eta[c]/vol)+" "

print("\n début du calcul")

while tps < temps_final:

  dt = temps[it+1]-temps[it]

  # initialisation du tableau de tallies
  for c in compos:
      eta[c] = 0.

  for pmc in PMC:
    
      tps_cur = 0.

      while tps_cur < dt:

          # section efficace totale
          sig = 0.
          for i in range(len(list_reac)):
              prod = 1.
              for H in h[i]:
                  prod *= pmc["densities"][H]

              exposant = 1
              if list_type[i] == "unaire":
                  exposant = 0
              volr = vol **exposant
              sig+= list_sigr[i] / volr * prod

          #tirage du temps de la prochaine reaction
          U = random.random()
          tau = 1.e32
          if sig > 0.:
              tau = - log(U) / sig

          # temps courant updaté
          tps_cur += tau

          # détermination de l'évenement que la pmc va subir
          if tps_cur > dt:
              #census
              tps_cur = dt
              for c in compos:
                  eta[c] += pmc["densities"][c] * pmc["weight"]

          else:
              #reaction
              U = random.random()

              reac = len(list_reac)-1
              proba = 0.
              for i in range(len(list_reac)-1):
                  prod = 1.
                  for H in h[i]:
                      prod *= pmc["densities"][H]

                  exposant = 1
                  if list_type[i] == "unaire":
                      exposant = 0
                  volr = vol **exposant
                  proba+= list_sigr[i] / volr * prod

                  if U * sig < proba:
                      reac = i
                      break

              for c in compos:
                  pmc["densities"][c]+=nu[reac][c]

  tps+=dt
  cmdt=""+str(tps)+" "
  for c in compos:
   cmdt+=str(eta[c] / vol)+" "
  cmd+="\n"+cmdt

output = open("rez.txt",'w')
output.write(cmd)
output.close()

#ancienne version 


#----------------

# cmd_gnu="set sty da l;set grid; set xl 'time'; set yl 'densities of the species'; plot "
# i=3
# cmd_gnu+="'rez.txt' lt 1 w lp  t '"+str(compos[0])+"'"
# for c in compos:
#    if not(c==compos[0]):
#      cmd_gnu+=",'' u 1:"+str(i)+" lt "+str(i)+" w lp t '"+str(compos[i-2])+"'"
#      i+=1

# cmd_gnu+=";pause -1"
# output = open("gnu.plot",'w')
# output.write(cmd_gnu)
# output.close()

# os.system("gnuplot gnu.plot")


#----------------------

# nouvelle visualisation avec matplotlib

#-------------------


# On lit les résultats depuis rez.txt
times = []
densities = {c: [] for c in compos}

with open("rez.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # on saute les lignes de commentaires et les lignes vides

        parts = line.split()
        t = float(parts[0])
        times.append(t)

        # les densites sont ensuite dans le meme ordre que la liste 'compos'
        for i, c in enumerate(compos):
            densities[c].append(float(parts[i + 1]))

# matplotlib
plt.figure(figsize=(10, 6))
for c in compos:
    plt.plot(times, densities[c], label=c)

plt.xlabel("time")
plt.ylabel("densities of the species")
plt.title("evolution des densites (methode MC)")
plt.grid(True)
plt.legend()
plt.tight_layout()

# sauvegarder 
plt.savefig("densites_matplotlib.png", dpi=150)
print("figure sauvée dans 'densites_matplotlib.png'")

plt.show() # affichage en local

#----------------------------------




