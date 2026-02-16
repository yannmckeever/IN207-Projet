"""
Page 3 - Création et Peuplement (DDL)
Requêtes CREATE TABLE et INSERT, création de la base SQLite
"""

import streamlit as st
import sqlite3
import os

st.title("3️⃣ Création et Peuplement (DDL)")

st.markdown("---")

# Chemin vers la base de données
DB_PATH = "database.db"

# Section : Requêtes CREATE TABLE
st.header("Requêtes CREATE TABLE")

st.markdown("""
Le DDL (Data Definition Language) permet de définir la structure de la base de données.
""")

create_table_sql = """CREATE TABLE IF NOT EXISTS Etudiant (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    age INTEGER
);"""

st.code(create_table_sql, language="sql")

st.markdown("""
**Explications :**
- `CREATE TABLE` : crée une nouvelle table
- `IF NOT EXISTS` : évite une erreur si la table existe déjà
- `INTEGER PRIMARY KEY` : clé primaire auto-incrémentée en SQLite
- `TEXT NOT NULL` : chaîne de caractères obligatoire
""")

st.markdown("---")

# Section : Requêtes INSERT
st.header("Requêtes INSERT")

st.markdown("""
Les requêtes INSERT permettent d'ajouter des données dans les tables.
""")

insert_sql = """INSERT INTO Etudiant (id, nom, prenom, age) VALUES
    (1, 'Dupont', 'Marie', 22),
    (2, 'Martin', 'Jean', 19),
    (3, 'Bernard', 'Sophie', 21),
    (4, 'Petit', 'Lucas', 23);"""

st.code(insert_sql, language="sql")

st.markdown("---")

# Afficher le contenu actuel de la base
st.subheader("Contenu actuel de la base")

if os.path.exists(DB_PATH):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Etudiant")
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            import pandas as pd
            df = pd.DataFrame(rows, columns=['id', 'nom', 'prenom', 'age'])
            st.dataframe(df, width='stretch')
        else:
            st.info("La table Etudiant est vide.")
    except Exception as e:
        st.error(f"Erreur de lecture : {e}")
