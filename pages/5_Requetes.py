"""
Page 5 - Requêtes SQL
10 requêtes algèbre → SQL + 10 requêtes avec agrégation
"""

import streamlit as st
import sqlite3
import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

st.title("Requêtes SQL")

st.markdown("---")

DB_PATH = os.path.join(PROJECT_ROOT, "database.db")


def executer_requete(sql):
    """Exécute une requête SQL et retourne un DataFrame."""
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


def afficher_requete_relationnelle(algebre, sql):
    st.markdown("**Algèbre relationnelle :**")
    st.latex(algebre)
    st.markdown("**SQL :**")
    st.code(sql, language="sql")


if not os.path.exists(DB_PATH):
    st.warning("La base de données n'existe pas. Veuillez d'abord la créer dans la page **DDL**.")
    st.stop()

st.header("Liste des requêtes")

st.markdown("Requêtes SQL (algèbre relationnelle + agrégations).")

st.markdown("---")

# ---- Requête 1 ----
st.subheader("Requête 1 — Sélection : Locations actuellement en cours")

sql1 = "SELECT * FROM Location WHERE statut = 'en_cours';"
afficher_requete_relationnelle(
    r"\sigma_{statut = 'en\_cours'}(Location)",
    sql1,
)

df = executer_requete(sql1)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 2 ----
st.subheader("Requête 2 — Projection : Couples (ville, catégorie) de l'offre")

sql2 = """SELECT DISTINCT A.ville, V.categorie
FROM Voitures V
JOIN Agences A ON V.id_agence = A.id_agence;"""
afficher_requete_relationnelle(
    r"\pi_{ville,\ categorie}(Agences \bowtie_{id\_agence} Voitures)",
    sql2,
)

df = executer_requete(sql2)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 3 ----
st.subheader("Requête 3 — Sélection + Projection : Utilitaires économiques (< 60€/jour)")

sql3 = """SELECT marque, modele, prix_journalier
FROM Voitures
WHERE categorie = 'Utilitaire' AND prix_journalier < 60;"""
afficher_requete_relationnelle(
    r"\pi_{marque,\ modele,\ prix\_journalier}(\sigma_{categorie = 'Utilitaire' \land prix\_journalier < 60}(Voitures))",
    sql3,
)

df = executer_requete(sql3)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 4 ----
st.subheader("Requête 4 — Jointure : Détail des locations terminées (client + véhicule)")

sql4 = """SELECT L.id_location, U.nom, U.prenom, V.marque, V.modele, L.date_debut, L.date_fin
FROM Location L
JOIN Utilisateurs U ON L.id_utilisateur = U.id_utilisateur
JOIN Voitures V ON L.id_voiture = V.id_voiture
WHERE L.statut = 'terminee';"""
afficher_requete_relationnelle(
    r"\pi_{id\_location,\ nom,\ prenom,\ marque,\ modele,\ date\_debut,\ date\_fin}(\sigma_{statut='terminee'}(Location) \bowtie_{id\_utilisateur} Utilisateurs \bowtie_{id\_voiture} Voitures)",
    sql4,
)

df = executer_requete(sql4)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 5 ----
st.subheader("Requête 5 — Jointure : Factures en attente (suivi recouvrement)")

sql5 = """SELECT F.id_facture, F.montant, U.nom, U.prenom, A.nom AS agence
FROM Facture F
JOIN Location L ON F.id_location = L.id_location
JOIN Utilisateurs U ON L.id_utilisateur = U.id_utilisateur
JOIN Voitures V ON L.id_voiture = V.id_voiture
JOIN Agences A ON V.id_agence = A.id_agence
WHERE F.statut_paiement = 'en_attente';"""
afficher_requete_relationnelle(
    r"\pi_{id\_facture,\ montant,\ nom,\ prenom,\ agence}(\sigma_{statut\_paiement='en\_attente'}(Facture) \bowtie_{id\_location} Location \bowtie_{id\_utilisateur} Utilisateurs \bowtie_{id\_voiture} Voitures \bowtie_{id\_agence} Agences)",
    sql5,
)

df = executer_requete(sql5)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 6 ----
st.subheader("Requête 6 — Jointure + Sélection : Avis critiques (note ≤ 3) par ville")

sql6 = """SELECT U.nom, U.prenom, V.marque, V.modele, Av.note, Av.commentaire, Ag.ville
FROM Avis Av
JOIN Utilisateurs U ON Av.id_utilisateur = U.id_utilisateur
JOIN Voitures V ON Av.id_voiture = V.id_voiture
JOIN Agences Ag ON V.id_agence = Ag.id_agence
WHERE Av.note <= 3;"""
afficher_requete_relationnelle(
    r"\pi_{nom,\ prenom,\ marque,\ modele,\ note,\ commentaire,\ ville}(\sigma_{note \leq 3}(Avis \bowtie_{id\_utilisateur} Utilisateurs \bowtie_{id\_voiture} Voitures \bowtie_{id\_agence} Agences))",
    sql6,
)

df = executer_requete(sql6)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 7 ----
st.subheader("Requête 7 — Jointures multiples : Locations avec options choisies")

sql7 = """SELECT L.id_location, U.nom, U.prenom, V.marque, V.modele, O.nom AS option_choisie
FROM Location L
JOIN Utilisateurs U ON L.id_utilisateur = U.id_utilisateur
JOIN Voitures V ON L.id_voiture = V.id_voiture
JOIN Option O ON L.id_option = O.id_option
WHERE L.id_option IS NOT NULL;"""
afficher_requete_relationnelle(
    r"\pi_{id\_location,\ nom,\ prenom,\ marque,\ modele,\ option}(\sigma_{id\_option\neq NULL}(Location) \bowtie_{id\_utilisateur} Utilisateurs \bowtie_{id\_voiture} Voitures \bowtie_{id\_option} Option)",
    sql7,
)

df = executer_requete(sql7)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 8 ----
st.subheader("Requête 8 — Jointure : Détail des locations annulées")

sql8 = """SELECT L.id_location, U.nom, U.prenom, V.marque, V.modele, L.date_debut, L.date_fin
FROM Location L
JOIN Utilisateurs U ON L.id_utilisateur = U.id_utilisateur
JOIN Voitures V ON L.id_voiture = V.id_voiture
WHERE L.statut = 'annulee';"""
afficher_requete_relationnelle(
    r"\pi_{id\_location,\ nom,\ prenom,\ marque,\ modele,\ date\_debut,\ date\_fin}(\sigma_{statut='annulee'}(Location) \bowtie_{id\_utilisateur} Utilisateurs \bowtie_{id\_voiture} Voitures)",
    sql8,
)

df = executer_requete(sql8)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 9 — DIVISION ----
st.subheader("Requête 9 — ÷ Division : Utilisateurs ayant loué dans TOUTES les agences")

sql9 = """SELECT U.nom, U.prenom
FROM Utilisateurs U
WHERE NOT EXISTS (
    SELECT A.id_agence FROM Agences A
    WHERE NOT EXISTS (
        SELECT 1 FROM Location L
        JOIN Voitures V ON L.id_voiture = V.id_voiture
        WHERE L.id_utilisateur = U.id_utilisateur
        AND V.id_agence = A.id_agence
    )
);"""
afficher_requete_relationnelle(
    r"\pi_{id\_utilisateur,\ id\_agence}(Location \bowtie_{id\_voiture} Voitures) \div \pi_{id\_agence}(Agences)",
    sql9,
)

st.info("La division en SQL se traduit par un double `NOT EXISTS`.")
df = executer_requete(sql9)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 10 — DIVISION ----
st.subheader("Requête 10 — ÷ Division : Utilisateurs ayant loué TOUTES les catégories")

sql10 = """SELECT U.nom, U.prenom
FROM Utilisateurs U
WHERE NOT EXISTS (
    SELECT DISTINCT V.categorie FROM Voitures V
    WHERE NOT EXISTS (
        SELECT 1
        FROM Location L
        JOIN Voitures V2 ON L.id_voiture = V2.id_voiture
        WHERE L.id_utilisateur = U.id_utilisateur
        AND V2.categorie = V.categorie
    )
);"""
afficher_requete_relationnelle(
    r"\pi_{id\_utilisateur,\ categorie}(Location \bowtie_{id\_voiture} Voitures) \div \pi_{categorie}(Voitures)",
    sql10,
)

st.info("Cette division met en évidence les clients polyvalents ayant déjà loué chaque catégorie disponible.")
df = executer_requete(sql10)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 11 ----
st.subheader("Requête 11 — COUNT : Nombre de locations par utilisateur")

sql11 = """SELECT U.nom, U.prenom, COUNT(*) AS nb_locations
FROM Location L
JOIN Utilisateurs U ON L.id_utilisateur = U.id_utilisateur
GROUP BY U.id_utilisateur;"""

st.code(sql11, language="sql")
df = executer_requete(sql11)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 12 ----
st.subheader("Requête 12 — AVG : Note moyenne par voiture")

sql12 = """SELECT V.marque, V.modele, ROUND(AVG(A.note), 2) AS note_moyenne
FROM Avis A
JOIN Voitures V ON A.id_voiture = V.id_voiture
GROUP BY V.id_voiture;"""

st.code(sql12, language="sql")
df = executer_requete(sql12)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 13 ----
st.subheader("Requête 13 — SUM : Chiffre d'affaires par agence")

sql13 = """SELECT Ag.nom AS agence, SUM(F.montant) AS chiffre_affaires
FROM Facture F
JOIN Location L ON F.id_location = L.id_location
JOIN Voitures V ON L.id_voiture = V.id_voiture
JOIN Agences Ag ON V.id_agence = Ag.id_agence
WHERE F.statut_paiement = 'payee'
GROUP BY Ag.id_agence;"""

st.code(sql13, language="sql")
df = executer_requete(sql13)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 14 ----
st.subheader("Requête 14 — MIN / MAX : Prix par catégorie")

sql14 = """SELECT categorie,
       MIN(prix_journalier) AS prix_min,
       MAX(prix_journalier) AS prix_max
FROM Voitures
GROUP BY categorie;"""

st.code(sql14, language="sql")
df = executer_requete(sql14)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 15 ----
st.subheader("Requête 15 — COUNT + HAVING : Utilisateurs avec plus de 3 locations")

sql15 = """SELECT U.nom, U.prenom, COUNT(*) AS nb_locations
FROM Location L
JOIN Utilisateurs U ON L.id_utilisateur = U.id_utilisateur
GROUP BY U.id_utilisateur
HAVING COUNT(*) > 3;"""

st.code(sql15, language="sql")
df = executer_requete(sql15)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 16 ----
st.subheader("Requête 16 — AVG + HAVING : Voitures avec note moyenne ≥ 4")

sql16 = """SELECT V.marque, V.modele, ROUND(AVG(A.note), 2) AS note_moyenne
FROM Avis A
JOIN Voitures V ON A.id_voiture = V.id_voiture
GROUP BY V.id_voiture
HAVING AVG(A.note) >= 4;"""

st.code(sql16, language="sql")
df = executer_requete(sql16)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---- Requête 17 ----
st.subheader("Requête 17 — COUNT : Nombre de voitures disponibles par agence et catégorie")

sql17 = """SELECT Ag.nom AS agence, V.categorie, COUNT(*) AS nb_voitures
FROM Voitures V
JOIN Agences Ag ON V.id_agence = Ag.id_agence
LEFT JOIN Location L ON L.id_voiture = V.id_voiture AND L.statut = 'en_cours'
WHERE L.id_location IS NULL
GROUP BY Ag.id_agence, V.categorie
ORDER BY Ag.nom, V.categorie;"""

st.code(sql17, language="sql")
df = executer_requete(sql17)
if df is not None:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

st.success("17 requêtes SQL au total : 10 traduites de l'algèbre relationnelle (dont 2 divisions ÷) + 7 avec agrégation (COUNT, SUM, AVG, MIN, MAX, GROUP BY, HAVING).")
