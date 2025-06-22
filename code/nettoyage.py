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
    "_code_forme_juridique",
    "parcelles-des-personnes-morales (3)_code_forme_juridique",
    #"parcelles-des-personnes-morales (3)_adresse",
    "parcelles-des-personnes-morales (3)_forme_juridique_abregee",
    #"parcelles-des-personnes-morales (3)_denomination",
    #"IDU"
    "FEUILLE",
    "SECTION",
	"CODE_DEP",
	"NOM_COM",
	"CODE_COM",
	"COM_ABS",
	"CODE_ARR",
	"CONTENANCE",
    "NUMERO"
]
mots_cles_a_remplacer={"parcelles-des-personnes-morales x_adresse": "Adresse",
                       "C:/Users/User/Bureau/69 separe par groupe/parcelles-des-personnes-morales 69_groupe_personne_0.kml":"",
                       "C:/Users/User/Bureau/69 separe par groupe/parcelles-des-personnes-morales 69_groupe_personne_1.kml":"",
                       "C:/Users/User/Bureau/69 separe par groupe/parcelles-des-personnes-morales 69_groupe_personne_2.kml":"",
                       "C:/Users/User/Bureau/69 separe par groupe/parcelles-des-personnes-morales 69_groupe_personne_3.kml":"",
                       "C:/Users/User/Bureau/69 separe par groupe/parcelles-des-personnes-morales 69_groupe_personne_4.kml":"",
                       "C:/Users/User/Bureau/69 separe par groupe/parcelles-des-personnes-morales 69_groupe_personne_5.kml":"",
                       "C:/Users/User/Bureau/69 separe par groupe/parcelles-des-personnes-morales 69_groupe_personne_6.kml":"",
                       "C:/Users/User/Bureau/69 separe par groupe/parcelles-des-personnes-morales 69_groupe_personne_7.kml":"",
                       "C:/Users/User/Bureau/69 separe par groupe/parcelles-des-personnes-morales 69_groupe_personne_8.kml":"",
                       "C:/Users/User/Bureau/69 separe par groupe/parcelles-des-personnes-morales 69_groupe_personne_9.kml":"",
                       "parcelles-des-personnes-morales x_groupe_personne\">0<": "Groupe de personne\">Personnes morales non remarquables<",
                       "parcelles-des-personnes-morales x_groupe_personne\">1<": "Groupe de personne\">Etat<",
                       "parcelles-des-personnes-morales x_groupe_personne\">2<": "Groupe de personne\">Region<",
                       "parcelles-des-personnes-morales x_groupe_personne\">3<": "Groupe de personne\">Departement<",
                       "parcelles-des-personnes-morales x_groupe_personne\">4<": "Groupe de personne\">Commune<",
                       "parcelles-des-personnes-morales x_groupe_personne\">5<": "Groupe de personne\">HLM<",
                       "parcelles-des-personnes-morales x_groupe_personne\">6<": "Groupe de personne\">Personnes morales representant des societes d'economie mixte<",
                       "parcelles-des-personnes-morales x_groupe_personne\">7<": "Groupe de personne\">Coproprietaires<",
                       "parcelles-des-personnes-morales x_groupe_personne\">8<": "Groupe de personne\">Associes<",
                       "parcelles-des-personnes-morales x_groupe_personne\">9<": "Groupe de personne\">Etablissements publics ou organismes associes<",
                       
                        "parcelles-des-personnes-morales x_groupe_personne\" type=\"string\"":"Groupe de personne\" type=\"string\"",
                        "<SimpleField type=\"string\" name=\"parcelles-des-personnes-morales x_groupe_personne\"></SimpleField>":"<SimpleField type=\"string\" name=\"Groupe de personne\"></SimpleField>",
                      "parcelles-des-personnes-morales x_forme_juridique_abregee": "Forme Juridique Abregee",
                      "parcelles-des-personnes-morales x_denomination":"Denomination",
                      "IDU":"Numero de Parcelle",
                      "parcelles-des-personnes-morales x_nom_commune":"Commune",
                      "<Polygon>":"<Polygon><altitudeMode>relativeToGround</altitudeMode>",
                    "NOM_COM":"Commune", 
                      "parcelles-des-personnes-morales x_departement":"Departement",
                        "name=\"parcelle_x_": "name=\"",  # Supprime le nom du schéma
    "id=\"parcelle_x_": "id=\"",      # Supprime l'id du schéma
    "schemaUrl=\"#parcelle_x_": "schemaUrl=\"#",
    "<coordinates>\n":"<coordinates>"
                    }



def nettoyer(lignes, departement):
    i=0
    global depart_actuel
    lignes = iter(lignes)

    dico = adapter_dico(departement)
    lignes_nettoyees = []
    for ligne in lignes:
        if "<Style" in ligne:
            ligne = next(lignes, None)
            while "</Style>" not in ligne:
                ligne = next(lignes, None)
            continue
        if not any(mot in ligne for mot in mots_cles_a_supprimer):
            for key in dico :
                if key in ligne:
                    ligne=ligne.replace(key, dico[key])
                    break
            lignes_nettoyees.append(ligne)
    return lignes_nettoyees


def adapter_dico(departement):
    nouveau_dico = {}
    for key, value in mots_cles_a_remplacer.items():
        if "x" in key:
            key_modifiee = key.replace("x", str(departement))
            nouveau_dico[key_modifiee] = value
        else:
            nouveau_dico[key] = value
    return nouveau_dico
