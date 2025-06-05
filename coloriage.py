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

def colorier(cheminFichier, option_nom_fichier):
    option_nom_fichier_bis=option_nom_fichier+"C_"
    supprimer_fichier(cheminFichier, option_nom_fichier_bis)
    for nom_fichier in file_name:
        if os.path.exists(cheminFichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml"):
            with open(cheminFichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        else:
            with open(option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "r", encoding="utf-8") as f:
                lignes = f.readlines()
        lignes = iter(lignes)
        lignes_colorees = []
        for ligne in lignes:
            if "<Folder>" in ligne:
                lignes_colorees.append(creeBlocStyle(nom_fichier))
            lignes_colorees.append(ligne)
            if "<Placemark " in ligne:
                lignes_colorees.append("<styleUrl>#"+nom_fichier+"</styleUrl>")
        with open(cheminFichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", "w", encoding="utf-8") as p:
            p.writelines(lignes_colorees)
        os.rename(cheminFichier+option_nom_fichier+"parcelle_13_"+nom_fichier+".kml", cheminFichier+option_nom_fichier_bis+"parcelle_13_"+nom_fichier+".kml")
        print("Coloration termine pour "+nom_fichier)
    return option_nom_fichier_bis

def inversionCouleur(couleur):
    groupes = [couleur[i:i+2] for i in range(0, len(couleur), 2)]
    groupes_inverses = groupes[::-1]
    resultat = ''.join(groupes_inverses)
    return resultat

def opacite(couleur):
    return "4d"+couleur

def creeBlocStyle(nomCouleur):
    return "\t<Style id=\""+nomCouleur+"\">\n\t\t<LineStyle>\n\t\t\t<color>00ffffff</color>\n\t\t\t<width>0</width>\n\t\t</LineStyle>\n\t\t<PolyStyle>\n\t\t\t<color>"+opacite(couleurs_kml[nomCouleur])+"</color>\n\t\t\t<fill>1</fill>\n\t\t\t<outline>0</outline>\n\t\t</PolyStyle>\n\t</Style>"
