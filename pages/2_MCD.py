"""
Page 1 - Modèle Conceptuel de Données (MCD)
Présentation du problème métier et du schéma entité-association
"""

import streamlit as st

st.title("1️⃣ Modèle Conceptuel de Données (MCD)")

st.markdown("---")

# Section : Énoncé du problème métier
st.header("Énoncé du problème métier")

st.markdown("""
> **Contexte :**  
> Une université souhaite gérer les informations de ses étudiants.
> Pour commencer simplement, nous allons modéliser uniquement les étudiants
> avec leurs informations de base.

**Besoins identifiés :**
- Stocker les informations des étudiants (nom, prénom, âge)
- Pouvoir identifier chaque étudiant de manière unique
- Permettre des recherches et des statistiques sur les étudiants
""")

st.info("💡 Dans un cas réel, l'énoncé serait plus complexe avec plusieurs entités (cours, professeurs, inscriptions, etc.)")

st.markdown("---")

# Section : Schéma entité-association
st.header("Schéma Entité-Association")

st.markdown("""
Pour ce problème simplifié, nous avons une seule entité :
""")

# Représentation textuelle du schéma E-A
st.subheader("Entité : ETUDIANT")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    ```
    ┌─────────────────────────┐
    │        ETUDIANT         │
    ├─────────────────────────┤
    │  #id                    │
    │   nom                   │
    │   prenom                │
    │   age                   │
    └─────────────────────────┘
    ```
    """)

st.markdown("""
**Légende :**
- `#` : identifiant (clé primaire)
- Les autres attributs sont des propriétés de l'entité
""")

st.markdown("---")

# Placeholder pour une image
st.subheader("📷 Schéma graphique (placeholder)")

st.warning("""
**Emplacement réservé pour un schéma graphique**

Vous pouvez ajouter ici une image de votre schéma entité-association :
```python
st.image("chemin/vers/schema_mcd.png", caption="Schéma E-A")
```
""")

st.markdown("---")

st.success("✅ Le MCD est la première étape : on identifie les entités et leurs attributs sans se soucier de l'implémentation technique.")
