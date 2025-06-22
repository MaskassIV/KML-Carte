import os
import glob
import shutil
from nettoyage import nettoyer
from simplifiage import simplifier
from coloriage import colorier
from zoommage import zoom
from repartissage_par_ville import repartir_par_ville
from creation_master import creer_master
from altitude import mise_en_hauteur
from departements import liste_departements
from fichiers import file_name
from kml_to_kmz import kml_to_kmz_batch

def main():
    nom_dossier="initial"
    os.mkdir("./modifie/Brute")
    if not os.path.exists(nom_dossier):
        os.makedirs(nom_dossier)
    chemin_fichier="./"+nom_dossier+"/"
    print("chemin : "+chemin_fichier)
    villes_box = {}
    for departement in liste_departements:
        print("début departement : "+str(departement))
        for fichier in file_name:
            print("debut fichier : "+fichier)
            if os.path.exists(chemin_fichier+str(departement)+"/parcelle_"+str(departement)+"_"+fichier+".kml"):
                with open(chemin_fichier+str(departement)+"/parcelle_"+str(departement)+"_"+fichier+".kml", "r", encoding="cp1252") as f:
                    lignes = f.readlines()
                #lignes=colorier(simplifier(nettoyer(lignes, departement)), fichier)
                lignes=zoom(colorier(simplifier(nettoyer(lignes, departement)), fichier))
                with open("./modifie/Brute/parcelle_"+str(departement)+"_"+fichier+"_test.kml", "w", encoding="cp1252") as p:
                    p.writelines(lignes)
        villes_box.update(repartir_par_ville(departement))
    
    mise_en_hauteur("./modifie")
    
    shutil.rmtree('./modifie/Brute')
    kml_to_kmz_batch("./modifie")
    creer_master("./modifie", villes_box)

      
main()

# def remplacement():
#     with open("./initial/13/parcelle_13_personne_morale.kml", "r", encoding="cp1252") as f:
#         lignes = f.readlines()

#     lignes_modifiees = [ligne.replace("(3)", "13") for ligne in lignes]
#     # lignes=zoom(colorier(simplifier(nettoyer(lignes)), fichier))
#     with open("./initial/13/parcelle_13_personne_morale.kml", "w", encoding="cp1252") as p:
#         p.writelines(lignes_modifiees)

#       #  creer_master("./modifie", repartir_par_ville(departement))
#        # mise_en_hauteur("./modifie")
#remplacement()