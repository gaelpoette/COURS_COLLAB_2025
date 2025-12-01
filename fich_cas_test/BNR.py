# BNR = Base de Non Regression
import os

list_cas_bnr=["premier_test"]

for cas in list_cas_bnr: 
    os.chdir(cas)
    os.system("cp param.json ../..")
    os.system("python3 ../../ode_mc.py")
    os.system("diff rez.txt rez_ref.txt > listing")
    print("si la commande renvoie 0, pas de différences")
    os.system("wc -l listing")
    os.chdir("..")
