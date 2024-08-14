# -------------------------------------------------------------------
#                               PERF PLUGIN
# -------------------------------------------------------------------

# Description :
# -------------
# Plugin permettant de parcourir un fichier csv : performance.csv
# A l'issu du parcours, le plugin génère un dictionnaire de dictionnaires.
# La clé du dictionnaire est 'session' et sa valeur l'année concernée.
# Les sous-dictionnaires contiennent en clé le nom des colonnes du csv
# et en valeurs, les valeurs des colonnes pour l'année considérée.


# IMPORTS :
# ---------
import os
import csv
import logging
from pelican import signals

# Configurer le logger pour le plugin
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def parse_csv_to_dict(file_path):
    """Parse the CSV file and return a dictionary of dictionaries."""
    result = {}
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:  # Note the 'utf-8-sig' encoding
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            session = row.pop('session')
            result[session] = row
            logger.info(f"Session {session} loaded with data: {row}")
    return result

def add_global_context(generator):
    """Add the parsed data to the global context of Pelican."""
    content_path = generator.settings.get('PATH')
    csv_path = os.path.join(content_path, 'pages', 'Performances', 'performances.csv')
    
    if os.path.exists(csv_path):
        logger.info(f"Reading CSV file at {csv_path}")
        generator.context['DICO_PERF'] = parse_csv_to_dict(csv_path)
        logger.info("CSV data successfully loaded into DICO_PERF.")
    else:
        logger.warning(f"CSV file not found at {csv_path}")

def register():
    """Plugin registration."""
    signals.generator_init.connect(add_global_context)
