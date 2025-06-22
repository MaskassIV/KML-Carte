import os
from fichiers import file_name
from suppression_fichier import supprimer_fichier

couleurs_kml = {
    "ASSOCIE": "02206f",
    "coproprietaire": "7c1404",
    "DEPT": "63f16c",
    "PMRSEM": "00faff",
    "region": "318006",
    "COM": "e6c645",
    "ETAT": "119ff7",
    "HLM": "e451f5",
    "personne_morale": "0000ff",
    "PUBLICorASSOCIE": "db2105"
}

def colorier(lignes, nom_fichier):
    lignes = iter(lignes)
    lignes_colorees = []
    style_ajoute = False
    
    for ligne in lignes:
        lignes_colorees.append(ligne)
        
        # Insérer le style après le Schema et avant le premier Placemark
        if not style_ajoute and ("</Schema>" in ligne or ("<Placemark " in ligne)):
            if "</Schema>" in ligne:
                # Insérer après la fermeture du Schema
                lignes_colorees.append(creer_bloc_style(nom_fichier))
                style_ajoute = True
            elif "<Placemark " in ligne and not style_ajoute:
                # Si on arrive à un Placemark sans avoir vu de Schema, insérer avant
                lignes_colorees.insert(-1, creer_bloc_style(nom_fichier))
                style_ajoute = True
        
        # Ajouter la référence de style après chaque ouverture de Placemark
        if "<Placemark " in ligne:
            lignes_colorees.append("\t\t<styleUrl>#"+nom_fichier+"</styleUrl>")
    
    return lignes_colorees

def inversion_couleur(couleur):
    groupes = [couleur[i:i+2] for i in range(0, len(couleur), 2)]
    groupes_inverses = groupes[::-1]
    resultat = ''.join(groupes_inverses)
    return resultat

def opacite(couleur, pourcentage):
    return str(format(round(255*(pourcentage/100)), '02X'))+couleur

def creer_bloc_style(nomCouleur):
    epaisseur_bordure = 1.5
    return "\t\t<Style id=\""+nomCouleur+"\">\n\t\t\t<LineStyle>\n\t\t\t\t<color>"+opacite(couleurs_kml[nomCouleur], 75)+"</color>\n\t\t\t\t<width>"+str(epaisseur_bordure)+"</width>\n\t\t\t</LineStyle>\n\t\t\t<PolyStyle>\n\t\t\t\t<color>"+opacite(couleurs_kml[nomCouleur], 30)+"</color>\n\t\t\t\t<fill>1</fill>\n\t\t\t\t<outline>1</outline>\n\t\t\t</PolyStyle>\n\t\t</Style>\n"