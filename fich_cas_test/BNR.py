import os
import platform

# Fonction pour vérifier si l'on est sous Windows
def is_windows():
    return platform.system() == "Windows"

# Liste des cas de tests
list_cas_bnr = ["premier_test"]

for cas in list_cas_bnr:

    os.chdir(cas)

    # Vérification de l'OS et exécution des commandes adaptées
    if is_windows():
        # Commandes adaptées pour Windows
        os.system("copy param.py ..\\..")  # Copie le fichier
        os.system("python ..\\..\\ode_mc.py")  # Exécution du script Python
        # Comparaison des fichiers sous Windows (utilisation de `fc`)
        os.system("fc rez.txt rez_ref.txt > listing")
        print("si la commande renvoie 0, pas de différences")

    else:
        # Commandes adaptées pour Linux
        os.system("cp param.py ../../")  # Copie le fichier
        os.system("python3 ../../ode_mc.py")  # Exécution du script Python
        print("si la commande renvoie 0, pas de différences")
        os.system("diff rez.txt rez_ref.txt > listing")
        print("si la commande renvoie 0, pas de différences")


    # Compter le nombre de lignes dans 'listing' selon l'OS
    if is_windows():
        # Equivalent de `wc -l` sous Windows  
        os.system("findstr /R /N \"^\" listing | find /C \":\"")  ##je suis pas sur de mon coup (Jules BAILLY)
    else:
        os.system("wc -l listing")  # Commande classique sous Linux

    os.chdir("..") ##on retourne dans le bon répertoire
