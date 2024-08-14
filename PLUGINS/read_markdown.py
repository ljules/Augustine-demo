
# DESCRIPTION :
#--------------

# Ce plugin permet de rajouter du contenu du spécifique à l'environnement de Pelican.
# Le contenu est lu à partir d'un fichier Markdown.

# Script généré avec l'aide de Chat GPT.


# IMPORTS :
# ---------
import os
from pelican import signals
from markdown import markdown


# GESTION DES LOGS :
# ------------------
import logging
logger = logging.getLogger(__name__)


# CONFIGURATION :
# ---------------

#NOM_FICHIER_MD = "accueil.md"   # Fichier Markdown contenant le contenu à intégrer
NOM_FICHIER_MD = os.path.abspath("content/accueil.md")
NOM_CONTENU = 'accueil'  # Nom donné au contenu dans le contexte de Pelican


# LECTURE DU CONTENU :
# --------------------
def add_extra_context(generator, metadata):
    md_file_path = os.path.join(generator.settings['PATH'], 'content', NOM_FICHIER_MD)
    
    logger.info(f"Checking for markdown file at: {md_file_path}")

    if os.path.exists(md_file_path):
        with open(md_file_path, 'r', encoding='utf-8') as md_file:                        
            content = md_file.read()
            logger.debug(f"Markdown content: {content[:100]}...")  # Log first 100 chars
            html_content = markdown(content)
            logger.debug(f"Generated HTML content: {html_content[:100]}...")  # Log first 100 chars
            generator.context[NOM_CONTENU] = html_content
    else:
        logger.warning(f"Markdown file not found at: {md_file_path}")

# Connexion aux signaux
#signals.article_generator_context.connect(add_extra_context)
#signals.page_generator_context.connect(add_extra_context)


# AJOUT DU CONTENU AU CONTEXT DE PELICAN :
# ----------------------------------------
def register():
    signals.article_generator_context.connect(add_extra_context)
    signals.page_generator_context.connect(add_extra_context)

