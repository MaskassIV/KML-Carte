import os
from fichiers import file_name
from suppression_fichier import supprimer_fichier

mots_cles_a_supprimer = [
    "name=\"fid",
    "(3)_fid",
    "contenance_parcelle",
    "code_commune",
   # "nom_commune",
    "code_voie_majic",
    "code_voie_rivoli",
    "SUF",
    "contenance_suf",
    "nature_culture",
    "code_droit",
    "numero_majic",
    "(3)_departement",
    "numero_siren",
    "parcelle_coords.coord",
    "infos_commune.code_commune",
    "infos_commune.nom_commune",
    "infos_commune.nom_departement",
    "infos_commune.code_epci",
    "infos_commune.nom_epci",
    "infos_commune.code_region",
    "infos_commune.nom_region",
    "(3)_groupe_personne",
    "parcelles-des-personnes-morales (3)_code_forme_juridique",
    "parcelles-des-personnes-morales (3)_adresse",
    "parcelles-des-personnes-morales (3)_forme_juridique_abregee",
    "parcelles-des-personnes-morales (3)_denomination",
    "IDU"
]

mots_cles_a_remplacer={"parcelles-des-personnes-morales (3)_adresse": "Adresse", 
                      "parcelles-des-personnes-morales (3)_forme_juridique_abregee": "Forme Juridique Abrégée",
                      "parcelles-des-personnes-morales (3)_denomination":"Dénomination",
                      "IDU":"Numéro de Parcelle",
                      "parcelles-des-personnes-morales (3)_nom_commune":"Commune"
                    }
                 
def nettoyer(chemin_fichier, option_nom_fichier):
    option_nom_fichier_bis=option_nom_fichier+"N_"
    supprimer_fichier(chemin_fichier, option_nom_fichier_bis)
    for nom_fichier in file_name:
        if  os.path.exists(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml"):
            with open(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        else:
            with open(option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        lignes = iter(lignes)
        lignes_nettoyees = []
        for ligne in lignes:
            if "<Style" in ligne:
                ligne = next(lignes, None)
                while "</Style>" not in ligne:
                    ligne = next(lignes, None)
                continue
            if not any(mot in ligne for mot in mots_cles_a_supprimer):
                for key in mots_cles_a_remplacer :
                    if key in ligne:
                        ligne=ligne.replace(key, mots_cles_a_remplacer[key])
                        break
                lignes_nettoyees.append(ligne)

        with open(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "w", encoding="utf-8") as f:
            f.writelines(lignes_nettoyees)
        os.rename(chemin_fichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", chemin_fichier+option_nom_fichier_bis+"parcelle_13_"+nom_fichier+".kml")
        print("Nettoyage termine pour "+nom_fichier)
    return option_nom_fichier_bis
