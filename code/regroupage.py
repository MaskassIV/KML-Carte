import os
from fichiers import file_name
from suppression_fichier import supprimer_fichier

def regrouper(chemin_fichier, option_nom_fichier):
    option_nom_fichier_bis=option_nom_fichier+"R_"
    supprimer_fichier(chemin_fichier, option_nom_fichier_bis)
    for nom_fichier in file_name:
        if  os.path.exists(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml"):
            with open(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        else:
            with open(option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        lignes = iter(lignes)
        lignes_regroupees = []
        for ligne in lignes:
            if "<Placemark" not in ligne:
                lignes_regroupees.append(ligne)
            else :
                break
        lignes_regroupees.append("<Placemark id=\"parcelle_13_com_grouped\">\n\t<styleUrl>#"+nom_fichier+"</styleUrl>\n\t<ExtendedData>\n\t\t<SchemaData schemaUrl=\"#parcelle_13_com\">\n\t\t\t<SimpleData name=\"Groupe personne\">"+nom_fichier +"</SimpleData>\n\t\t</SchemaData>\n\t</ExtendedData>\n\t<MultiGeometry>\n")
        for ligne in lignes:
            if "<MultiGeometry" in ligne :
                lignes_regroupees.append(ligne.replace("<MultiGeometry>", "").replace("</MultiGeometry>", ""))
        lignes_regroupees.append("\t</MultiGeometry>\n</Placemark>\n</Folder>\n</Document></kml>")
        with open(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "w", encoding="utf-8") as p:
            p.writelines(lignes_regroupees)
        os.rename(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", chemin_fichier+option_nom_fichier_bis+"parcelle_13_"+nom_fichier+".kml")
        print("Regroupage termine pour "+nom_fichier)
    return option_nom_fichier_bis