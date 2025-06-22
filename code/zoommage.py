import os
import re
from fichiers import file_name

def zoom(lignes):
    """
    Ajoute des balises Region avec LatLonAltBox aux placemarks KML
    """
    lignes_zoomees = []
    index = -1
    puissance_zoom = 100
    puissance_inverse = -1
    
    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        
        # Détecter la fin des ExtendedData pour savoir où insérer la Region
        if "</ExtendedData>" in ligne:
            index = len(lignes_zoomees)
        
        # Détecter le début des coordonnées
        if "<coordinates>" in ligne:
            coords_completes = ""
            ligne_coords_debut = i
            
            # Cas 1: <coordinates> seul sur une ligne
            if re.sub(r'\s+', '', ligne) == "<coordinates>":
                lignes_zoomees.append(ligne)
                i += 1
                # Lire les lignes suivantes jusqu'à </coordinates>
                while i < len(lignes) and "</coordinates>" not in lignes[i]:
                    coords_completes += lignes[i].strip() + " "
                    lignes_zoomees.append(lignes[i])
                    i += 1
                
                # Traiter la ligne de fermeture </coordinates>
                if i < len(lignes) and "</coordinates>" in lignes[i]:
                    coords_sur_ligne_fermeture = lignes[i].replace("</coordinates>", "").strip()
                    if coords_sur_ligne_fermeture:
                        coords_completes += coords_sur_ligne_fermeture
                    lignes_zoomees.append(lignes[i])
            
            # Cas 2: coordonnées sur la même ligne que <coordinates>
            else:
                coords_completes = ligne.replace("<coordinates>", "").replace("</coordinates>", "").strip()
                
                # Si pas de </coordinates> sur cette ligne, continuer à lire
                if "</coordinates>" not in ligne:
                    lignes_zoomees.append(ligne)
                    i += 1
                    while i < len(lignes) and "</coordinates>" not in lignes[i]:
                        coords_completes += " " + lignes[i].strip()
                        lignes_zoomees.append(lignes[i])
                        i += 1
                    
                    # Traiter la ligne de fermeture
                    if i < len(lignes) and "</coordinates>" in lignes[i]:
                        coords_sur_ligne_fermeture = lignes[i].replace("</coordinates>", "").strip()
                        if coords_sur_ligne_fermeture:
                            coords_completes += " " + coords_sur_ligne_fermeture
                        lignes_zoomees.append(lignes[i])
                else:
                    # Tout est sur une seule ligne
                    lignes_zoomees.append(ligne)
            
            # Calculer et insérer la Region si on a trouvé des coordonnées
            if coords_completes.strip() and index != -1:
                try:
                    north, south, east, west = calculer_box(coords_completes)
                    region_xml = ("\t<Region>\n"
                                 "\t\t<LatLonAltBox>\n"
                                 f"\t\t\t<north> {north} </north>\n"
                                 f"\t\t\t<south> {south} </south>\n"
                                 f"\t\t\t<east> {east} </east>\n"
                                 f"\t\t\t<west> {west} </west>\n"
                                 "\t\t</LatLonAltBox>\n"
                                 "\t\t<Lod>\n"
                                 f"\t\t\t<minLodPixels>{puissance_zoom}</minLodPixels>\n"
                                 f"\t\t\t<maxLodPixels>{puissance_inverse}</maxLodPixels>\n"
                                 "\t\t</Lod>\n"
                                 "\t</Region>\n")
                    
                    lignes_zoomees.insert(index + 1, region_xml)
                    index = -1  # Reset pour le prochain placemark
                except Exception as e:
                    print(f"Erreur lors du calcul de la bounding box: {e}")
                    print(f"Coordonnées: {coords_completes[:200]}...")
        else:
            # Ligne normale, on l'ajoute telle quelle
            lignes_zoomees.append(ligne)
        
        i += 1
    
    return lignes_zoomees

def calculer_box(coords_string):
    """
    Calcule la bounding box à partir d'une chaîne de coordonnées
    """
    # Pattern pour longitude,latitude avec altitude optionnelle
    pattern = r'(-?\d+\.?\d*),(-?\d+\.?\d*)(?:,(-?\d+\.?\d*))?'
    longitudes = []
    latitudes = []

    matches = re.findall(pattern, coords_string)
    
    if matches:
        for match in matches:
            lon_str, lat_str = match[0], match[1]
            try:
                longitudes.append(float(lon_str))
                latitudes.append(float(lat_str))
            except ValueError:
                continue
        
        if longitudes and latitudes:
            return max(latitudes), min(latitudes), max(longitudes), min(longitudes)
        else:
            raise ValueError("Aucune coordonnée valide trouvée")
    else:
        raise ValueError("Format de coordonnées non reconnu")

# Exemple d'utilisation (à adapter selon votre fichier fichiers.py)
def traiter_fichier_kml(nom_fichier):
    """
    Traite un fichier KML pour y ajouter les régions de zoom
    """
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
        
        lignes_avec_zoom = zoom(lignes)
        
        # Écrire le fichier de sortie
        nom_sortie = nom_fichier.replace('.kml', '_avec_zoom.kml')
        with open(nom_sortie, 'w', encoding='utf-8') as f:
            f.writelines(lignes_avec_zoom)
        
        print(f"Fichier traité: {nom_sortie}")
        
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")

# Test si le script est exécuté directement
if __name__ == "__main__":
    # Remplacez par le nom de votre fichier
    traiter_fichier_kml("votre_fichier.kml")