"""
Application principale - Définition de la navigation
"""

import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="IN207 - Bases de Données",
    page_icon="🗄️",
    layout="wide"
)

# Configuration de la navigation
pg = st.navigation([
    st.Page("pages/1_Accueil.py", title="Accueil", default=True),
    st.Page("pages/2_MCD.py", title="MCD"),
    st.Page("pages/3_MLD.py", title="MLD"),
    st.Page("pages/4_DDL.py", title="DDL"),
    st.Page("pages/5_Requetes.py", title="Requêtes"),
    st.Page("pages/6_Location.py", title="Location"),
    st.Page("pages/7_Facturation.py", title="Facturation")
])

pg.run()
