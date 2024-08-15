---
layout: docs
title: readme.md
author: L. JULES
---

# Site Augustine avec le gestionnaire de site statique **Pelican**

## Bref présentation :
Vous trouverez de la documentation plus détaillée dans le dossier `DOCUMENTATION` :
- Guide d'installation et configuration de Pelican pour Windows : `DOCUMENTATION/Guide Pelican avec Windows.md`
- Guide pour la rédaction des articles : `DOCUMENTATION/Guide articles.md`

Voici un rappel des principales commandes :
- `pelican content` : Génère l'ensemble des fichiers du projet en utilisant la configuration du fichier `pelicanconf.py`
- `pelican -lr` : Exécute le serveur local de **Pelican** pour tester le site en local, l'URL est : http://localhost:8000 
- `pelican content -s publishconf.py` : Génère l'ensemble des fichiers dans l'objectif de procéder à la mise en production du site.

## Dépendances :
La construction du site nécessite d'avoir la bibliothèque **pillow**.


