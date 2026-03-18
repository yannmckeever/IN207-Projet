"""
Page 6 - Processus d'enregistrement des Locations
Agence de location de voitures
"""

import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Configuration ────────────────────────────────────────────────────────────
DB_PATH = os.path.join(PROJECT_ROOT, "database.db")

st.title("📅 Gestion des Locations")
st.markdown("---")

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_conn():
    return sqlite3.connect(DB_PATH)


def run_query(sql, params=()):
    conn = get_conn()
    try:
        df = pd.read_sql_query(sql, conn, params=params)
        return df
    except Exception as e:
        st.error(f"Erreur SQL : {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def run_write(sql, params=()):
    conn = get_conn()
    try:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError as e:
        st.error(f"Erreur d'intégrité : {e}")
        return None
    except Exception as e:
        st.error(f"Erreur : {e}")
        return None
    finally:
        conn.close()


def calcul_montant(prix_voiture, prix_option, date_debut, date_fin):
    nb_jours = (date_fin - date_debut).days
    if nb_jours <= 0:
        return 0.0
    return round((prix_voiture + prix_option) * nb_jours, 2)


# ── Garde : base inexistante ──────────────────────────────────────────────────
if not os.path.exists(DB_PATH):
    st.warning("⚠️ La base de données n'existe pas. Créez-la d'abord dans la page **DDL**.")
    st.stop()


# ── Migration : s'assure que les colonnes nécessaires existent ────────────────
def ensure_schema():
    conn = get_conn()
    try:
        cols = [row[1] for row in conn.execute("PRAGMA table_info(Location)").fetchall()]
        if "id_option" not in cols:
            conn.execute("ALTER TABLE Location ADD COLUMN id_option INTEGER REFERENCES Option(id_option)")
            conn.commit()
    finally:
        conn.close()

ensure_schema()

# ── Onglets ───────────────────────────────────────────────────────────────────
tab_loc, tab_clients, tab_voitures, tab_options = st.tabs([
    "📋 Locations", "👤 Clients (Utilisateurs)", "🚘 Voitures", "🔧 Options"
])

# ═══════════════════════════════════════════════════════════════════════════════
# ONGLET 1 — LOCATIONS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_loc:

    # ── Vue d'ensemble ────────────────────────────────────────────────────────
    st.subheader("📊 Vue d'ensemble des locations")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtre_statut = st.selectbox(
            "Filtrer par statut",
            ["Tous", "en_cours", "terminee", "annulee"],
            key="filtre_statut_loc"
        )
    with col_f2:
        filtre_client_search = st.text_input("Rechercher par nom client", key="search_client_loc")

    sql_loc = """
        SELECT l.id_location, u.nom || ' ' || u.prenom AS client,
               v.marque || ' ' || v.modele AS voiture,
               o.nom AS option,
               l.date_debut, l.date_fin, l.statut
        FROM Location l
        JOIN Utilisateurs u ON l.id_utilisateur = u.id_utilisateur
        JOIN Voitures v ON l.id_voiture = v.id_voiture
        LEFT JOIN Option o ON l.id_option = o.id_option
    """
    conditions = []
    params_loc = []
    if filtre_statut != "Tous":
        conditions.append("l.statut = ?")
        params_loc.append(filtre_statut)
    if filtre_client_search:
        conditions.append("(u.nom LIKE ? OR u.prenom LIKE ?)")
        params_loc.extend([f"%{filtre_client_search}%", f"%{filtre_client_search}%"])
    if conditions:
        sql_loc += " WHERE " + " AND ".join(conditions)
    sql_loc += " ORDER BY l.date_debut DESC"

    df_loc = run_query(sql_loc, tuple(params_loc))
    st.dataframe(df_loc, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Créer une location ────────────────────────────────────────────────────
    with st.expander("➕ Créer une nouvelle location", expanded=False):
        df_users = run_query("SELECT id_utilisateur, nom || ' ' || prenom AS label FROM Utilisateurs ORDER BY nom")
        df_cars = run_query("""
            SELECT v.id_voiture,
                   v.marque || ' ' || v.modele || ' (' || a.ville || ') — ' || v.prix_journalier || '€/j' AS label,
                   v.prix_journalier
            FROM Voitures v JOIN Agences a ON v.id_agence = a.id_agence
            ORDER BY v.marque
        """)
        df_opts = run_query("SELECT id_option, nom || ' — ' || prix_journalier || '€/j' AS label, prix_journalier FROM Option ORDER BY nom")

        if df_users.empty or df_cars.empty:
            st.warning("Vous devez avoir au moins un client et une voiture pour créer une location.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                client_labels = df_users["label"].tolist()
                client_ids = df_users["id_utilisateur"].tolist()
                sel_client = st.selectbox("Client *", client_labels, key="new_loc_client")
                id_client = client_ids[client_labels.index(sel_client)]

                car_labels = df_cars["label"].tolist()
                car_ids = df_cars["id_voiture"].tolist()
                car_prices = df_cars["prix_journalier"].tolist()
                sel_car = st.selectbox("Voiture *", car_labels, key="new_loc_car")
                idx_car = car_labels.index(sel_car)
                id_voiture = car_ids[idx_car]
                prix_voiture = car_prices[idx_car]

            with c2:
                opt_labels = ["Aucune"] + df_opts["label"].tolist()
                opt_ids = [None] + df_opts["id_option"].tolist()
                opt_prices = [0.0] + df_opts["prix_journalier"].tolist()
                sel_opt = st.selectbox("Option", opt_labels, key="new_loc_opt")
                idx_opt = opt_labels.index(sel_opt)
                id_option = opt_ids[idx_opt]
                prix_option = opt_prices[idx_opt]

                today = date.today()
                date_debut = st.date_input("Date de début *", value=today, key="new_loc_dd")
                date_fin = st.date_input("Date de fin *", value=today + timedelta(days=3), key="new_loc_df")

            montant_estime = calcul_montant(prix_voiture, prix_option, date_debut, date_fin)
            st.info(f"💰 Montant estimé : **{montant_estime} €** "
                    f"({(date_fin - date_debut).days} jour(s) × {prix_voiture + prix_option:.2f} €/j)")

            if st.button("✅ Créer la location", key="btn_create_loc"):
                if date_fin <= date_debut:
                    st.error("La date de fin doit être après la date de début.")
                else:
                    lid = run_write(
                        "INSERT INTO Location (id_utilisateur, id_voiture, id_option, date_debut, date_fin, statut) "
                        "VALUES (?, ?, ?, ?, ?, 'en_cours')",
                        (id_client, id_voiture, id_option,
                         date_debut.isoformat(), date_fin.isoformat())
                    )
                    if lid:
                        # Créer automatiquement la facture associée
                        run_write(
                            "INSERT INTO Facture (id_location, montant, date_facture, statut_paiement) "
                            "VALUES (?, ?, ?, 'en_attente')",
                            (lid, montant_estime, date_fin.isoformat())
                        )
                        st.success(f"✅ Location #{lid} créée avec succès ! (Facture générée automatiquement)")
                        st.rerun()

    st.markdown("---")

    # ── Modifier le statut d'une location ────────────────────────────────────
    with st.expander("✏️ Modifier le statut d'une location", expanded=False):
        df_loc_ids = run_query("""
            SELECT l.id_location,
                   '#' || l.id_location || ' — ' || u.nom || ' ' || u.prenom || ' — ' || v.marque || ' ' || v.modele AS label,
                   l.statut
            FROM Location l
            JOIN Utilisateurs u ON l.id_utilisateur = u.id_utilisateur
            JOIN Voitures v ON l.id_voiture = v.id_voiture
            ORDER BY l.id_location DESC
        """)
        if not df_loc_ids.empty:
            loc_labels = df_loc_ids["label"].tolist()
            loc_ids = df_loc_ids["id_location"].tolist()
            loc_statuts = df_loc_ids["statut"].tolist()
            sel_loc_mod = st.selectbox("Location à modifier", loc_labels, key="mod_loc_sel")
            idx_mod = loc_labels.index(sel_loc_mod)
            statut_options = ["en_cours", "terminee", "annulee"]
            cur_statut = loc_statuts[idx_mod]
            new_statut = st.selectbox(
                "Nouveau statut",
                statut_options,
                index=statut_options.index(cur_statut) if cur_statut in statut_options else 0,
                key="mod_loc_statut"
            )
            if st.button("💾 Mettre à jour le statut", key="btn_upd_statut"):
                run_write("UPDATE Location SET statut = ? WHERE id_location = ?",
                          (new_statut, loc_ids[idx_mod]))
                st.success("Statut mis à jour !")
                st.rerun()

    st.markdown("---")

    # ── Supprimer une location ────────────────────────────────────────────────
    with st.expander("🗑️ Supprimer une location", expanded=False):
        st.warning("Cette action supprime également la facture associée.")
        df_loc_del = run_query("""
            SELECT l.id_location,
                   '#' || l.id_location || ' — ' || u.nom || ' ' || u.prenom || ' (' || l.statut || ')' AS label
            FROM Location l
            JOIN Utilisateurs u ON l.id_utilisateur = u.id_utilisateur
            ORDER BY l.id_location DESC
        """)
        if not df_loc_del.empty:
            del_labels = df_loc_del["label"].tolist()
            del_ids = df_loc_del["id_location"].tolist()
            sel_del = st.selectbox("Location à supprimer", del_labels, key="del_loc_sel")
            confirm_del = st.checkbox("Je confirme la suppression", key="confirm_del_loc")
            if st.button("🗑️ Supprimer", key="btn_del_loc", type="primary"):
                if confirm_del:
                    id_to_del = del_ids[del_labels.index(sel_del)]
                    run_write("DELETE FROM Facture WHERE id_location = ?", (id_to_del,))
                    run_write("DELETE FROM Location WHERE id_location = ?", (id_to_del,))
                    st.success("Location supprimée.")
                    st.rerun()
                else:
                    st.error("Veuillez cocher la case de confirmation.")

# ═══════════════════════════════════════════════════════════════════════════════
# ONGLET 2 — CLIENTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_clients:
    st.subheader("👤 Clients enregistrés")
    df_clients = run_query("SELECT * FROM Utilisateurs ORDER BY nom, prenom")
    st.dataframe(df_clients, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Ajouter un client ─────────────────────────────────────────────────────
    with st.expander("➕ Ajouter un client", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            nom_c = st.text_input("Nom *", key="add_cli_nom")
            prenom_c = st.text_input("Prénom *", key="add_cli_prenom")
            email_c = st.text_input("Email *", key="add_cli_email")
        with c2:
            tel_c = st.text_input("Téléphone", key="add_cli_tel")
            ddn_c = st.date_input("Date de naissance", value=date(1990, 1, 1),min_value=date(1900, 1, 1),max_value=date.today(), key="add_cli_ddn")
        if st.button("✅ Ajouter le client", key="btn_add_cli"):
            if not nom_c or not prenom_c or not email_c:
                st.error("Nom, prénom et email sont obligatoires.")
            else:
                uid = run_write(
                    "INSERT INTO Utilisateurs (nom, prenom, email, telephone, date_naissance) VALUES (?,?,?,?,?)",
                    (nom_c.strip(), prenom_c.strip(), email_c.strip(),
                     tel_c.strip() or None, ddn_c.isoformat())
                )
                if uid:
                    st.success(f"✅ Client #{uid} ajouté !")
                    st.rerun()

    st.markdown("---")

    # ── Modifier un client ────────────────────────────────────────────────────
    with st.expander("✏️ Modifier un client", expanded=False):
        df_cli_sel = run_query("SELECT id_utilisateur, nom || ' ' || prenom AS label FROM Utilisateurs ORDER BY nom")
        if not df_cli_sel.empty:
            cli_labels = df_cli_sel["label"].tolist()
            cli_ids = df_cli_sel["id_utilisateur"].tolist()
            sel_cli = st.selectbox("Client à modifier", cli_labels, key="mod_cli_sel")
            id_cli_mod = cli_ids[cli_labels.index(sel_cli)]
            row = run_query("SELECT * FROM Utilisateurs WHERE id_utilisateur = ?", (id_cli_mod,))
            if not row.empty:
                r = row.iloc[0]
                c1, c2 = st.columns(2)
                with c1:
                    new_nom = st.text_input("Nom", value=r["nom"], key="mod_cli_nom")
                    new_prenom = st.text_input("Prénom", value=r["prenom"], key="mod_cli_prenom")
                    new_email = st.text_input("Email", value=r["email"], key="mod_cli_email")
                with c2:
                    new_tel = st.text_input("Téléphone", value=r["telephone"] or "", key="mod_cli_tel")
                    try:
                        ddn_val = date.fromisoformat(r["date_naissance"]) if r["date_naissance"] else date(1990, 1, 1)
                    except Exception:
                        ddn_val = date(1990, 1, 1)
                    new_ddn = st.date_input("Date de naissance", value=ddn_val, key="mod_cli_ddn")
                if st.button("💾 Enregistrer les modifications", key="btn_mod_cli"):
                    run_write(
                        "UPDATE Utilisateurs SET nom=?, prenom=?, email=?, telephone=?, date_naissance=? "
                        "WHERE id_utilisateur=?",
                        (new_nom, new_prenom, new_email, new_tel or None, new_ddn.isoformat(), id_cli_mod)
                    )
                    st.success("Client mis à jour !")
                    st.rerun()

    st.markdown("---")

    # ── Supprimer un client ───────────────────────────────────────────────────
    with st.expander("🗑️ Supprimer un client", expanded=False):
        st.warning("Impossible de supprimer un client ayant des locations associées.")
        df_cli_del = run_query("SELECT id_utilisateur, nom || ' ' || prenom AS label FROM Utilisateurs ORDER BY nom")
        if not df_cli_del.empty:
            del_cli_labels = df_cli_del["label"].tolist()
            del_cli_ids = df_cli_del["id_utilisateur"].tolist()
            sel_del_cli = st.selectbox("Client à supprimer", del_cli_labels, key="del_cli_sel")
            confirm_del_cli = st.checkbox("Je confirme la suppression", key="confirm_del_cli")
            if st.button("🗑️ Supprimer", key="btn_del_cli", type="primary"):
                if confirm_del_cli:
                    id_del_cli = del_cli_ids[del_cli_labels.index(sel_del_cli)]
                    run_write("DELETE FROM Utilisateurs WHERE id_utilisateur = ?", (id_del_cli,))
                    st.success("Client supprimé.")
                    st.rerun()
                else:
                    st.error("Veuillez cocher la case de confirmation.")

# ═══════════════════════════════════════════════════════════════════════════════
# ONGLET 3 — VOITURES
# ═══════════════════════════════════════════════════════════════════════════════
with tab_voitures:
    st.subheader("🚘 Flotte de véhicules")
    df_voit = run_query("""
        SELECT v.id_voiture, v.marque, v.modele, v.annee, v.categorie,
               v.prix_journalier, a.nom AS agence, a.ville
        FROM Voitures v JOIN Agences a ON v.id_agence = a.id_agence
        ORDER BY v.marque, v.modele
    """)
    st.dataframe(df_voit, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Ajouter une voiture ────────────────────────────────────────────────────
    with st.expander("➕ Ajouter une voiture", expanded=False):
        df_agences = run_query("SELECT id_agence, nom || ' (' || ville || ')' AS label FROM Agences ORDER BY nom")
        if df_agences.empty:
            st.warning("Aucune agence disponible.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                marque_v = st.text_input("Marque *", key="add_voit_marque")
                modele_v = st.text_input("Modèle *", key="add_voit_modele")
                annee_v = st.number_input("Année", min_value=2000, max_value=2030,
                                          value=date.today().year, step=1, key="add_voit_annee")
            with c2:
                categories = ["Citadine", "Berline", "SUV", "Utilitaire", "Coupé", "Cabriolet"]
                cat_v = st.selectbox("Catégorie *", categories, key="add_voit_cat")
                prix_v = st.number_input("Prix journalier (€) *", min_value=0.0,
                                         value=50.0, step=5.0, key="add_voit_prix")
                ag_labels = df_agences["label"].tolist()
                ag_ids = df_agences["id_agence"].tolist()
                sel_ag = st.selectbox("Agence *", ag_labels, key="add_voit_ag")
                id_ag = ag_ids[ag_labels.index(sel_ag)]
            if st.button("✅ Ajouter la voiture", key="btn_add_voit"):
                if not marque_v or not modele_v:
                    st.error("Marque et modèle sont obligatoires.")
                else:
                    vid = run_write(
                        "INSERT INTO Voitures (marque, modele, annee, categorie, prix_journalier, id_agence) VALUES (?,?,?,?,?,?)",
                        (marque_v.strip(), modele_v.strip(), int(annee_v), cat_v, float(prix_v), id_ag)
                    )
                    if vid:
                        st.success(f"✅ Voiture #{vid} ajoutée !")
                        st.rerun()

    st.markdown("---")

    # ── Modifier une voiture ──────────────────────────────────────────────────
    with st.expander("✏️ Modifier une voiture", expanded=False):
        df_voit_sel = run_query("""
            SELECT v.id_voiture, v.marque || ' ' || v.modele || ' (' || a.ville || ')' AS label
            FROM Voitures v JOIN Agences a ON v.id_agence = a.id_agence ORDER BY v.marque
        """)
        if not df_voit_sel.empty:
            voit_labels = df_voit_sel["label"].tolist()
            voit_ids = df_voit_sel["id_voiture"].tolist()
            sel_voit = st.selectbox("Voiture à modifier", voit_labels, key="mod_voit_sel")
            id_voit_mod = voit_ids[voit_labels.index(sel_voit)]
            row_v = run_query("SELECT * FROM Voitures WHERE id_voiture = ?", (id_voit_mod,))
            if not row_v.empty:
                rv = row_v.iloc[0]
                df_agences2 = run_query("SELECT id_agence, nom || ' (' || ville || ')' AS label FROM Agences ORDER BY nom")
                c1, c2 = st.columns(2)
                with c1:
                    new_marque = st.text_input("Marque", value=rv["marque"], key="mod_voit_marque")
                    new_modele = st.text_input("Modèle", value=rv["modele"], key="mod_voit_modele")
                    new_annee = st.number_input("Année", min_value=2000, max_value=2030,
                                                value=int(rv["annee"]) if rv["annee"] else 2020,
                                                step=1, key="mod_voit_annee")
                with c2:
                    cats = ["Citadine", "Berline", "SUV", "Utilitaire", "Coupé", "Cabriolet"]
                    cur_cat = rv["categorie"] if rv["categorie"] in cats else cats[0]
                    new_cat = st.selectbox("Catégorie", cats, index=cats.index(cur_cat), key="mod_voit_cat")
                    new_prix = st.number_input("Prix journalier (€)", min_value=0.0,
                                               value=float(rv["prix_journalier"]), step=5.0, key="mod_voit_prix")
                    ag2_labels = df_agences2["label"].tolist()
                    ag2_ids = df_agences2["id_agence"].tolist()
                    cur_ag_idx = ag2_ids.index(rv["id_agence"]) if rv["id_agence"] in ag2_ids else 0
                    sel_ag2 = st.selectbox("Agence", ag2_labels, index=cur_ag_idx, key="mod_voit_ag")
                    id_ag2 = ag2_ids[ag2_labels.index(sel_ag2)]
                if st.button("💾 Enregistrer", key="btn_mod_voit"):
                    run_write(
                        "UPDATE Voitures SET marque=?, modele=?, annee=?, categorie=?, prix_journalier=?, id_agence=? "
                        "WHERE id_voiture=?",
                        (new_marque, new_modele, int(new_annee), new_cat, float(new_prix), id_ag2, id_voit_mod)
                    )
                    st.success("Voiture mise à jour !")
                    st.rerun()

    st.markdown("---")

    # ── Supprimer une voiture ─────────────────────────────────────────────────
    with st.expander("🗑️ Supprimer une voiture", expanded=False):
        st.warning("Impossible de supprimer une voiture ayant des locations associées.")
        df_voit_del = run_query("""
            SELECT v.id_voiture, v.marque || ' ' || v.modele AS label
            FROM Voitures v ORDER BY v.marque
        """)
        if not df_voit_del.empty:
            del_voit_labels = df_voit_del["label"].tolist()
            del_voit_ids = df_voit_del["id_voiture"].tolist()
            sel_del_v = st.selectbox("Voiture à supprimer", del_voit_labels, key="del_voit_sel")
            confirm_del_v = st.checkbox("Je confirme la suppression", key="confirm_del_voit")
            if st.button("🗑️ Supprimer", key="btn_del_voit", type="primary"):
                if confirm_del_v:
                    id_del_v = del_voit_ids[del_voit_labels.index(sel_del_v)]
                    run_write("DELETE FROM Voitures WHERE id_voiture = ?", (id_del_v,))
                    st.success("Voiture supprimée.")
                    st.rerun()
                else:
                    st.error("Veuillez cocher la case de confirmation.")

# ═══════════════════════════════════════════════════════════════════════════════
# ONGLET 4 — OPTIONS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_options:
    st.subheader("🔧 Options disponibles")
    df_opts_view = run_query("SELECT * FROM Option ORDER BY nom")
    st.dataframe(df_opts_view, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Ajouter une option ─────────────────────────────────────────────────────
    with st.expander("➕ Ajouter une option", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            nom_o = st.text_input("Nom *", key="add_opt_nom")
            desc_o = st.text_area("Description", key="add_opt_desc", height=80)
        with c2:
            prix_o = st.number_input("Prix journalier (€) *", min_value=0.0,
                                     value=5.0, step=1.0, key="add_opt_prix")
        if st.button("✅ Ajouter l'option", key="btn_add_opt"):
            if not nom_o:
                st.error("Le nom est obligatoire.")
            else:
                oid = run_write(
                    "INSERT INTO Option (nom, description, prix_journalier) VALUES (?,?,?)",
                    (nom_o.strip(), desc_o.strip() or None, float(prix_o))
                )
                if oid:
                    st.success(f"✅ Option #{oid} ajoutée !")
                    st.rerun()

    st.markdown("---")

    # ── Modifier une option ────────────────────────────────────────────────────
    with st.expander("✏️ Modifier une option", expanded=False):
        df_opt_sel = run_query("SELECT id_option, nom AS label FROM Option ORDER BY nom")
        if not df_opt_sel.empty:
            opt_mod_labels = df_opt_sel["label"].tolist()
            opt_mod_ids = df_opt_sel["id_option"].tolist()
            sel_opt_mod = st.selectbox("Option à modifier", opt_mod_labels, key="mod_opt_sel")
            id_opt_mod = opt_mod_ids[opt_mod_labels.index(sel_opt_mod)]
            row_o = run_query("SELECT * FROM Option WHERE id_option = ?", (id_opt_mod,))
            if not row_o.empty:
                ro = row_o.iloc[0]
                c1, c2 = st.columns(2)
                with c1:
                    new_nom_o = st.text_input("Nom", value=ro["nom"], key="mod_opt_nom")
                    new_desc_o = st.text_area("Description", value=ro["description"] or "", key="mod_opt_desc", height=80)
                with c2:
                    new_prix_o = st.number_input("Prix journalier (€)", min_value=0.0,
                                                 value=float(ro["prix_journalier"]), step=1.0, key="mod_opt_prix")
                if st.button("💾 Enregistrer", key="btn_mod_opt"):
                    run_write(
                        "UPDATE Option SET nom=?, description=?, prix_journalier=? WHERE id_option=?",
                        (new_nom_o, new_desc_o or None, float(new_prix_o), id_opt_mod)
                    )
                    st.success("Option mise à jour !")
                    st.rerun()

    st.markdown("---")

    # ── Supprimer une option ───────────────────────────────────────────────────
    with st.expander("🗑️ Supprimer une option", expanded=False):
        df_opt_del = run_query("SELECT id_option, nom AS label FROM Option ORDER BY nom")
        if not df_opt_del.empty:
            del_opt_labels = df_opt_del["label"].tolist()
            del_opt_ids = df_opt_del["id_option"].tolist()
            sel_del_o = st.selectbox("Option à supprimer", del_opt_labels, key="del_opt_sel")
            confirm_del_o = st.checkbox("Je confirme la suppression", key="confirm_del_opt")
            if st.button("🗑️ Supprimer", key="btn_del_opt", type="primary"):
                if confirm_del_o:
                    id_del_o = del_opt_ids[del_opt_labels.index(sel_del_o)]
                    run_write("DELETE FROM Option WHERE id_option = ?", (id_del_o,))
                    st.success("Option supprimée.")
                    st.rerun()
                else:
                    st.error("Veuillez cocher la case de confirmation.")

