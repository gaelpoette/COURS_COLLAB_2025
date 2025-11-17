#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from math import *
from string import *
import os
import random


# importation des paramètres
from param import *

print("liste des reactions")
print(list_reac)
if (not(len(list_reac)==len(list_sigr))):
  print("ATTENTION! LES LISTES DOIVENT AVOIR LA MEME TAILLE!")
  exit(1)

# ============================================================
# 1. Préparation des espèces et conditions initiales
# ============================================================

def get_species(list_reac):
    compos=[]
    for i in range(len(list_reac)): 
        compos_reac=(list_reac[i].split(' '))
        for j in range(len(compos_reac)):
            if not(compos_reac[j] in compos):
                compos.append(compos_reac[j])
    return compos


def initial_eta(compos, vol):
    eta = {}
    for c in compos:
        eta[c] = vol if c in ["Ar", "e^-"] else 0.
    return eta

# ============================================================
# 2. Construction des vecteurs h et nu
# ============================================================

def build_reactants_and_stoechiometry(list_reac, list_type, compos):
    h = {}
    nu = {}

    for i in range(len(list_reac)):
        reac = list_reac[i].split(" ")

        # définition des réactifs selon le type
        if list_type[i] == "binaire":
            h[i] = [reac[0], reac[1]]
        elif list_type[i] == "unaire":
            h[i] = [reac[0]]
        else:
            raise ValueError("Type de réaction inconnu")

        # stoechiométrie
        nu[i] = {}
        for cg in compos:
            nu[i][cg] = 0.
            num = 0
            for c in reac:
                isnum = (num < len(h[i]))  # indices des réactifs
                if c == cg:
                    nu[i][cg] += -1. if isnum else 1.
                num += 1

    return h, nu

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


# ============================================================
# 4. Simulation Monte Carlo
# ============================================================

def compute_total_sigma(pmc, h, list_sigr, list_type, vol):
    sig = 0.
    for i in range(len(list_sigr)):
        prod = 1.
        for H in h[i]:
            prod *= pmc["densities"][H]

        exposant = 0 if list_type[i] == "unaire" else 1
        volr = vol ** exposant

        sig += list_sigr[i] * prod / volr
    return sig

def choose_reaction(pmc, sig, h, list_sigr, list_type, vol):
    U = random.random()
    proba = 0.

    for i in range(len(list_sigr) - 1):
        prod = 1.
        for H in h[i]:
            prod *= pmc["densities"][H]

        exposant = 0 if list_type[i] == "unaire" else 1
        volr = vol ** exposant
        proba += list_sigr[i] * prod / volr

        if U * sig < proba:
            return i

    return len(list_sigr) - 1


def simulate_step(PMC, eta, compos, h, nu, list_reac, list_type, list_sigr, vol, dt):

    # initialisation du tableau de tallies
    for c in compos:
        eta[c] = 0.

    for pmc in PMC:

        tps_cur = 0.

        while tps_cur < dt:

            sig = 0.
            for i in range(len(list_reac)):
                prod = 1.
                for H in h[i]:
                    prod *= pmc["densities"][H]

                exposant = 1
                if list_type[i] == "unaire":
                    exposant = 0
                volr = vol ** exposant
                sig += list_sigr[i] / volr * prod

            # tirage du temps de la prochaine reaction
            U = random.random()
            tau = 1.e32
            if sig > 0.:
                tau = -log(U) / sig

            # temps courant updaté
            tps_cur += tau

            # détermination de l'événement que la pmc va subir
            if tps_cur > dt:  
                # census
                tps_cur = dt
                for c in compos:
                    eta[c] += pmc["densities"][c] * pmc["weight"]

            else:
                # réaction
                U = random.random()

                reac = len(list_reac) - 1
                proba = 0.

                for i in range(len(list_reac) - 1):
                    prod = 1.
                    for H in h[i]:
                        prod *= pmc["densities"][H]

                    exposant = 1
                    if list_type[i] == "unaire":
                        exposant = 0
                    volr = vol ** exposant
                    proba += list_sigr[i] / volr * prod

                    if U * sig < proba:
                        reac = i
                        break

                for c in compos:
                    pmc["densities"][c] += nu[reac][c]
    

def simulate(PMC, eta, compos, temps, temps_final, h, nu, list_sigr, list_type, vol):

    tps = 0.
    it = 0

    cmd = "\n#temps " + " ".join(compos) + "\n"
    cmd += f"{tps} " + " ".join(str(eta[c] / vol) for c in compos)

    while tps < temps_final:

        if it + 1 >= len(temps):
            print("Erreur : tableau temps trop court.")
            break

        dt = temps[it + 1] - temps[it]

        # Appel au simulation en une step de temps 
        simulate_step(PMC, eta, compos, h, nu, list_reac, list_type, list_sigr, vol, dt)

        # mise à jour temps
        tps += dt

        # stockage des valeurs
        cmd += "\n" + str(tps) + " " + " ".join(str(eta[c] / vol) for c in compos)

        it += 1

    return cmd

# ============================================================
# 5. Export des résultats
# ============================================================

def write_results(cmd):
    with open("rez.txt", "w") as f:
        f.write(cmd)


def write_gnuplot(compos):
    cmd_gnu = "set sty da l; set grid; set xl 'time'; set yl 'densities'; plot "
    cmd_gnu += "'rez.txt' lt 1 w lp t '" + compos[0] + "'"

    for i in range(1, len(compos)):
        cmd_gnu += f", '' u 1:{i+2} lt {i+1} w lp t '{compos[i]}'"

    cmd_gnu += "; pause -1"

    with open("gnu.plot", "w") as f:
        f.write(cmd_gnu)
        


# ============================================================
# 6. MAIN
# ============================================================

def main():
    print("liste des reactions")
    print(list_reac)

    if len(list_reac) != len(list_sigr):
        print("ATTENTION! tailles incohérentes !")
        return

    compos = get_species(list_reac)
    print("liste des espèces")
    print(compos)

    eta = initial_eta(compos, vol)
    print("conditions initiales")
    print(eta)

    h, nu = build_reactants_and_stoechiometry(list_reac, list_type, compos)

    PMC = init_PMC(Nmc, compos, eta)

    print("\nDébut du calcul...")
    cmd = simulate(PMC, eta, compos, temps, temps_final, h, nu, list_sigr, list_type, vol)

    write_results(cmd)
    write_gnuplot(compos)

    os.system("gnuplot gnu.plot")


if __name__ == "__main__":
    main()

