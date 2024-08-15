#########################################################
#                                                       #
#   FICHIER DE CONFIGURATION PERSONNALISE AUGUSTINE     #
#                                                       #
#########################################################


# GENERATION SUR LES LOGS :
# -------------------------

import logging
import os

# Décommenter le code ci-dessous pour activer le journal de log :
"""
# Définir le chemin complet pour le fichier de log
LOG_FILE = os.path.join(os.path.dirname(__file__), 'pelican_debug.log')

# Configuration du logger
logger = logging.getLogger()   
logger.setLevel(logging.DEBUG)

# Créer un gestionnaire pour écrire les logs dans un fichier
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Créer un gestionnaire pour afficher les logs dans la console
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# console_handler.setFormatter(console_formatter)
# logger.addHandler(console_handler)
"""


# INFORMATIONS GENERALES DU SITE :
# --------------------------------

AUTHOR = 'Membres équipe Augustine'
SITENAME = 'Augustine'
TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = 'fr'
#SITEURL = 'https://ljules.github.io/Augustine-Tests'
SITEURL = ''
RELATIVE_URLS = True # Est surchargé par la valeur False dans le fichier publishconf.py


# OPTIONS DE STRUCTURATION DU SITE :
# ----------------------------------

# Pagination des articles :
DEFAULT_PAGINATION = 3          # Nombre d'articles par pages
SUMMARY_MAX_LENGTH = 100        # Longueur des résumés par défaut des articles
#DEFAULT_DATE = None  # fs pour file system, indique la date du système, none pour ne pas générer la date


# Création des catégories pour les articles :
USE_FOLDER_AS_CATEGORY = True
DEFAULT_CATEGORY = "Sans catégorie"


# ELEMENTS DE NAVIGATION :
# ------------------------

# Choix des éléments de navigation par pages et/ou catégories gérés nativement par PELICAN :
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
MENUITEMS = [("LdV", "https://www.vinci-melun.org/")] # Une liste de tuples (Titre, URL) complémentaires pour la barre de menu (Apparait en tête)


# Navigation SPECIFIQUE au thème AUGUSTINE :
# ((nom, url, icone, (nom, url, icone)),...)
NAV_SITE_AUGUSTINE = (#("Home", "/", "bi bi-house-fill", None),
                      ("Articles", "", "feather", (
                            ("Archive des articles", "/archives"),
                            ("Liste des catégories", "/categories"),
                            ("Liste des auteurs", "/authors"),
                            ("Liste des mots clés", "/tags"))),
                      ("Equipes", "", "people-fill", (
                            ("Trombinoscope", "/pages/trombi"),
                            ("Liste des équipes", "/pages/equipes"))),
                      ("Galerie", "", "image-fill", []), # ATTENTION : L'indice de la galerie doit être renseignée dans le plugin gallery_plugin
                      ("Véhicules", "", "ev-front-fill", (
                          ("Augustine I", "/pages/augustine-1"),
                          ("Augustine II", "/pages/augustine-2"),
                          ("Augustine III", "/pages/augustine-3"),
                          ("Augustine IV", "/pages/augustine-4"),
                          ("Augustine V", "/pages/augustine-5"))),
                      ("Performances", "/pages/performances", "trophy-fill", None),
                      ("A propos", "", "info-circle-fill", (
                          ("De nous", "/pages/a-propos-de-nous"),
                          ("De l'Eco-marathon", "/pages/a-propos-du-shell"),
                          ("On parle de nous", "/pages/on-parle-de-nous"),
                          ("Devenir partenaire", "/pages/devenir-partenaire")))
                    )



# CHEMINS POUR LE CONTENU DE DEVELOPPEMENT :
# ------------------------------------------

THEME = 'THEMES/Augustine-theme'
#THEME = 'THEMES/notmyidea'
PATH = 'content'
ARTICLE_PATHS = ['articles']   # Sous-dossier de PATH qui contient les articles.
PAGE_PATHS = ['pages']         # Dossier qui contient les pages statiques du site.
STATIC_PATHS = ['images', 'videos', 'trombi', 'galerie']
OUTPUT_PATH = 'docs'           # Attention, pour la publication sur GitHub Pages le dossier doit être "/docs"


# CONFIGURATION DES PLUGINS :
# ---------------------------

# Chemin vers le dossier des plugins
PLUGIN_PATHS = ['PLUGINS']

# Liste des plugins à utiliser
PLUGINS = ['read_markdown', 'trombi_plugin', 'perf_plugin', 'gallery_plugin']
#PLUGINS = None # Désactive les plugins



# Eléments de template personnalisé à copier dans le fichier de production :
#TEMPLATE_PAGES = {'home.html': 'home.html'} # fichier_template.html: fichier_out.html

#THEME_TEMPLATES_OVERRIDES = ['templates']


# OPTION DE PERSONNALISATION DU THEME :
# -------------------------------------

# Valeurs pour l'entête :
# -----------------------
SITESUBTITLE = """Plus loin <i class="bi bi-speedometer"></i>, Moins d'énergie <i class="bi bi-battery-full"></i>"""
LOGOS = ("Logo_tournesol.jpg", "logo&baseline-fondblanc.png")


# Caroussel :
# -----------
CAROUSEL = (("augustine_2017-01-R.jpg", "Un véhicule électrique", "Réalisé par notre équipe."),
             ("session_2024-R.jpg", "Une équipe de professeurs & d'étudiants", "Pour vivre ensemble l'aventure."),
             ("augustine_2017-03-R.jpg", "Un objectif", "Prendre part au challenge international du Shell Eco-Marthon."))



# Valeur pour le pied de page :
# -----------------------------

# Nous contacter :
POSTAL_ADDRESS_LINE_1 = "Lycée Léonard de Vinci"
POSTAL_ADDRESS_LINE_2 = "2, bis rue Edouard Branly"
POSTAL_ADDRESS_LINE_3 = "77000 MELUN CEDEX"
PHONE_NUMBER = "+33 1 60 60 56 60"
GOOGLE_MAP = "https://maps.google.com/?q=Lyc%C3%A9e%20Vinci,%20Melun"


# Nous suivre (Texte, URL, nom icône Bootstrap):
SOCIAL = (("Instagram", "https://www.instagram.com/augusteam.ldv", "instagram"),
          ("Facebook", "https://www.facebook.com/AugustineShellEco", "facebook"))


# Autres liens :
LINKS = (("Site du lycée", "https://www.vinci-melun.org/", "ldv.png"),
         ("Site Shell Eco-Marathon", "https://www.shellecomarathon.com/", "shell-flat.png"),
         ("Site Shell Eco-Marathon France", "https://www.shell.fr/energie-innovation/shell-eco-marathon.html", "shell-flat.png"))


# Bas pied de page :
# ------------------
LINES = ("Section de Technicien Supérieur <b>CPI</b> du Lycée <b>Léonard de Vinci</b>",
         "Site développé par la S.T.S. <b>SIO</b> du Lycée <b>Léonard de Vinci</b>")



# OPTIONS & CONFIGURATION DE GENERATION DU SITE :
# -----------------------------------------------
DELETE_OUTPUT_DIRECTORY = False



# OPTIONS POUR LES FLUX DE CONTENU :
# ----------------------------------

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None







