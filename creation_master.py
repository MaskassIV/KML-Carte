import os
from fichiers import file_name

def creer_master(cheminFichier, villes_box):
    intro = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n\t<Document>\n\t\t<name>Master KML - Chargement selon zoom</name>"
    with open(cheminFichier+"/"+"Master.kml", "w", encoding="utf-8") as p:
        p.writelines(intro)
        for ville in villes_box:
            liste_fichier = {}
            for nom_fichiers in file_name:
                if os.path.exists("./modifie"+"/"+nom_fichiers+"/"+nom_fichiers+"_"+ville+".kml"):
                    liste_fichier[nom_fichiers]=nom_fichiers+"/"+nom_fichiers+"_"+ville+".kml"
            p.writelines("\t<Folder>\n\t\t<name>"+ville+"</name>\n")
            for fichier in liste_fichier:
                lien ="https://raw.githubusercontent.com/MaskassIV/KML-Carte/refs/heads/main/"+liste_fichier[fichier].replace(" ", "%20")
            #lien = liste_fichier[fichier]
            
                p.writelines("\t\t<NetworkLink>\n\t\t\t<name>"+fichier+"</name>\n\t\t\t<Region>\n\t\t\t\t<LatLonAltBox>\n\t\t\t\t\t<north>"+str(villes_box[ville][0])+"</north>\n\t\t\t\t\t<south>"+str(villes_box[ville][1])+"</south>\n\t\t\t\t\t<east>"+str(villes_box[ville][2])+"</east>\n\t\t\t\t\t<west>"+str(villes_box[ville][3])+"</west>\n\t\t\t\t</LatLonAltBox>\n\t\t\t\t<Lod>\n\t\t\t\t\t<minLodPixels>128</minLodPixels>\n\t\t\t\t\t<maxLodPixels>-1</maxLodPixels>\n\t\t\t\t</Lod>\n\t\t\t</Region>\n\t\t\t<Link>\n\t\t\t\t<href>"+lien+"</href>\n\t\t\t\t<viewRefreshMode>Never</viewRefreshMode>\n\t\t\t</Link>\n\t\t</NetworkLink>\n")
            p.write("\t\t</Folder>")
        p.writelines("\n\t</Document>\n</kml>")