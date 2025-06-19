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
   # "(3)_departement",
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
    #"parcelles-des-personnes-morales (3)_adresse",
    "parcelles-des-personnes-morales (3)_forme_juridique_abregee",
    #"parcelles-des-personnes-morales (3)_denomination",
    #"IDU"
]

mots_cles_a_remplacer={"parcelles-des-personnes-morales (3)_adresse": "Adresse", 
                      "parcelles-des-personnes-morales (3)_forme_juridique_abregee": "Forme Juridique Abrégée",
                      "parcelles-des-personnes-morales (3)_denomination":"Dénomination",
                      "IDU":"Numéro de Parcelle",
                      "parcelles-des-personnes-morales (3)_nom_commune":"Commune", 
                      "parcelles-des-personnes-morales (3)_departement":"Departement"
                    }
                 
def nettoyer(lignes):
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
    return lignes_nettoyees
