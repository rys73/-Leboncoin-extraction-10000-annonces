# Leboncoin Scraper (Playwright)

Petit script Python qui permet de récupérer des annonces sur **Leboncoin** (titre, prix et lien) et de les enregistrer dans un fichier **CSV**.

Le script est ecrit avec la bibliothèque **Playwright** et fonction de manière asynchrone qui veut dire ne pas perdre de temps à attendre, donc faire plusieurs "en parallèle" dans le même prgramme.
--

## A quoi sert ce programme ?
- Lancer une recherche (ex: Iphone, voiture, etc.)
- Parcourir automatiquement les pages de résultats
- Récupérer des données:
  - le nom de l'annonce
  - le prix
  - le lien
- Sauvegarder en temps réel dans un fichier csv.
---

## Fonctionnalités principales
- Recherche automatique sur Leboncoin
- Gestion de la popup cookies
- Pagination (page suivante automatique)
- Sauvegarde progessive en temps réel dans un CSV
- Fermeture propre du navigateur **(Chromium)**

