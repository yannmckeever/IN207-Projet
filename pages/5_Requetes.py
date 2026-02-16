"""
Page 4 - Requêtes SQL
Requêtes SELECT avec correspondance algèbre relationnelle
"""

import streamlit as st
import sqlite3
import pandas as pd
import os

st.title("4️⃣ Requêtes SQL")

st.markdown("---")

# Chemin vers la base de données
DB_PATH = "database.db"


def executer_requete(sql):
    """Exécute une requête SQL et retourne un DataFrame"""
    if not os.path.exists(DB_PATH):
        return None
    
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
        return df
    except Exception as e:
        st.error(f"Erreur SQL : {e}")
        return None
    finally:
        conn.close()


# Vérifier si la base existe
if not os.path.exists(DB_PATH):
    st.warning("⚠️ La base de données n'existe pas. Veuillez d'abord la créer dans la page DDL.")
    st.stop()

# Requête 1 : Sélection de tous les étudiants
st.header("1. Afficher tous les étudiants")

sql1 = "SELECT * FROM Etudiant;"

col1, _, col3 = st.columns([1, 1, 2])

with col1:
    st.subheader("Algèbre relationnelle")
    st.latex(r"Etudiant")

with col3:
    st.subheader("SQL")
    st.code(sql1, language="sql")

st.subheader("Résultat")
df1 = executer_requete(sql1)
if df1 is not None:
    st.dataframe(df1, width='stretch')

st.markdown("---")

# Requête 2 : Projection (noms et prénoms)
st.header("2. Projection : noms et prénoms uniquement")

sql2 = "SELECT nom, prenom FROM Etudiant;"

col1, _, col3 = st.columns([1, 1, 2])

with col1:
    st.subheader("Algèbre relationnelle")
    st.latex(r"\pi_{nom, prenom}(Etudiant)")

with col3:
    st.subheader("SQL")
    st.code(sql2, language="sql")

st.subheader("Résultat")
df2 = executer_requete(sql2)
if df2 is not None:
    st.dataframe(df2, width='stretch')

st.markdown("---")

# Requête 3 : Sélection (étudiants > 20 ans)
st.header("3. Sélection : étudiants de plus de 20 ans")

sql3 = "SELECT * FROM Etudiant WHERE age > 20;"

col1, _, col3 = st.columns([1, 1, 2])

with col1:
    st.subheader("Algèbre relationnelle")
    st.latex(r"\sigma_{age > 20}(Etudiant)")

with col3:
    st.subheader("SQL")
    st.code(sql3, language="sql")

st.subheader("Résultat")
df3 = executer_requete(sql3)
if df3 is not None:
    st.dataframe(df3, width='stretch')

st.markdown("---")

# Requête 4 : Combinaison sélection + projection
st.header("4. Sélection + Projection : noms des étudiants > 20 ans")

sql4 = "SELECT nom FROM Etudiant WHERE age > 20;"

col1, _, col3 = st.columns([1, 1, 2])

with col1:
    st.subheader("Algèbre relationnelle")
    st.latex(r"\pi_{nom}(\sigma_{age > 20}(Etudiant))")

with col3:
    st.subheader("SQL")
    st.code(sql4, language="sql")

st.subheader("Résultat")
df4 = executer_requete(sql4)
if df4 is not None:
    st.dataframe(df4, width='stretch')
