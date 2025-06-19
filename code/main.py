import os
import glob
from nettoyage import nettoyer
from simplifiage import simplifier
from coloriage import colorier
from zoommage import zoom
from repartissage_par_ville import repartir_par_ville
from creation_master import creer_master
from suppression_fichier import nettoyage_final
from altitude import mise_en_hauteur
from departements import liste_departements
from fichiers import file_name

def main():
    nom_dossier="initial"
  #  for :
        # if os.path.exists(nom_dossier+"/"):
        #     pattern = "N_S_C_Z*"
        #     fichiers = glob.glob(os.path.join("/", pattern))
        #     for fichier in fichiers:
        #         if os.path.isfile(fichier):
        #             os.remove(fichier)
        #             print(f"Supprimé : {fichier}")
        #         else:
        #             print(f"Ignoré (pas un fichier) : {fichier}")
    if not os.path.exists(nom_dossier):
        os.makedirs(nom_dossier)
    chemin_fichier="./"+nom_dossier+"/"
    print("chemin : "+chemin_fichier)
    for departement in liste_departements:
        print("début departement : "+str(departement))
        for fichier in file_name:
            print("debut fichier : "+fichier)
            if os.path.exists(chemin_fichier+"/"+str(departement)+"parcelle_"+str(departement)+"_"+fichier+".kml"):
                with open(chemin_fichier+"parcelle_"+str(departement)+"_"+fichier+".kml", "r", encoding="utf-8") as f:
                    lignes = f.readlines()
            else:
                with open("parcelle_"+str(departement)+"_"+fichier+".kml", "r", encoding="utf-8") as f:
                    lignes = f.readlines()
            lignes=zoom(colorier(simplifier(nettoyer(lignes))))
            with open(chemin_fichier+"parcelle_"+str(departement)+"_"+fichier+"_test.kml", "w", encoding="utf-8") as p:
                p.writelines(lignes)

   # creer_master(chemin_fichier, repartir_par_ville(chemin_fichier, option_nom_fichier))
    #mise_en_hauteur(chemin_fichier)
    #nettoyage_final(chemin_fichier, option_nom_fichier)
main()
