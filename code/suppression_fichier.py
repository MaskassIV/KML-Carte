import os

def supprimer_fichier(chemin_fichier, option_nom_fichier):
    for nom_fichier in os.listdir(chemin_fichier):
        if option_nom_fichier in nom_fichier:
            chemin_fichier = os.path.join(chemin_fichier, nom_fichier)
            if os.path.isfile(chemin_fichier):
                os.remove(chemin_fichier)
                print(f"Supprime : {chemin_fichier}")
                
def nettoyage_final(chemin_fichier, option_nom_fichier):
    for nom_fichier in os.listdir(chemin_fichier):
        if option_nom_fichier in nom_fichier:
                os.remove(chemin_fichier+nom_fichier)
                print("suppression de "+nom_fichier)