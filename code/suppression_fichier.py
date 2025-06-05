import os

def supprimer_fichier(cheminFichier, option_nom_fichier):
    for nom_fichier in os.listdir(cheminFichier):
        if option_nom_fichier in nom_fichier:
            chemin_fichier = os.path.join(cheminFichier, nom_fichier)
            if os.path.isfile(chemin_fichier):
                os.remove(chemin_fichier)
                print(f"Supprimé : {chemin_fichier}")
                        