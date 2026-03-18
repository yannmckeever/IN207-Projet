"""
Page 3 - Modèle Logique de Données (MLD)
Description des tables et algèbre relationnelle
"""

import streamlit as st

st.title("2. Modèle Logique de Données (MLD)")

st.markdown("---")

# ================================================================
# RÈGLES DE PASSAGE MCD → MLD
# ================================================================
st.header("Règles de passage MCD → MLD")

st.markdown("""
- Chaque **entité** devient une **table**
- Chaque **association 1:N** → clé étrangère dans la table côté "1,1"
- Chaque **association N:M** → **table associative** avec deux clés étrangères
- Chaque **association 1:1** → clé étrangère dans la table la plus pertinente
""")

st.markdown("---")

# ================================================================
# DESCRIPTION DES TABLES
# ================================================================
st.header("Description des tables")

# Table Agences
st.subheader("Table : Agences")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_agence` | INTEGER | **PRIMARY KEY** |
| `nom` | TEXT | NOT NULL |
| `adresse` | TEXT | NOT NULL |
| `ville` | TEXT | NOT NULL |
| `telephone` | TEXT | — |
""")

# Table Utilisateurs
st.subheader("Table : Utilisateurs")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_utilisateur` | INTEGER | **PRIMARY KEY** |
| `nom` | TEXT | NOT NULL |
| `prenom` | TEXT | NOT NULL |
| `email` | TEXT | UNIQUE, NOT NULL |
| `telephone` | TEXT | — |
| `date_naissance` | DATE | — |
""")

# Table Voitures
st.subheader("Table : Voitures")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_voiture` | INTEGER | **PRIMARY KEY** |
| `marque` | TEXT | NOT NULL |
| `modele` | TEXT | NOT NULL |
| `annee` | INTEGER | — |
| `categorie` | TEXT | NOT NULL |
| `prix_journalier` | REAL | NOT NULL |
| `id_agence` | INTEGER | **FOREIGN KEY → Agences** |
""")

# Table Option
st.subheader("Table : Option")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_option` | INTEGER | **PRIMARY KEY** |
| `nom` | TEXT | NOT NULL |
| `description` | TEXT | — |
| `prix_journalier` | REAL | NOT NULL |
""")

# Table Location
st.subheader("Table : Location")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_location` | INTEGER | **PRIMARY KEY** |
| `id_utilisateur` | INTEGER | **FOREIGN KEY → Utilisateurs** |
| `id_voiture` | INTEGER | **FOREIGN KEY → Voitures** |
| `id_option` | INTEGER | **FOREIGN KEY → Option** |
| `date_debut` | DATE | NOT NULL |
| `date_fin` | DATE | NOT NULL |
| `statut` | TEXT | DEFAULT 'en_cours' |
""")

# Table Avis
st.subheader("Table : Avis")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_avis` | INTEGER | **PRIMARY KEY** |
| `id_utilisateur` | INTEGER | **FOREIGN KEY → Utilisateurs** |
| `id_voiture` | INTEGER | **FOREIGN KEY → Voitures** |
| `note` | INTEGER | CHECK (1 à 5) |
| `commentaire` | TEXT | — |
| `date_avis` | DATE | — |
""")

# Table Facture
st.subheader("Table : Facture")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_facture` | INTEGER | **PRIMARY KEY** |
| `id_location` | INTEGER | **FOREIGN KEY → Location** |
| `montant` | REAL | NOT NULL |
| `date_facture` | DATE | — |
| `statut_paiement` | TEXT | DEFAULT 'en_attente' |
""")

st.markdown("---")

# ================================================================
# SCHÉMA RELATIONNEL RÉSUMÉ
# ================================================================
st.header("Schéma relationnel")

st.code("""
Agences (id_agence, nom, adresse, ville, telephone)
Utilisateurs (id_utilisateur, nom, prenom, email, telephone, date_naissance)
Voitures (id_voiture, marque, modele, annee, categorie, prix_journalier, #id_agence)
Option (id_option, nom, description, prix_journalier)
Location (id_location, #id_utilisateur, #id_voiture, #id_option, date_debut, date_fin, statut)
Avis (id_avis, #id_utilisateur, #id_voiture, note, commentaire, date_avis)
Facture (id_facture, #id_location, montant, date_facture, statut_paiement)
""", language="text")

st.markdown("**Légende :** `#attribut` = clé étrangère")

st.markdown("---")

# ================================================================
# ALGÈBRE RELATIONNELLE
# ================================================================
st.header("Algèbre Relationnelle")

st.markdown("""
L'algèbre relationnelle est un langage formel pour manipuler les relations (tables).
Voici les opérateurs utilisés :
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**Sélection (σ)**")
    st.latex(r"\sigma_{cond}(R)")

with col2:
    st.markdown("**Projection (π)**")
    st.latex(r"\pi_{attr}(R)")

with col3:
    st.markdown("**Jointure (⋈)**")
    st.latex(r"R \bowtie S")

with col4:
    st.markdown("**Division (÷)**")
    st.latex(r"R \div S")

st.markdown("---")


