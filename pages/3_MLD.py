"""
Page 3 - Modèle Logique de Données (MLD)
Description des tables et algèbre relationnelle
"""

import streamlit as st

st.title("2️⃣ Modèle Logique de Données (MLD)")

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
st.subheader("🏢 Table : Agences")
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
st.subheader("👤 Table : Utilisateurs")
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
st.subheader("🚘 Table : Voitures")
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
st.subheader("🔧 Table : Option")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_option` | INTEGER | **PRIMARY KEY** |
| `nom` | TEXT | NOT NULL |
| `description` | TEXT | — |
| `prix_journalier` | REAL | NOT NULL |
""")

# Table Location
st.subheader("📅 Table : Location")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_location` | INTEGER | **PRIMARY KEY** |
| `id_utilisateur` | INTEGER | **FOREIGN KEY → Utilisateurs** |
| `id_voiture` | INTEGER | **FOREIGN KEY → Voitures** |
| `date_debut` | DATE | NOT NULL |
| `date_fin` | DATE | NOT NULL |
| `statut` | TEXT | DEFAULT 'en_cours' |
""")

# Table Avis
st.subheader("⭐ Table : Avis")
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
st.subheader("💰 Table : Facture")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_facture` | INTEGER | **PRIMARY KEY** |
| `id_location` | INTEGER | **FOREIGN KEY → Location** |
| `montant` | REAL | NOT NULL |
| `date_facture` | DATE | — |
| `statut_paiement` | TEXT | DEFAULT 'en_attente' |
""")

# Table associative Location_Option
st.subheader("🔗 Table associative : Location_Option")
st.markdown("""
| Attribut | Type | Contraintes |
|----------|------|-------------|
| `id_location` | INTEGER | **PK, FOREIGN KEY → Location** |
| `id_option` | INTEGER | **PK, FOREIGN KEY → Option** |

> Cette table résulte de l'association **N:M** entre Location et Option.
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
Location (id_location, #id_utilisateur, #id_voiture, date_debut, date_fin, statut)
Avis (id_avis, #id_utilisateur, #id_voiture, note, commentaire, date_avis)
Facture (id_facture, #id_location, montant, date_facture, statut_paiement)
Location_Option (#id_location, #id_option)
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

# ---- 10 REQUÊTES EN ALGÈBRE RELATIONNELLE ----
st.header("10 requêtes en algèbre relationnelle")

# Requête 1
with st.expander("**Requête 1** — Sélection : Utilisateurs nés avant 1995"):
    st.markdown("Trouver tous les utilisateurs nés avant le 1er janvier 1995.")
    st.latex(r"\sigma_{date\_naissance < '1995\text{-}01\text{-}01'}(Utilisateurs)")

# Requête 2
with st.expander("**Requête 2** — Projection : Marques et modèles des voitures"):
    st.markdown("Afficher uniquement les marques et modèles de toutes les voitures.")
    st.latex(r"\pi_{marque,\ modele}(Voitures)")

# Requête 3
with st.expander("**Requête 3** — Sélection + Projection : Voitures de catégorie SUV"):
    st.markdown("Afficher les marques et modèles des voitures de catégorie SUV.")
    st.latex(r"\pi_{marque,\ modele}(\sigma_{categorie = 'SUV'}(Voitures))")

# Requête 4
with st.expander("**Requête 4** — Jointure : Locations avec noms des utilisateurs"):
    st.markdown("Afficher les locations avec le nom et prénom du client.")
    st.latex(r"Location \bowtie_{id\_utilisateur} Utilisateurs")

# Requête 5
with st.expander("**Requête 5** — Jointure : Voitures avec leur agence"):
    st.markdown("Afficher chaque voiture avec le nom de son agence.")
    st.latex(r"\pi_{marque,\ modele,\ categorie,\ nom}(Voitures \bowtie_{id\_agence} Agences)")

# Requête 6
with st.expander("**Requête 6** — Jointure + Sélection : Avis avec note ≥ 4"):
    st.markdown("Afficher les avis avec note ≥ 4 et le nom de l'utilisateur.")
    st.latex(r"\pi_{nom,\ prenom,\ note,\ commentaire}(\sigma_{note \geq 4}(Avis \bowtie_{id\_utilisateur} Utilisateurs))")

# Requête 7
with st.expander("**Requête 7** — Jointures multiples : Factures détaillées"):
    st.markdown("Afficher les factures avec le nom du client et la voiture louée.")
    st.latex(r"\pi_{nom,\ prenom,\ marque,\ modele,\ montant}(Facture \bowtie Location \bowtie Utilisateurs \bowtie Voitures)")

# Requête 8
with st.expander("**Requête 8** — Jointure : Options choisies par location"):
    st.markdown("Afficher les options associées à chaque location.")
    st.latex(r"\pi_{id\_location,\ nom}(Location\_Option \bowtie_{id\_option} Option)")

# Requête 9 — DIVISION
with st.expander("**Requête 9** — ÷ Division : Utilisateurs ayant loué dans TOUTES les agences"):
    st.markdown("Trouver les utilisateurs qui ont loué au moins une voiture dans **chacune** des agences.")
    st.latex(r"\pi_{id\_utilisateur,\ id\_agence}(Location \bowtie Voitures) \div \pi_{id\_agence}(Agences)")

# Requête 10 — DIVISION
with st.expander("**Requête 10** — ÷ Division : Utilisateurs ayant loué TOUTES les catégories"):
    st.markdown("Trouver les utilisateurs qui ont loué au moins une voiture de **chaque** catégorie.")
    st.latex(r"\pi_{id\_utilisateur,\ categorie}(Location \bowtie Voitures) \div \pi_{categorie}(Voitures)")

st.markdown("---")

st.success("✅ Le MLD définit 8 tables avec leurs contraintes. Les 10 requêtes d'algèbre relationnelle incluent **2 divisions (÷)**.")
