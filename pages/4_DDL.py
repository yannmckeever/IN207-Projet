"""
Page 4 - Création et Peuplement (DDL)
Agence de location de voitures
Lit le fichier init_db.sql pour créer et peupler la base.
"""

import streamlit as st
import sqlite3
import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

st.title("3️⃣ Création et Peuplement (DDL)")

st.markdown("---")

DB_PATH = os.path.join(PROJECT_ROOT, "database.db")
SQL_PATH = os.path.join(PROJECT_ROOT, "init_db.sql")

# ================================================================
# LECTURE DU FICHIER SQL
# ================================================================

if not os.path.exists(SQL_PATH):
    st.error(f"❌ Fichier `{SQL_PATH}` introuvable.")
    st.stop()

with open(SQL_PATH, "r", encoding="utf-8") as f:
    sql_script = f.read()

# ================================================================
# AFFICHAGE DU CONTENU SQL
# ================================================================
st.header("Fichier SQL : `init_db.sql`")

st.markdown("Le fichier `init_db.sql` contient toutes les requêtes de création et de peuplement de la base.")

st.code(sql_script, language="sql")

st.markdown("""
**Explications :**
- `PRIMARY KEY` : identifiant unique de chaque enregistrement
- `FOREIGN KEY` : clé étrangère référençant une autre table
- `NOT NULL` : valeur obligatoire
- `UNIQUE` : valeur unique dans la table
- `CHECK` : contrainte de validité (note entre 1 et 5)
- `DEFAULT` : valeur par défaut
""")

st.markdown("---")

# ================================================================
# BOUTON DE CRÉATION DE LA BASE
# ================================================================
st.header("Création de la base de données")

if st.button("🔄 Créer / Réinitialiser la base de données", type="primary"):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(sql_script)
        conn.commit()
        st.success("✅ Base de données créée et peuplée avec succès à partir de `init_db.sql` !")
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
    finally:
        conn.close()

st.markdown("---")

# ================================================================
# AFFICHAGE DU CONTENU DE LA BASE
# ================================================================
st.header("Contenu actuel de la base")

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)

    tables = [
        "Agences", "Utilisateurs", "Voitures", "Option",
        "Location", "Avis", "Facture"
    ]

    for table in tables:
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            st.subheader(f"📋 {table} ({len(df)} lignes)")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.warning(f"Table {table} : {e}")

    conn.close()
else:
    st.info("📭 Aucune base de données trouvée. Cliquez sur le bouton ci-dessus pour la créer.")
