import os
import re
from fichiers import file_name

def simplifier(cheminFichier, option_nom_fichier):
    for nom_fichier in os.listdir(cheminFichier):
        if "S_" in nom_fichier:
                chemin_fichier = os.path.join(cheminFichier, nom_fichier)
                if os.path.isfile(chemin_fichier):
                    os.remove(chemin_fichier)
                    print(f"Supprimé : {chemin_fichier}")
    option_nom_fichier_bis=option_nom_fichier+"S_"
    for nom_fichier in file_name:
        if  os.path.exists(cheminFichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml"):
            with open(cheminFichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        else:
            with open(option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        lignes = iter(lignes)
        lignes_simplifiees = []
        for ligne in lignes:
            if "<coordinates>" in ligne:
                lignes_simplifiees.append(arrondir_coordonnees(ligne))
            else:
                lignes_simplifiees.append(ligne)
        with open(cheminFichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "w", encoding="utf-8") as p:
            p.writelines(lignes_simplifiees)
        os.rename(cheminFichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", cheminFichier+option_nom_fichier_bis+"parcelle_13_"+nom_fichier+".kml")
        print("Simplification termine pour "+nom_fichier)
    return option_nom_fichier_bis
        
def arrondir_coordonnees(ligne):
    pattern = r'(-?\d+\.\d+),(-?\d+\.\d+)'

    def replacer(match):
        lon, lat = match.groups()
        lon = round(float(lon), 6)

        lat = round(float(lat), 6)
 
        return f'{lon},{lat}'
    
    
    if re.search(pattern, ligne):
        line_modifiee = re.sub(pattern, replacer, ligne)
        return line_modifiee
    else:
        return ligne
    
