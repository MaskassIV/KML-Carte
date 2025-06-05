import re

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
    
