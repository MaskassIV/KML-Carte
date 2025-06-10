import os
import glob
from nettoyage import nettoyer
from simplifiage import simplifier
from coloriage import colorier
from zoommage import zoom
from repartissage_par_ville import repartir_par_ville
from creation_master import creer_master

def main():
    nom_dossier="modifie"
    if os.path.exists(nom_dossier+"/"):
        pattern = "N_S_C_Z*"
        fichiers = glob.glob(os.path.join("/", pattern))
        for fichier in fichiers:
            if os.path.isfile(fichier):
                os.remove(fichier)
                print(f"Supprimé : {fichier}")
            else:
                print(f"Ignoré (pas un fichier) : {fichier}")
    if not os.path.exists(nom_dossier):
        os.makedirs(nom_dossier)
    chemin_fichier="./"+nom_dossier+"/"
    option_nom_fichier=""
    option_nom_fichier=nettoyer(chemin_fichier, option_nom_fichier)
    option_nom_fichier=simplifier(chemin_fichier, option_nom_fichier)
    option_nom_fichier=colorier(chemin_fichier, option_nom_fichier)
    option_nom_fichier=zoom(chemin_fichier, option_nom_fichier)
    creer_master(chemin_fichier, repartir_par_ville(chemin_fichier, option_nom_fichier))
main()
