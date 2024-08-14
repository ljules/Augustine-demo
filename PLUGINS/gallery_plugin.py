# -------------------------------------------------------------------
#                               GALLERY PLUGIN 
# -------------------------------------------------------------------

# Description :
# -------------
# Ce plugin permet de générer la galerie d'images. 
# 
# Etapes réalisées :
# 1/ Parcours le dossier : content/galerie afin de lister ses dossiers
# 2/ Ajout d'une entrée pour chaque dossier dans le menu de navigation en renseignant la liste de NAV_SITE_AUGUSTINE[3][3]
# 3/ Exécution sur chaque dossier du script thumbnail_generator.py pour générer et mettre à jour les vignettes (thumbnails)
# 4/ Parcours de tous les dossiers et consignation des chemins des thumbnails dans un dictionnaire DICO_GALERY de listes ou chaque 
#    nom de dossier sera une clé, et la valeur associée une liste contenant le nom de l'image
# 5/ Génération des pages (une page par dossier) en utilisant la page de template dédiée.


# IMPORTS :
# ---------
import os
import sys
from datetime import datetime
from pelican import signals
import logging
from jinja2 import Environment, FileSystemLoader
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Configure le logger
logger = logging.getLogger(__name__)

# Ajout du chemin absolu au dossier des plugins
plugin_path = os.path.dirname(__file__)
if plugin_path not in sys.path:
    sys.path.append(plugin_path)

from thumbnail_generator import generate_thumbnails  # Import de la fonction

# CONSTANTES :
# ------------

# Dimension des thumbnail en pixel :
THUMBNAIL_SIZE = 256


# Dictionnaire global pour stocker les galeries
DICO_GALERY = {}


# DEFINITION DES FONCTIONS :
# --------------------------

def initialize_galeries(generator):
    logger.info("Initialisation des galeries.")
    # Chemin vers le dossier des galeries
    content_path = generator.settings.get('PATH', 'content')
    galerie_path = os.path.join(content_path, 'galerie')

    if os.path.exists(galerie_path) and os.path.isdir(galerie_path):
        for item in os.listdir(galerie_path):
            item_path = os.path.join(galerie_path, item)
            if os.path.isdir(item_path):
                DICO_GALERY[item] = []
                logger.info(f"Galerie trouvée : {item}")
    else:
        logger.warning(f"Le chemin {galerie_path} n'existe pas ou n'est pas un répertoire.")


def modify_navigation_bar(generator):
    """Ajoute dans le menu Galerie un sous menu pour chaque sous-dossier."""

    logger.info("Modification de la barre de navigation.")
    nav_bar = generator.settings.get('NAV_SITE_AUGUSTINE', [])
    
    if len(nav_bar) > 3 and isinstance(nav_bar[3], tuple) and len(nav_bar[3]) > 2 and isinstance(nav_bar[3][3], list):
                        
        # Ajout des sous-menus :
        site_url = ""
        #site_url = generator.settings.get('SITEURL', '')        
        for key in DICO_GALERY.keys():
            nav_entry = (key, f"{site_url}/pages/{key}") 
            if nav_entry not in nav_bar[3][3]: 
                nav_bar[3][3].append(nav_entry)
                logger.info(f"Ajouté à la navigation : {nav_entry}")
    else:
        logger.warning("La structure NAV_SITE_AUGUSTINE n'est pas conforme à ce qui est attendu.")


def generate_thumbnails_for_galeries(generator):
    """Génère les thumbnails pour tous les fichiers images avec la fonction generate_thumbnails."""

    logger.info("Génération des vignettes pour les galeries.")
    content_path = generator.settings.get('PATH', 'content')
    galerie_path = os.path.join(content_path, 'galerie')

    for galerie in DICO_GALERY.keys():
        input_folder = os.path.join(galerie_path, galerie)
        output_folder = os.path.join(input_folder, 'thumbnails')
        generate_thumbnails(input_folder, output_folder, THUMBNAIL_SIZE)
        logger.info(f"Vignettes générées pour la galerie : {galerie}")


def get_exif_data(image_path):
    """Extract EXIF data from an image and return a dictionary of relevant fields."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is not None:
            exif = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                exif[tag_name] = value
            
            # Extract GPS information if available
            gps_info = exif.get('GPSInfo')
            if gps_info:
                gps_data = {}
                for key in gps_info.keys():
                    decode = GPSTAGS.get(key, key)
                    gps_data[decode] = gps_info[key]
                exif['GPSInfo'] = gps_data

            return exif
    except Exception as e:
        logger.warning(f"Erreur lors de l'extraction des données EXIF pour {image_path}: {e}")
        return None


def extract_image_metadata(image_path):
    """Extract image metadata including size, date, and location."""
    exif_data = get_exif_data(image_path)
    metadata = {
        'name': os.path.basename(image_path),
        'size': None,
        'date': None,
        'location': None,
    }
    if exif_data:
        # Extract image size
        with Image.open(image_path) as img:
            metadata['size'] = img.size  # (width, height)

        # Extract date
        date_str = exif_data.get('DateTimeOriginal') or exif_data.get('DateTime')        

        if date_str is not None:
            metadata['date'] = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        else:
            metadata['date'] = None


        # Extract GPS coordinates
        gps_info = exif_data.get('GPSInfo')
        if gps_info:
            lat = gps_info.get('GPSLatitude')
            lat_ref = gps_info.get('GPSLatitudeRef')
            lon = gps_info.get('GPSLongitude')
            lon_ref = gps_info.get('GPSLongitudeRef')
            if lat and lat_ref and lon and lon_ref:
                lat = convert_to_degrees(lat)
                if lat_ref != 'N':
                    lat = -lat
                lon = convert_to_degrees(lon)
                if lon_ref != 'E':
                    lon = -lon
                metadata['location'] = (lat, lon)
    
    return metadata


def convert_to_degrees(value):
    """Convert GPS coordinates to degrees."""
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)


def populate_galery_images(generator):
    logger.info("Population des images de galeries.")
    content_path = generator.settings.get('PATH', 'content')
    galerie_path = os.path.join(content_path, 'galerie')

    for galerie, images_list in DICO_GALERY.items():
        galerie_folder = os.path.join(galerie_path, galerie)
        if os.path.exists(galerie_folder) and os.path.isdir(galerie_folder):
            image_metadata_list = []
            for file in os.listdir(galerie_folder):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    image_path = os.path.join(galerie_folder, file)
                    metadata = extract_image_metadata(image_path)
                    image_metadata_list.append(metadata)
            DICO_GALERY[galerie] = image_metadata_list
            logger.info(f"Images pour la galerie '{galerie}': {image_metadata_list}")
        else:
            logger.warning(f"Le dossier de galerie {galerie_folder} est introuvable.")


def generate_gallery_pages(generator):
    logger.info("Génération des pages de galerie.")
    output_path = generator.settings.get('OUTPUT_PATH', 'output')
    theme_path = generator.settings.get('THEME', '')
    template_dir = os.path.join(theme_path, 'templates')

    template_file = 'gallery.html'

    logger.info(f"Chemin du template : {template_dir}")
    logger.info(f"Fichier de template : {template_file}")

    env = Environment(loader=FileSystemLoader(template_dir))

    try:
        template = env.get_template(template_file)
    except Exception as e:
        logger.error(f"Erreur lors du chargement du template {template_file}: {e}")
        return

    pelican_context = generator.context.copy()

    for galerie, images in DICO_GALERY.items():
        galerie_data = {
            'galerie_name': galerie,
            'images': images,
        }

        context = {**pelican_context, **galerie_data}

        try:
            rendered_content = template.render(context)
        except Exception as e:
            logger.error(f"Erreur lors du rendu du template pour {galerie}: {e}")
            continue

        output_dir = os.path.join(output_path, 'pages')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file = os.path.join(output_dir, f'{galerie}.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
        logger.info(f"Page de galerie générée : {output_file}")


# Enregistrement des fonctions :
# ------------------------------

def register():
    signals.static_generator_init.connect(initialize_galeries)
    signals.static_generator_init.connect(modify_navigation_bar)
    signals.static_generator_init.connect(generate_thumbnails_for_galeries)
    signals.static_generator_finalized.connect(populate_galery_images)
    signals.static_generator_finalized.connect(generate_gallery_pages)
