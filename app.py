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
    st.Page("pages/1_Accueil.py", title="Accueil", icon="🏠", default=True),
    st.Page("pages/2_MCD.py", title="MCD", icon="📊"),
    st.Page("pages/3_MLD.py", title="MLD", icon="📋"),
    st.Page("pages/4_DDL.py", title="DDL", icon="🔧"),
    st.Page("pages/5_Requetes.py", title="Requêtes", icon="🔍")
])

pg.run()
