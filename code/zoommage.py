import os
import re
from fichiers import file_name

def zoom(lignes):
    lignes = iter(lignes)
    lignes_zoomees = []
    index = -1
    puissance_zoom = 100
    puissance_inverse=-1
    for ligne in lignes:
        if "</ExtendedData>" in ligne:
            index = len(lignes_zoomees)
        if "<coordinates>" in ligne:
            if re.sub(r'\s+', '', ligne) == "<coordinates>":
                lignes_zoomees.append(ligne)
                ligne = next(lignes, None)
            north, south, east, west = calculer_box(ligne)
            lignes_zoomees.insert(index+1, "\t<Region>\n\t\t<LatLonAltBox>\n\t\t\t<north> "+str(north)+" </north>\n\t\t\t<south> "+str(south)+" </south>\n\t\t\t<east> "+str(east)+" </east>\n\t\t\t<west> "+str(west)+" </west>\n\t\t</LatLonAltBox>\n\t\t<Lod>\n\t\t\t<minLodPixels>"+str(puissance_zoom)+"</minLodPixels>\n\t\t\t<maxLodPixels>"+str(puissance_inverse)+"</maxLodPixels>\n\t\t</Lod>\n\t</Region>\n" )
            index=-1
        lignes_zoomees.append(ligne)
    return lignes_zoomees

  
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
        print("Pas de position a recuperer")
        exit()