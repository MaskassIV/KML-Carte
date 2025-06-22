import os
import re
from fichiers import file_name
from ville import villes

def mise_en_hauteur(chemin_fichier):
    for city in villes:
        print("ville : " + city)
        altitude = 15
        affichage = False
        
        for fichier in file_name:
            fichier_path = chemin_fichier + "/" + fichier + "/" + fichier + "_" + city + ".kml"
            if os.path.exists(fichier_path):
                affichage = True
                with open(fichier_path, "r", encoding="cp1252") as f:
                    lignes = f.readlines()
                
                if city == "MARSEILLE 2EME":
                    altitude = 30
                
                lignes_elevees = traiter_coordonnees_multilignes(lignes, altitude, city)
                with open(fichier_path, "w", encoding="cp1252") as p:
                    p.writelines(lignes_elevees)
        
        if affichage:
            print("Elevage en hauteur termine pour " + city)



def traiter_coordonnees_multilignes(lignes, altitude, city):
    """
    Traite les coordonnées qui peuvent être sur plusieurs lignes
    """
    lignes_elevees = []
    i = 0
    
    while i < len(lignes):
        ligne = lignes[i]
        
        if "<coordinates>" in ligne:
            # Détecter si c'est sur une ligne ou plusieurs
            if "</coordinates>" in ligne:
                # Cas simple : tout sur une ligne
                ligne_modifiee = add_altitude_to_coordinates_simple(ligne, altitude, city)
                lignes_elevees.append(ligne_modifiee)
            else:
                # Cas complexe : coordonnées sur plusieurs lignes
                lignes_coords = [ligne]  # Ligne avec <coordinates>
                i += 1
                
                # Collecter toutes les lignes jusqu'à </coordinates>
                while i < len(lignes) and "</coordinates>" not in lignes[i]:
                    lignes_coords.append(lignes[i])
                    i += 1
                
                # Ajouter la ligne de fermeture
                if i < len(lignes):
                    lignes_coords.append(lignes[i])
                
                # Traiter le bloc complet
                bloc_modifie = add_altitude_to_coordinates_bloc(lignes_coords, altitude, city)
                lignes_elevees.extend(bloc_modifie)
        else:
            lignes_elevees.append(ligne)
        
        i += 1
    
    return lignes_elevees

def add_altitude_to_coordinates_bloc(lignes_coords, altitude, city):
    """
    Traite un bloc de coordonnées sur plusieurs lignes
    """
    # Reconstituer le texte complet des coordonnées
    texte_complet = ''.join(lignes_coords)
    
    # Utiliser DOTALL pour que . capture aussi les retours à la ligne
    match = re.search(r'<coordinates>(.*?)</coordinates>', texte_complet, re.DOTALL)
    if not match:
        return lignes_coords
    
    coords_text = match.group(1).strip()
    coords_modifiees = modifier_altitude_coordonnees(coords_text, altitude, city)
    
    # Remplacer dans le texte complet
    nouveau_texte = texte_complet.replace(match.group(1), coords_modifiees)
    
    # Retourner les lignes modifiées
    return nouveau_texte.splitlines(keepends=True)

def add_altitude_to_coordinates_simple(ligne, altitude, city):
    """
    Traite les coordonnées sur une seule ligne
    """
    match = re.search(r'<coordinates>(.*?)</coordinates>', ligne)
    if not match:
        return ligne
    
    coords_text = match.group(1).strip()
    coords_modifiees = modifier_altitude_coordonnees(coords_text, altitude, city)
    
    return ligne.replace(match.group(1), coords_modifiees)

def modifier_altitude_coordonnees(coords_text, altitude, city):
    """
    Modifie l'altitude dans une chaîne de coordonnées
    """
    coords = coords_text.split()
    new_coords = []
    
    for coord in coords:
        if coord.strip():  # Ignorer les chaînes vides
            parts = coord.split(',')
             
            if len(parts) == 2:
                # Ajouter l'altitude
                parts.append(str(altitude))
            elif len(parts) == 3:
                # Corriger l'index : l'altitude est à l'index 2, pas 3
                parts[2] = str(altitude)

            new_coords.append(','.join(parts))
    
    return ' '.join(new_coords)

def add_altitude_to_coordinates(ligne, altitude, city):
    """
    Version originale corrigée pour compatibilité
    """
    return add_altitude_to_coordinates_simple(ligne, altitude, city)