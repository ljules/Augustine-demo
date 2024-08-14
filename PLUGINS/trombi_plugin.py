# -------------------------------------------------------------------
#                               TROMBI PLUGIN 
# -------------------------------------------------------------------

# Description :
# -------------
# Plugin permettant de parcourir un dossier comportant des fichiers
# Markdown contenant les informations d'utilisateurs pour établir
# leur trombi. Les trombi seront des objets placés dans une collection
# mise à disposition dans le contexte de Pelican.

# IMPORTS :
# ---------

import os
import re
import logging
import datetime
from pelican import signals

# CONFIGURATION :
# ---------------

# Dossier qui contient les fichiers .md :
DOSSIER_TROMBI = 'trombi'

# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# DEFINITION DU MODELE OBJET (CLASSE) :
# -------------------------------------

class Trombi:
    def __init__(self, nom, prenom, photo, fonction, entree, sortie, role, bio, instagram, facebook, linked_in):
        self.nom = nom
        self.prenom = prenom
        self.photo = photo
        self.fonction = fonction
        self.entree = entree
        self.sortie = sortie
        self.role = role
        self.bio = bio
        self.instagram = instagram
        self.facebook = facebook
        self.linked_in = linked_in


# DEFINITION DE LA FONCTION DE PARSING :
# --------------------------------------

def parse_trombi_file(file_path):
    """
    Parse le contenu du fichier ayant file_path comme chemin.
    Retourne un objet Trombi valorisé avec les données du fichier parsé.
    """

    logger.debug(f'Parsing file: {file_path}')

    # Ouverture du fichier :
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        data = {}
        # Parcours des lignes du fichier :
        for line in content.split('\n'):
            # Application d'une expression régulière pour extraire chaque métadonnée :
            match = re.match(r'^(\w+):\s*(.*)', line)
            # Enregistrement dans le dictionnaire data des données :
            if match:
                key, value = match.groups()
                data[key.lower()] = value

        # Instance et valorisation de l'objet trombi retourné
        trombi = Trombi(
            nom = data.get('nom', ''),
            prenom = data.get('prenom', ''),
            photo = data.get('photo', ''),
            fonction = data.get('fonction', ''),
            entree = data.get('entree', ''),
            sortie = data.get('sortie', ''),
            role = data.get('role', ''),
            bio = data.get('bio', ''),            
            instagram = data.get('instagram', ''),
            facebook = data.get('facebook', ''),
            linked_in = data.get('linked_in', '')
        )

        logger.debug(f'Parsed trombi: {trombi.__dict__}')

        return trombi

# GENERATION DE LA LISTE D'OBJETS TROMBI :
# ----------------------------------------

def generate_trombi(pelican):
    logger.info('Generating trombi collection...')

    content_path = pelican.settings.get('PATH', 'content')      # Récupération du chemin du dossier de contenu
    trombi_path = os.path.join(content_path, DOSSIER_TROMBI)    # Chemin du dossier trombi
    trombi_collection = []                                      # Initialisation de la liste de d'objets Trombi
    dico_team = {}                                              # Dictionnaire ayant pour clé l'année de session et en valeur une liste des Trombis

    # Parcours des fichiers du dossier trombi :
    if os.path.isdir(trombi_path):
        for filename in os.listdir(trombi_path):
            if filename.endswith('.md'):                            # Sélection des fichiers .md
                file_path = os.path.join(trombi_path, filename)     # Chemin du fichier courant
                trombi = parse_trombi_file(file_path)               # Instance d'un objet trombi sur le fichier courant
                trombi_collection.append(trombi)                    # Ajout de l'objet Trombi à la liste

                logger.debug(f'Added trombi: {trombi.nom} {trombi.prenom}')

    pelican.settings['TROMBI_COLLECTION'] = trombi_collection       # Enregistrement de la liste des objets Trombi dans les settings Pelican

    logger.info('TROMBI_COLLECTION add in settings.')

    # Valorisation du dictionnaire dico_team :
    logger.info('Generating dico _team...')
    for trombi in trombi_collection:
       logger.info(f'Current trombi : {trombi.nom} {trombi.prenom} with start: {trombi.entree} -> end: {trombi.sortie}')
       entree = int(trombi.entree)
       if trombi.sortie == "":
           sortie = datetime.datetime.now().year
       else:
           sortie = int(trombi.sortie)
       for i in range(sortie - entree + 1):           
           if entree + i not in dico_team:
               dico_team[entree + i] = []           
           dico_team[entree + i] += [trombi]
    
    pelican.settings['DICO_TROMBI'] = dico_team

    logger.info('DICO_TROMBI add in setting.')


# ENREGISTREMENT DE LA LISTE DE TROMBI DANS PELICAN :
# ---------------------------------------------------
def register():
    logger.info('Registering trombi plugin...')
    signals.initialized.connect(generate_trombi)
    logger.info('Trombi plugin registered.')
