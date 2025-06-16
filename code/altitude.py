import os
import re
from fichiers import file_name
from ville import villes

def mise_en_hauteur(chemin_fichier):
    for city in villes:
        print("ville : "+city)
        altitude=15
        affichage=False
        for fichier in file_name:
                if os.path.exists(chemin_fichier+fichier+"/"+fichier+"_"+city+".kml"):
                    affichage = True
                    with open(chemin_fichier+fichier+"/"+fichier+"_"+city+".kml", "r", encoding="utf-8") as f:
                        lignes = f.readlines()
                    lignes = iter(lignes)
                    lignes_elevees = []

                    for ligne in lignes :
                        if city == "MARSEILLE 2EME":
                            altitude = 30
                        if "<coordinates>" in ligne:
                            ligne=add_altitude_to_coordinates(ligne, altitude)
                        lignes_elevees.append(ligne)
                    with open(chemin_fichier+fichier+"/"+fichier+"_"+city+".kml", "w", encoding="utf-8") as p:
                        p.writelines(lignes_elevees)
        if affichage:
            print("Elevage en hauteur termine pour "+city)



def add_altitude_to_coordinates(ligne, altitude):
    match = re.search(r'<coordinates>(.*?)</coordinates>', ligne)
    if not match:
        return ligne  # Rien à faire
    coords_text = match.group(1).strip()
    coords = coords_text.split()
    new_coords = []
    for coord in coords:
        parts = coord.split(',')
        if len(parts) == 2:
            parts.append(str(altitude))
        new_coords.append(','.join(parts))

    # Remplace dans le texte original
    new_coords_text = ' '.join(new_coords)
    return f'\t\t<MultiGeometry><Polygon><altitudeMode>relativeToGround</altitudeMode><outerBoundaryIs><LinearRing><coordinates>{new_coords_text}</coordinates></LinearRing></outerBoundaryIs></Polygon></MultiGeometry>'

