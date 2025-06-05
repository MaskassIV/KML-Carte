import os
import glob
from nettoyage import nettoyer
from simplifiage import simplifier
from coloriage import colorier
from zoommage import zoom
from repartissage_par_ville import repartir_par_ville
from creation_master import creer_master

def main():
    nomDossier="modifie"
    if os.path.exists(nomDossier+"/"):
        pattern = "N_S_C_Z*"
        fichiers = glob.glob(os.path.join("/", pattern))
        for fichier in fichiers:
            if os.path.isfile(fichier):
                os.remove(fichier)
                print(f"Supprimé : {fichier}")
            else:
                print(f"Ignoré (pas un fichier) : {fichier}")
    if not os.path.exists(nomDossier):
        os.makedirs(nomDossier)
    cheminFichier="./"+nomDossier+"/"
    option_nom_fichier=""
    option_nom_fichier=nettoyer(cheminFichier, option_nom_fichier)
    option_nom_fichier=simplifier(cheminFichier, option_nom_fichier)
    option_nom_fichier=colorier(cheminFichier, option_nom_fichier)
    option_nom_fichier=zoom(cheminFichier, option_nom_fichier)
    creer_master(cheminFichier, repartir_par_ville(cheminFichier, option_nom_fichier))
main()

