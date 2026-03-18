"""
Page 1 - Accueil du projet IN207
Agence de location de voitures
"""

import streamlit as st

# Titre principal
st.title("IN207 - Agence de Location de Voitures")

st.markdown("---")

# Présentation du projet
st.header("Bienvenue !")

st.markdown("""
Cette application présente la conception d'une **base de données relationnelle** 
pour une **agence de location de voitures**.

**Contexte métier :** Une entreprise de location de véhicules possède plusieurs 
agences réparties dans différentes villes. Elle souhaite gérer sa flotte de voitures, 
ses clients, les locations avec option, les avis clients et la facturation.
""")

st.markdown("---")

# Présentation des tables
st.header("Tables de la base de données")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Agences")
    st.markdown("Informations sur les agences de location")

    st.subheader("Utilisateurs")
    st.markdown("Clients de l'agence de location")

    st.subheader("Voitures")
    st.markdown("Flotte de véhicules disponibles")

    st.subheader("Option")
    st.markdown("Options supplémentaires (GPS, assurance...)")

with col2:
    st.subheader("Location")
    st.markdown("Réservations de véhicules par les clients")

    st.subheader("Avis")
    st.markdown("Évaluations des véhicules par les clients")

    st.subheader("Facture")
    st.markdown("Facturation des locations")

st.markdown("---")

# Présentation des 4 étapes
st.header("Étapes du projet")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Modèle Conceptuel (MCD)")
    st.markdown("""
    - Analyse du problème métier
    - Identification des entités et associations
    - Schéma entité-association
    """)

    st.subheader("2. Modèle Logique (MLD)")
    st.markdown("""
    - Traduction du MCD en tables
    - Définition des attributs et types
    - Algèbre relationnelle (10 requêtes)
    """)

with col2:
    st.subheader("3. Création et Peuplement (DDL)")
    st.markdown("""
    - Requêtes CREATE TABLE
    - Requêtes INSERT
    - Création de la base SQLite
    """)

    st.subheader("4. Requêtes SQL")
    st.markdown("""
    - 10 requêtes (algèbre relationnelle → SQL)
    - 10 requêtes avec agrégation
    - GROUP BY, HAVING, fonctions d'agrégat
    """)

st.markdown("---")

st.info("Utilisez le menu latéral pour naviguer entre les différentes étapes.")

