# ------------------------------------------------------------------#
#                   GENERATEUR DE VIGNETTES                         #
# ------------------------------------------------------------------#

# IMPORTS :
# ---------

# Bibliothèques natives :
import os  # Gestion des fichiers & dossiers

# Bibliothèques tierces :
from PIL import Image, ExifTags  # PIL bibliothèque de gestion des images


# DEFINITION DES FONCTIONS :
# --------------------------

# Fonction de nettoyage des thumbnails orphelins :
def clean_orphan_thumbnails(input_folder, output_folder):
    """
    Supprime les miniatures orphelines, c'est-à-dire celles dont l'image source n'existe plus.

    Args:
        input_folder (str): Le chemin du dossier contenant les images sources.
        output_folder (str): Le chemin du dossier où les miniatures sont enregistrées.
    """
    for filename in os.listdir(output_folder):
        if filename.startswith('thumbnail_'):
            original_filename = filename[len('thumbnail_'):]
            original_path = os.path.join(input_folder, original_filename)
            if not os.path.exists(original_path):
                os.remove(os.path.join(output_folder, filename))
                print(f"Miniature orpheline supprimée : {filename}")


# Fonction de génération et mise à jour des thumbnails :
def generate_thumbnails(input_folder, output_folder, thumb_size=256):
    """
    Génère des miniatures carrées pour les images dans un dossier donné,
    en ajoutant des bandes pour maintenir le rapport d'aspect des images d'origine.

    Args:
        input_folder (str): Le chemin du dossier contenant les images sources.
        output_folder (str): Le chemin du dossier où les miniatures seront enregistrées.
                             Ce dossier sera créé s'il n'existe pas déjà.
        thumb_size (int): La taille (en pixels) du côté des miniatures carrées. 
                          La valeur par défaut est 512 pixels.

    Description:
        Cette fonction parcourt tous les fichiers dans le dossier `input_folder` et génère
        des miniatures pour les images. Les images sont d'abord redimensionnées pour s'adapter
        à une zone carrée de côté `thumb_size`, en maintenant le ratio d'aspect d'origine.
        Si les dimensions de l'image ne correspondent pas au carré, des bandes transparentes sont
        ajoutées pour remplir les espaces vides, produisant une image finale de taille `thumb_size x thumb_size`.

    Détails techniques:
        - La fonction vérifie et corrige l'orientation des images en fonction des données EXIF
          lorsque cela est possible.
        - Seules les images avec les extensions '.png', '.jpg', '.jpeg', '.gif', et '.bmp' 
          sont traitées.
        - Les images miniatures sont enregistrées dans le dossier `output_folder` avec le 
          même nom que l'image d'origine, précédé par "thumbnail_".

    Exemples:
        Pour générer des miniatures pour des images situées dans le dossier 'images',
        et les enregistrer dans le sous-dossier 'thumbnails':

        ```python
        generate_thumbnails('images', 'images/thumbnails')
        ```

    Notes:
        - Assurez-vous que le module PIL (Pillow) est installé: `pip install pillow`
    """
    # Crée le dossier de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)

    # Nettoyage des miniatures orphelines
    clean_orphan_thumbnails(input_folder, output_folder)

    # Dictionnaire pour l'orientation EXIF :
    orientation_tag = None
    for tag, value in ExifTags.TAGS.items():
        if value == 'Orientation':
            orientation_tag = tag
            break

    # Parcours des fichiers dans le dossier d'entrée
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # Filtres pour les fichiers image
            image_path = os.path.join(input_folder, filename)
            thumbnail_filename = f"thumbnail_{filename}"
            thumbnail_path = os.path.join(output_folder, thumbnail_filename)
            
            # Vérifie si le fichier miniature existe déjà et est à jour
            if os.path.exists(thumbnail_path):
                if os.path.getmtime(image_path) <= os.path.getmtime(thumbnail_path):
                    # La miniature existe et est à jour
                    continue

            with Image.open(image_path) as img:
                # Vérifier et ajuster l'orientation avant la conversion en RGBA
                try:
                    exif = img._getexif()
                    if exif is not None and orientation_tag in exif:
                        orientation = exif[orientation_tag]
                        if orientation == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:
                            img = img.rotate(90, expand=True)
                except (AttributeError, KeyError, IndexError):
                    # S'il y a une erreur en récupérant les EXIF, passer à la suite
                    pass
                
                # Convertir l'image en mode RGBA pour la transparence
                img = img.convert('RGBA')

                # Calcul des dimensions de l'image et de la miniature
                width, height = img.size
                aspect_ratio = width / height

                # Créer une image de fond transparente carrée
                square_background = Image.new('RGBA', (thumb_size, thumb_size), (0, 0, 0, 0))

                # Calcul de la nouvelle taille de l'image pour respecter l'aspect ratio
                if aspect_ratio > 1:  # Image plus large que haute
                    new_width = thumb_size
                    new_height = int(thumb_size / aspect_ratio)
                else:  # Image plus haute que large ou carrée
                    new_height = thumb_size
                    new_width = int(thumb_size * aspect_ratio)

                # Redimensionnement de l'image
                img_resized = img.resize((new_width, new_height))

                # Calcul des positions pour centrer l'image redimensionnée sur le fond carré
                x_offset = (thumb_size - new_width) // 2
                y_offset = (thumb_size - new_height) // 2

                # Coller l'image redimensionnée sur le fond transparent
                square_background.paste(img_resized, (x_offset, y_offset), img_resized)

                # Enregistrement de la miniature
                square_background.save(thumbnail_path, 'PNG')

    print("Miniatures générées avec succès.")


# Bloc de code pour l'exécution directe :
# ---------------------------------------
if __name__ == "__main__":
    INPUT_FOLDER = 'test'  # Remplacez par le chemin de votre dossier
    OUTPUT_FOLDER = os.path.join(INPUT_FOLDER, 'thumbnails')
    THUMB_SIZE = 256       # Taille de la miniature carrée
    generate_thumbnails(INPUT_FOLDER, OUTPUT_FOLDER, THUMB_SIZE)
