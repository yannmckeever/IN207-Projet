"""
Page 2 - Modèle Conceptuel de Données (MCD)
Agence de location de voitures
"""

import streamlit as st

st.title("1️⃣ Modèle Conceptuel de Données (MCD)")

st.markdown("---")

# ================================================================
# ÉNONCÉ DU PROBLÈME MÉTIER
# ================================================================
st.header("Énoncé du problème métier")

st.markdown("""
> **Contexte :**  
> Une entreprise de location de voitures possède plusieurs **agences** réparties 
> dans différentes villes françaises. Chaque agence dispose d'une flotte de **voitures** 
> classées par catégorie (SUV, Berline, Citadine, Utilitaire).
>
> Les **clients** (utilisateurs) peuvent louer des véhicules pour une durée déterminée, 
> ajouter une **option** à leur location (GPS, assurance, siège bébé...), 
> laisser des **avis** sur les véhicules utilisés et recevoir une **facture** 
> pour chaque location.

**Besoins identifiés :**
- Gérer les informations des agences et de leur flotte de véhicules
- Permettre aux clients de louer des voitures avec une option supplémentaire
- Collecter les avis clients sur les véhicules loués
- Générer et suivre les factures de location
- Effectuer des statistiques (chiffre d'affaires par agence, notes moyennes, etc.)
""")

st.markdown("---")

# ================================================================
# ENTITÉS ET ATTRIBUTS
# ================================================================
st.header("Entités et Attributs")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏢 AGENCES")
    st.markdown("""
    ```
    ┌─────────────────────────┐
    │        AGENCES          │
    ├─────────────────────────┤
    │  #id_agence             │
    │   nom                   │
    │   adresse               │
    │   ville                 │
    │   telephone             │
    └─────────────────────────┘
    ```
    """)

    st.subheader("🚘 VOITURES")
    st.markdown("""
    ```
    ┌─────────────────────────┐
    │        VOITURES         │
    ├─────────────────────────┤
    │  #id_voiture            │
    │   marque                │
    │   modele                │
    │   annee                 │
    │   categorie             │
    │   prix_journalier       │
    └─────────────────────────┘
    ```
    """)

    st.subheader("📅 LOCATION")
    st.markdown("""
    ```
    ┌─────────────────────────┐
    │        LOCATION         │
    ├─────────────────────────┤
    │  #id_location           │
    │   date_debut            │
    │   date_fin              │
    │   statut                │
    └─────────────────────────┘
    ```
    """)

    st.subheader("💰 FACTURE")
    st.markdown("""
    ```
    ┌─────────────────────────┐
    │        FACTURE          │
    ├─────────────────────────┤
    │  #id_facture            │
    │   montant               │
    │   date_facture          │
    │   statut_paiement       │
    └─────────────────────────┘
    ```
    """)

with col2:
    st.subheader("👤 UTILISATEURS")
    st.markdown("""
    ```
    ┌─────────────────────────┐
    │      UTILISATEURS       │
    ├─────────────────────────┤
    │  #id_utilisateur        │
    │   nom                   │
    │   prenom                │
    │   email                 │
    │   telephone             │
    │   date_naissance        │
    └─────────────────────────┘
    ```
    """)

    st.subheader("⭐ AVIS")
    st.markdown("""
    ```
    ┌─────────────────────────┐
    │          AVIS           │
    ├─────────────────────────┤
    │  #id_avis               │
    │   note                  │
    │   commentaire           │
    │   date_avis             │
    └─────────────────────────┘
    ```
    """)

    st.subheader("🔧 OPTION")
    st.markdown("""
    ```
    ┌─────────────────────────┐
    │         OPTION          │
    ├─────────────────────────┤
    │  #id_option             │
    │   nom                   │
    │   description           │
    │   prix_journalier       │
    └─────────────────────────┘
    ```
    """)

st.markdown("""
**Légende :** `#` = identifiant (clé primaire)
""")

st.markdown("---")

# ================================================================
# ASSOCIATIONS
# ================================================================
st.header("Associations")

st.markdown("""
| Association | Entité 1 | Cardinalité | Entité 2 | Cardinalité | Description |
|---|---|---|---|---|---|
| **Possède** | AGENCES | 1,n | VOITURES | 1,1 | Une agence possède plusieurs voitures |
| **Effectue** | UTILISATEURS | 0,n | LOCATION | 1,1 | Un utilisateur peut faire plusieurs locations |
| **Concerne** | VOITURES | 0,n | LOCATION | 1,1 | Une voiture peut être louée plusieurs fois |
| **Rédige** | UTILISATEURS | 0,n | AVIS | 1,1 | Un utilisateur peut rédiger plusieurs avis |
| **Évalue** | VOITURES | 0,n | AVIS | 1,1 | Une voiture peut recevoir plusieurs avis |
| **Génère** | LOCATION | 1,1 | FACTURE | 0,1 | Une location génère au plus une facture |
| **Inclut** | LOCATION | 0,1 | OPTION | 0,n | Une location peut inclure une option |
""")

st.info("""💡 Une location peut inclure **au plus une option**. Une option peut être utilisée par plusieurs locations.""")

st.markdown("---")

# ================================================================
# SCHÉMA E-A SIMPLIFIÉ
# ================================================================
st.header("Schéma Entité-Association")

st.image("pages/content/Schema_EA.png", caption="Schéma Entité-Association")

st.markdown("---")

st.success("✅ Le MCD identifie **7 entités** et **7 associations**. Le passage au MLD produira **7 tables**.")
