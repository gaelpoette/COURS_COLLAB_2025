# BNR = Base de Non Regression
import os

list_cas_bnr=["premier_test"]

for cas in list_cas_bnr: 
    os.chdir(cas)
    os.system("cp param.py ../..")
    os.system("python3 ../../ode_mc.py")
    os.chdir("..")
