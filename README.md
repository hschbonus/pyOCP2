# 📘 Books to Scrape – Système de surveillance des prix

## 📝 Description  
Ce projet Python met en œuvre un pipeline **ETL** (Extract, Transform, Load) pour le site **BooksToScrape.com**.  
Il permet d’extraire les données des livres, de les transformer en format exploitable, et de charger les résultats dans des fichiers CSV ainsi que d’enregistrer les images associées.

## 🚀 Fonctionnalités principales  
- 📂 Extraction de **toutes les catégories** du site.  
- 🔁 Parcours complet de chaque catégorie, gestion de la pagination.  
- 📊 Extraction des informations suivantes pour chaque livre :  
  - 🆔 UPC  
  - 📖 Titre  
  - 💶 Prix TTC / HT  
  - 📦 Disponibilité  
  - 📝 Description  
  - 🏷️ Catégorie  
  - ⭐ Note (rating)  
  - 🌄 URL de l’image  
- 📷 Téléchargement de toutes les couvertures d’images (nommées selon l’UPC).  
- 📑 Génération d’un fichier CSV par catégorie.

## 🧰 Installation  
```bash
git clone https://github.com/<votre-utilisateur>/<votre-repo>.git  
cd <votre-repo>
mkdir csv
mkdir images
python -m venv venv  
# macOS / Linux  
source venv/bin/activate  
# Windows  
venv\Scripts\activate  
pip install -r requirements.txt  
```

## ​▶️​ Execution
```bash
python scrap_all_books.py
```

Une fois terminé :

- 📄 Les fichiers CSV sont générés dans le dossier csv/
- 🖼️ Les images sont enregistrées dans le dossier images/
- ⏳ Le temps total d’exécution est affiché en console