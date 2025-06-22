import os
import re
from fichiers import file_name

def repartir_par_ville(departement):
    i=0
    villes_box={}
    for nom_fichier in file_name:
        if os.path.exists("./modifie/Brute/parcelle_"+str(departement)+"_"+nom_fichier+"_test.kml"):
            with open("./modifie/Brute/parcelle_"+str(departement)+"_"+nom_fichier+"_test.kml", "r", encoding="cp1252") as f:
                lignes = f.readlines()
            lignes = iter(lignes)
            intro = []
            villes = {}
            nom_ville=""
            schema_id = ""
            
            # Analyser la structure pour déterminer le type de fermeture nécessaire
            content_str = ''.join(lignes)
            lignes = iter(content_str.splitlines(True))  # Recréer l'itérateur
            
            # Compter les balises Document pour déterminer la fermeture appropriée
            document_count = content_str.count('<Document')
            if document_count > 1:
                outro = ["</Document></Document></kml>"]
            else:
                outro = ["</Folder></Document></kml>"]
            
            # Collecter l'intro jusqu'au premier Placemark
            for ligne in lignes :
                if "<Placemark" in ligne:
                    break
                else:
                    intro.append(ligne)
                    # Capturer l'ID du schema original
                    if 'Schema name=' in ligne and 'id=' in ligne:
                        match = re.search(r'id="([^"]+)"', ligne)
                        if match:
                            schema_id = match.group(1)
            
            # Traiter les Placemark
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
                            if "<north>" in ligne_bloc or "<south>" in ligne_bloc or "<east>" in ligne_bloc or "<west>" in ligne_bloc :
                                if nom_ville:
                                    calculer_box_ville(ligne_bloc, villes_box, nom_ville)
                            bloc.append(ligne_bloc)
                        else:
                            bloc.append(ligne_bloc)
                            break
                    if nom_ville:
                        if nom_ville not in villes:
                            i+=1
                            villes[nom_ville] = []
                        villes[nom_ville].extend(bloc)
            
            # Créer les fichiers par ville
            os.makedirs("./modifie/"+nom_fichier, exist_ok=True)
            for ville in villes:
                with open("./modifie/"+nom_fichier+"/"+nom_fichier+"_"+ville+".kml", "w", encoding="cp1252") as p:
                    intro_modifiee = modifier_intro(intro, ville, nom_fichier, schema_id)
                    p.writelines(intro_modifiee)
                    for bloc in villes.get(ville):
                        # Mettre à jour les références schemaUrl dans les blocs
                        bloc_modifie = []
                        for ligne_bloc in bloc:
                            if 'schemaUrl=' in ligne_bloc and schema_id:
                                ligne_bloc = re.sub(r'schemaUrl="#[^"]*"', f'schemaUrl="#{ville}_{nom_fichier}.schema"', ligne_bloc)
                            bloc_modifie.append(ligne_bloc)
                        p.writelines(bloc_modifie)
                    p.writelines(outro)
            print("Fichier par ville termine pour "+ nom_fichier)
    print("i vaut "+str(len(villes)))
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

def modifier_intro(intro, ville, nom_fichier, schema_id):
    lignes_modifiees = []
    nouveau_schema_id = f"{ville}_{nom_fichier}"
    
    for ligne in intro:
        if ligne.strip().startswith('<Schema name='):
            # Modifier le nom et l'id du Schema
            ligne = re.sub(r'name="[^"]*"', f'name="{nouveau_schema_id}"', ligne)
            ligne = re.sub(r'id="[^"]*"', f'id="{nouveau_schema_id}.schema"', ligne)
        elif '<name>' in ligne and any(tag in ligne for tag in ['parcelles-des-personnes-morales', nom_fichier]):
            # Mettre à jour le nom du document si nécessaire
            ligne = re.sub(r'<name>.*?</name>', f'<name>{nouveau_schema_id}</name>', ligne)
        elif 'id=' in ligne and schema_id and schema_id in ligne:
            # Mettre à jour les autres références à l'ancien schema_id
            ligne = ligne.replace(schema_id, nouveau_schema_id)
        
        lignes_modifiees.append(ligne)
    return lignes_modifiees