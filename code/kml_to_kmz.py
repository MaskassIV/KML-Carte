import zipfile
import os

def kml_to_kmz_batch(dossier_racine):
    """
    Parcourt un dossier racine et tous ses sous-dossiers pour convertir
    chaque fichier .kml en un fichier .kmz correspondant.
    Les fichiers .kml originaux sont supprimés après une conversion réussie.

    Args:
        dossier_racine (str): Le chemin du dossier où se trouvent tes fichiers KML.
    """
    print(f"Début de la conversion des KML en KMZ dans : {dossier_racine}")

    # Pour garder une trace des fichiers KML supprimés ou non
    fichiers_kml_supprimes = []
    fichiers_kml_non_supprimes = []

    # Parcourir le dossier racine et tous ses sous-dossiers
    for chemin_actuel, sous_dossiers, fichiers in os.walk(dossier_racine):
        for nom_fichier in fichiers:
            # Vérifier si c'est un fichier KML
            if nom_fichier.lower().endswith('.kml'):
                chemin_complet_kml = os.path.join(chemin_actuel, nom_fichier)
                # Construire le nom du fichier KMZ
                nom_fichier_kmz = os.path.splitext(nom_fichier)[0] + '.kmz'
                chemin_complet_kmz = os.path.join(chemin_actuel, nom_fichier_kmz)

                # Si le fichier KMZ existe déjà, on peut choisir de le sauter ou de l'écraser
                if os.path.exists(chemin_complet_kmz):
                    print(f"  Le fichier KMZ '{nom_fichier_kmz}' existe déjà. Écrasement et suppression de l'original...")
                    # Ou tu peux faire un 'continue' ici si tu ne veux pas écraser
                    # continue

                try:
                    # Créer le fichier KMZ (qui est une archive ZIP)
                    with zipfile.ZipFile(chemin_complet_kmz, 'w', zipfile.ZIP_DEFLATED) as kmz_file:
                        # Ajouter le fichier KML à l'archive KMZ
                        kmz_file.write(chemin_complet_kml, 'doc.kml')
                        print(f"  Converti : '{nom_fichier}' en '{nom_fichier_kmz}'")

                        # --- Gestion des ressources associées (Optionnel mais important) ---
                        # Insère ici le code pour ajouter les ressources associées si tu en as.
                        # (Laissée inchangée par rapport à ton code)
                        # Par exemple :
                        # images_folder = os.path.join(chemin_actuel, 'images')
                        # if os.path.isdir(images_folder):
                        #     for root, _, img_files in os.walk(images_folder):
                        #         for img_file in img_files:
                        #             full_img_path = os.path.join(root, img_file)
                        #             arcname = os.path.relpath(full_img_path, chemin_actuel)
                        #             kmz_file.write(full_img_path, arcname)
                        #             print(f"    Ajouté ressource : {arcname}")

                    # --- NOUVEAUTÉ : Supprimer le fichier KML original après conversion réussie ---
                    os.remove(chemin_complet_kml)
                    print(f"  Supprimé l'original : '{nom_fichier}'")
                    fichiers_kml_supprimes.append(chemin_complet_kml)

                except Exception as e:
                    print(f"  Erreur lors de la conversion ou de la suppression de '{nom_fichier}' : {e}")
                    fichiers_kml_non_supprimes.append(chemin_complet_kml)
                    # Si une erreur se produit, on ne supprime pas le KML original pour éviter la perte de données

    print("\nConversion des KML en KMZ terminée.")
    if fichiers_kml_supprimes:
        print(f"Fichiers KML supprimés ({len(fichiers_kml_supprimes)}):")
        for f in fichiers_kml_supprimes:
            print(f"- {f}")
    if fichiers_kml_non_supprimes:
        print(f"\nAttention : Fichiers KML non supprimés en raison d'erreurs ({len(fichiers_kml_non_supprimes)}):")
        for f in fichiers_kml_non_supprimes:
            print(f"- {f}")
    else:
        print("\nTous les fichiers KML originaux ont été supprimés avec succès.")


# Pour nettoyer les fichiers de test après exécution (désactive si tu veux vérifier)
# import shutil
# if os.path.exists("communes_test"):
#    shutil.rmtree("communes_test")