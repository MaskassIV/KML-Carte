import os
import re
from fichiers import file_name

def simplifier(lignes):
    lignes = iter(lignes)
    lignes_simplifiees = []
    for ligne in lignes:
        if "<coordinates>" in ligne:
            lignes_simplifiees.append(arrondir_coordonnees(ligne))
        else:
            lignes_simplifiees.append(ligne)
    return lignes_simplifiees
        
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
    
