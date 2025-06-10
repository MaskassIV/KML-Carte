import os
import re
from fichiers import file_name

def repartir_par_ville(chemin_fichier, option_nom_fichier):
    villes_box = {}
    for nom_fichier in file_name:
        if os.path.exists(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml"):
            with open(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        else:
            with open(option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        lignes = iter(lignes)
        intro = []
        outro = ["</Folder></Document></kml>"]
        villes = {}
        nom_ville=""
        for ligne in lignes :
            if "Placemark" in ligne:
                break
            else:
                intro.append(ligne)
        for ligne in lignes:
                if "<Placemark" in ligne:
                    bloc = []
                    bloc.append(ligne)
                    for ligne_bloc in lignes :
                        if "</Placemark>" not in ligne_bloc:
                            if "<SimpleData" in ligne_bloc:
                                match = re.search(r'<SimpleData name="Commune">(.*?)</SimpleData>', ligne_bloc)
                                if match:
                                    nom_ville= match.group(1)
                                else:
                                    nom_ville = "Pas de ville"
                                    print(">> Pas de match")
                            if "<north>" in ligne_bloc or "<south>" in ligne_bloc or "<east>" in ligne_bloc or "<west>" in ligne_bloc :
                                if nom_ville:
                                    calculer_box_ville(ligne_bloc, villes_box, nom_ville)
                            bloc.append(ligne_bloc)
                        else:
                            bloc.append(ligne_bloc)
                            break
                    if nom_ville:
                        if nom_ville not in villes:
                            villes[nom_ville] = []
                        villes[nom_ville].extend(bloc)
        os.makedirs("./modifie/"+nom_fichier, exist_ok=True)
        for ville in villes:
            with open(chemin_fichier+nom_fichier+"/"+nom_fichier+"_"+ville+".kml", "w", encoding="utf-8") as p:
                p.writelines(modifier_intro(intro, ville, nom_fichier))
                for bloc in villes.get(ville):
                    p.writelines(bloc)
                p.writelines(outro)
        print("Fichier par ville termine pour "+ nom_fichier)
    return villes_box


def calculer_box_ville(ligne_bloc, villes_box, nom_ville):
    match = re.search(r"<(\w+)>\s*([\d\.\-]+)\s*</\1>", ligne_bloc)
    if match:
        point_cardinal = match.group(1)     # north, south, east, west
        match point_cardinal:
            case "north":
                if not nom_ville in villes_box:
                    villes_box[nom_ville]=[]
                    villes_box[nom_ville]=[(float(match.group(2)))]
                elif villes_box[nom_ville][0] < float(match.group(2)):
                    villes_box[nom_ville][0] = float(match.group(2))
            case "south":
                if len(villes_box[nom_ville])<2:
                    villes_box[nom_ville].append(float(match.group(2)))
                elif villes_box[nom_ville][1] > float(match.group(2)):
                    villes_box[nom_ville][1] = float(match.group(2))
            case "east":
                if len(villes_box[nom_ville])<3:
                    villes_box[nom_ville].append(float(match.group(2)))
                elif villes_box[nom_ville][2] < float(match.group(2)):
                    villes_box[nom_ville][2] = float(match.group(2))
            case "west":
                if len(villes_box[nom_ville])<4:
                    villes_box[nom_ville].append(float(match.group(2)))
                elif villes_box[nom_ville][3] > float(match.group(2)):
                    villes_box[nom_ville][3] = float(match.group(2))

def modifier_intro(intro, ville, nom_fichier):
    lignes_modifiees = []
    for ligne in intro:
        if ligne.strip().startswith('<Schema name='):
            ligne = re.sub(r'name="[^"]+"', f'name="{ville+"_"+nom_fichier}"', ligne)
            ligne = re.sub(r'id="[^"]+"', f'id="{ville+"_"+nom_fichier}"', ligne)
        lignes_modifiees.append(ligne)
    return lignes_modifiees

