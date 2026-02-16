# IN207 - Introduction aux Bases de Données

## Description

Application pédagogique Streamlit illustrant les étapes de conception d'une base de données relationnelle.

Ce projet accompagne le cours IN207 et présente les étapes fondamentales de la modélisation et de l'interrogation d'une base de données.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

L'application sera accessible dans votre navigateur à l'adresse `http://localhost:8501`.

## Outil recommandé : DB Browser for SQLite

> **En parallèle de l'application Streamlit, nous recommandons l'utilisation de [DB Browser for SQLite](https://sqlitebrowser.org/) pour concevoir et tester votre base de données.**

L'application Streamlit sert à **illustrer et présenter** votre travail de manière interactive. En revanche, pour le travail de conception au quotidien (créer vos tables, insérer des données de test, expérimenter vos requêtes SQL), **DB Browser for SQLite** est un outil visuel bien plus adapté.

DB Browser for SQLite (DB4S) est un outil open source qui permet de :
- Concevoir et modifier la structure des tables
- Parcourir, ajouter et éditer des enregistrements facilement
- Tester et déboguer vos requêtes SQL avant de les intégrer à Streamlit
- Importer/exporter des données (CSV, SQL)

**Téléchargement** : [https://sqlitebrowser.org/dl/](https://sqlitebrowser.org/dl/)

Disponible sur Windows, macOS et Linux.

## Structure du projet

```
in207/
├── README.md
├── requirements.txt
├── .gitignore
├── app.py                  # Point d'entrée et navigation
├── database.db             # Base SQLite
└── pages/
    ├── 1_Accueil.py        # Page d'accueil
    ├── 2_MCD.py            # Modèle Conceptuel de Données
    ├── 3_MLD.py            # Modèle Logique de Données
    ├── 4_DDL.py            # Création et peuplement
    └── 5_Requetes.py       # Requêtes SQL
```

---

## Travail à réaliser

### Étape 1 : Modèle Conceptuel de Données (MCD)

- Proposer une **application métier réaliste** de votre choix
- Identifier les **entités** et leurs **attributs**
- Définir les **associations** entre entités (cardinalités)
- Produire un **schéma entité-association** (diagramme E-A)
- Le schéma doit comporter suffisamment d'entités pour générer **au moins 4 tables** dans le MLD

### Étape 2 : Modèle Logique de Données (MLD)

- Traduire le MCD en **schéma relationnel** (au moins 4 tables)
- Définir pour chaque table : attributs, types, clés primaires, clés étrangères
- Documenter les **contraintes d'intégrité**
- Rédiger **10 requêtes en algèbre relationnelle** minimum, dont :
  - Sélections (σ)
  - Projections (π)
  - Jointures (⋈)
  - **2 divisions (÷)** obligatoires

### Étape 3 : Création et peuplement (DDL)

- Écrire les requêtes **CREATE TABLE** pour chaque table
- Écrire les requêtes **INSERT** pour peupler la base avec des données de test
- Implémenter la création/réinitialisation de la base SQLite

### Étape 4 : Requêtes SQL

- **10 requêtes SQL** traduisant les 10 requêtes d'algèbre relationnelle de l'étape 2
- **10 requêtes SQL supplémentaires** impliquant :
  - Des **fonctions d'agrégation** (COUNT, SUM, AVG, MIN, MAX)
  - Des **regroupements** (GROUP BY)
  - Des **filtres sur agrégats** (HAVING)

### Étape 5 : Valorisation des données

Créez une **page Streamlit supplémentaire** (`6_Valorisation.py`) pour illustrer l'intérêt de votre base de données au-delà des simples requêtes.

**Exemples possibles** : tableau de bord, graphiques dynamiques, filtres interactifs, recherche par critères...

---

## Récapitulatif des livrables et notation

| Étape | Contenu attendu | Barème |
|-------|-----------------|--------|
| MCD | Schéma E-A avec entités, attributs, associations | /4 |
| MLD | 4+ tables, 10+ requêtes algèbre relationnelle (dont 2 divisions) | /4 |
| DDL | CREATE TABLE + INSERT pour toutes les tables | /4 |
| SQL | 10 requêtes (traduction algèbre) + 10 requêtes (agrégats / GROUP BY / HAVING) | /4 |
| Valorisation | Interagir avec les données de manière créative | /4 |

### Répartition des points par étape

Pour chaque étape, les 4 points sont répartis ainsi :
- **2 points** : qualité du code (lisibilité, structure, fonctionnement)
- **2 points** : qualité de la présentation lors de la soutenance

### Utilisation de l'IA générative

L'utilisation d'outils d'IA générative (ChatGPT, Claude, Copilot, etc.) est **autorisée et encouragée**. Cependant, vous devez être capable d'**expliquer et de justifier** l'ensemble de votre travail lors de la soutenance.
