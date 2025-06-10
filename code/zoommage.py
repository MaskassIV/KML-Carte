import os
import re
from fichiers import file_name

def zoom(chemin_fichier, option_nom_fichier):
    for nom_fichier in os.listdir(chemin_fichier):
        if "Z_" in nom_fichier:
                chemin_fichier = os.path.join(chemin_fichier, nom_fichier)
                if os.path.isfile(chemin_fichier):
                    os.remove(chemin_fichier)
                    print(f"Supprimé : {chemin_fichier}")
    option_nom_fichier_bis=option_nom_fichier+"Z_"
    for nom_fichier in file_name:
        if  os.path.exists(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml"):
            with open(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        else:
            with open(option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        lignes = iter(lignes)
        lignes_zoomees = []
        index = -1
        puissance_zoom = 100
        for ligne in lignes:
            if "</ExtendedData>" in ligne:
                index = len(lignes_zoomees)
            if "<coordinates>" in ligne:
                north, south, east, west = calculer_box(ligne)
                lignes_zoomees.insert(index+1, "\t<Region>\n\t\t<LatLonAltBox>\n\t\t\t<north> "+str(north)+" </north>\n\t\t\t<south> "+str(south)+" </south>\n\t\t\t<east> "+str(east)+" </east>\n\t\t\t<west> "+str(west)+" </west>\n\t\t</LatLonAltBox>\n\t\t<Lod>\n\t\t\t<minLodPixels>"+str(puissance_zoom)+"</minLodPixels>\n\t\t\t<maxLodPixels>-1</maxLodPixels>\n\t\t</Lod>\n\t</Region>\n" )
                index=-1
            lignes_zoomees.append(ligne)

        with open(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "w", encoding="utf-8") as p:
            p.writelines(lignes_zoomees)
        os.rename(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", chemin_fichier+option_nom_fichier_bis+"parcelle_13_"+nom_fichier+".kml")
        print("Zoom termine pour "+nom_fichier)
    return option_nom_fichier_bis


  
def calculer_box(ligne):
    pattern = r'(-?\d+\.\d+),(-?\d+\.\d+)'
    longitudes = []
    latitudes = []

    matches = re.findall(pattern, ligne)
    
    if matches:
        for lon_str, lat_str in matches:
            longitudes.append(float(lon_str))
            latitudes.append(float(lat_str))
        
        return max(latitudes), min(latitudes), max(longitudes), min(longitudes)
        # Ordre : North, South, East, West
    else:
        print("Pas de position à récupérer")
        exit()