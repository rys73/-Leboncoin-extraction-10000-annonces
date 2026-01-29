# Leboncoin Scraper (Playwright)

Petit script Python qui permet de récupérer des annonces sur **Leboncoin** (titre, prix et lien) et de les enregistrer dans un fichier **CSV**.

Le script est ecrit avec la bibliothèque **Playwright** et fonction de manière asynchrone qui veut dire ne pas perdre de temps à attendre, donc faire plusieurs "en parallèle" dans le même prgramme.
Ce code il inclue également des **techniques anti-bot** avec des **timeout aléatoires (random)** pour éviter d'être bloque.
--

## A quoi sert ce programme ?
- Lancer une recherche (ex: Iphone, voiture, etc.)
- Sauvegarder les noms, prix et liens dans un CSV
- Navigue comme un vrai utilisateur grâce à :
  - anti-bot simple
  - délais alétoires entre les actions (mouse move, clics, chargement)
- Parcourir jusqu'à plus de 100 pages automatiquement et rapidement
---

## Fonctionnalités principales
- Recherche automatique sur Leboncoin
- Gestion de la popup cookies
- Sauvegarde progressive dans un CSV
- Anti-bot intégré avec :
  - modification du user_agent
  - désactivation de `navigator.webdriver`
  - mouvement de souris simulés
- Attentes aléatoires entre les actions pour paraître naturel
- Fermeture propre du navigateur **(Chromium)**
- Logs simple pour suivre le déroulement des événements
---

## Prérequis
- Python 3
- Playwright
- os

Installation de Playwright :
```bash
pip install playwright
playwright install

