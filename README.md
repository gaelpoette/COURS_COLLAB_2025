# COURS_COLLAB_REAC - Résolution de l'équation cinétique chimique principale avec un schéma de Monte Carlo.

 - auteurs : GAEL POETTE et la promotion 2025-2026 développement de codes collaboratif

Fichier éxécutable : ode_mc.py

## Général

Dans ce répertoire, on retrouve un code de cinétique chimique résolu par méthode MC, la documentation associée et les paramètres d'un cas test.

Le code permet de résoudre pour 3 types de réacitons : 
 - Les réactions unaires.
 - Les réactions binaires.
 - Les réactions ternaires.

# Documentation

Un jupyternotebook ode_reac.ipynb sert de documentation, il contient :
 - une simple description de la cinétique chimique. 
 - L'ODE qui construite et résolue.
 - Les données d'entrées.
 - Les développements réalisés

# fich_cas_test

Dans ce dossier on retrouve l'ensemble des tests qui permettent d'attester du bon foncitonnement du code
## premier_test
### param.py
Fichier python contenant le jeu de paramètre du test 1
###rez_ref.txt
Fichier contenant les résultats obtenus.

### Résultats attendus 
ATTENTION : pour obtenir le graphique attendu il faut absolument vérifier que dans ode_mc.py ligne 9 il y a "random.seed(42)"



##BNR.py



# TESTS
pour tester, lancer la commande
python BNR.py 
dans fich_cas_test

TODO (idée pour améliorer le code)
- faire un readme digne de ce nom                                                              => Jules 
- Conditions initiales en dur. Pas fou ça                                                      => Younoussa
- constante de réactions négatives                                                             => Justin
- encapsulation de certaines fonctions                                                         => Ilias
- un seul .py... En faire plus? 
- Pas de base de non regression                                                                => Gael
- réactions ternaires                                                                          => Camille
- type de réaction et reactions = redondant                                                    => Thomas
- regle de codage: pas de document "règle de codage"... Et mauvaise pratique identifiées
- il existe des variables dont le nom n'est qu'un caractère                                    => Zineb
- fichier de param en python... Bof bof. ça pourrait être du txt, du json, du yaml             => Samuel
- est ce qu'on resout vraiment les bonnes equations?
- gnuplot pour la visu = bof, utilisons matplotlib                                             => Saad
- IHM
