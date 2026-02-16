"""
Page 1 - Accueil du cours IN207
"""

import streamlit as st

# Titre principal
st.title("IN207 - Introduction aux Bases de Données")

st.markdown("---")

# Présentation du projet
st.header("Bienvenue !")

st.markdown("""
Cette application pédagogique vous accompagne dans la découverte des **bases de données relationnelles**.

Vous allez explorer les 4 étapes fondamentales de la conception d'une base de données :
""")

# Présentation des 4 étapes
col1, col2 = st.columns(2)

with col1:
    st.subheader("1️⃣ Modèle Conceptuel de Données (MCD)")
    st.markdown("""
    - Analyse du problème métier
    - Identification des entités et associations
    - Schéma entité-association
    """)
    
    st.subheader("2️⃣ Modèle Logique de Données (MLD)")
    st.markdown("""
    - Traduction du MCD en tables
    - Définition des attributs et types
    - Clés primaires et étrangères
    - Introduction à l'algèbre relationnelle
    """)

with col2:
    st.subheader("3️⃣ Création et Peuplement (DDL)")
    st.markdown("""
    - Requêtes CREATE TABLE
    - Requêtes INSERT
    - Création de la base SQLite
    """)
    
    st.subheader("4️⃣ Requêtes SQL")
    st.markdown("""
    - Requêtes SELECT
    - Filtrage, projection, jointures
    - Correspondance avec l'algèbre relationnelle
    """)

st.markdown("---")

st.info("👈 Utilisez le menu latéral pour naviguer entre les différentes étapes.")
