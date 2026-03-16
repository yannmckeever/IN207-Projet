"""
Page 7 - Processus de Facturation
Agence de location de voitures
"""

import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Configuration ─────────────────────────────────────────────────────────────
DB_PATH = os.path.join(PROJECT_ROOT, "database.db")

st.title("💰 Gestion de la Facturation")
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


# ── Garde : base inexistante ──────────────────────────────────────────────────
if not os.path.exists(DB_PATH):
    st.warning("⚠️ La base de données n'existe pas. Créez-la d'abord dans la page **DDL**.")
    st.stop()

# ── Métriques globales ────────────────────────────────────────────────────────
df_stats = run_query("""
    SELECT
        COUNT(*) AS total_factures,
        COALESCE(SUM(montant), 0) AS chiffre_affaires,
        COALESCE(SUM(CASE WHEN statut_paiement = 'payee' THEN montant ELSE 0 END), 0) AS montant_encaisse,
        COALESCE(SUM(CASE WHEN statut_paiement = 'en_attente' THEN montant ELSE 0 END), 0) AS montant_en_attente,
        COUNT(CASE WHEN statut_paiement = 'payee' THEN 1 END) AS nb_payees,
        COUNT(CASE WHEN statut_paiement = 'en_attente' THEN 1 END) AS nb_en_attente
    FROM Facture
""")

if not df_stats.empty:
    s = df_stats.iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📄 Total factures", int(s["total_factures"]))
    col2.metric("💵 CA total", f"{s['chiffre_affaires']:.2f} €")
    col3.metric("✅ Encaissé", f"{s['montant_encaisse']:.2f} €", f"{int(s['nb_payees'])} facture(s)")
    col4.metric("⏳ En attente", f"{s['montant_en_attente']:.2f} €", f"{int(s['nb_en_attente'])} facture(s)")

st.markdown("---")

# ── Onglets ────────────────────────────────────────────────────────────────────
tab_list, tab_create, tab_avis = st.tabs([
    "📋 Liste des factures", "➕ Créer une facture", "⭐ Avis clients"
])

# ═══════════════════════════════════════════════════════════════════════════════
# ONGLET 1 — LISTE DES FACTURES
# ═══════════════════════════════════════════════════════════════════════════════
with tab_list:
    st.subheader("📋 Toutes les factures")

    # Filtres
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filtre_paiement = st.selectbox(
            "Statut de paiement",
            ["Tous", "payee", "en_attente"],
            key="filt_paiement"
        )
    with col_f2:
        filtre_client_f = st.text_input("Rechercher par client", key="filt_client_fact")
    with col_f3:
        tri = st.selectbox("Trier par", ["Date (récent)", "Date (ancien)", "Montant ↑", "Montant ↓"], key="tri_fact")

    sql_fact = """
        SELECT f.id_facture,
               u.nom || ' ' || u.prenom AS client,
               v.marque || ' ' || v.modele AS voiture,
               l.date_debut, l.date_fin,
               f.montant, f.date_facture, f.statut_paiement,
               l.id_location
        FROM Facture f
        JOIN Location l ON f.id_location = l.id_location
        JOIN Utilisateurs u ON l.id_utilisateur = u.id_utilisateur
        JOIN Voitures v ON l.id_voiture = v.id_voiture
    """
    conditions_f = []
    params_f = []
    if filtre_paiement != "Tous":
        conditions_f.append("f.statut_paiement = ?")
        params_f.append(filtre_paiement)
    if filtre_client_f:
        conditions_f.append("(u.nom LIKE ? OR u.prenom LIKE ?)")
        params_f.extend([f"%{filtre_client_f}%", f"%{filtre_client_f}%"])
    if conditions_f:
        sql_fact += " WHERE " + " AND ".join(conditions_f)

    order_map = {
        "Date (récent)": "f.date_facture DESC",
        "Date (ancien)": "f.date_facture ASC",
        "Montant ↑": "f.montant ASC",
        "Montant ↓": "f.montant DESC",
    }
    sql_fact += f" ORDER BY {order_map[tri]}"

    df_fact = run_query(sql_fact, tuple(params_f))

    # Coloration des lignes selon statut
    def colorize(val):
        if val == "payee":
            return "background-color: #d4edda; color: #155724"
        elif val == "en_attente":
            return "background-color: #fff3cd; color: #856404"
        return ""

    if not df_fact.empty:
        st.dataframe(
            df_fact.drop(columns=["id_location"]).style.applymap(
                colorize, subset=["statut_paiement"]
            ),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Aucune facture trouvée.")

    st.markdown("---")

    # ── Marquer une/plusieurs factures comme payée ────────────────────────────
    st.subheader("✅ Enregistrer un paiement")

    df_unpaid = run_query("""
        SELECT f.id_facture,
               '#' || f.id_facture || ' — ' || u.nom || ' ' || u.prenom ||
               ' — ' || v.marque || ' ' || v.modele ||
               ' — ' || f.montant || '€' AS label
        FROM Facture f
        JOIN Location l ON f.id_location = l.id_location
        JOIN Utilisateurs u ON l.id_utilisateur = u.id_utilisateur
        JOIN Voitures v ON l.id_voiture = v.id_voiture
        WHERE f.statut_paiement = 'en_attente'
        ORDER BY f.id_facture
    """)

    if df_unpaid.empty:
        st.success("✅ Toutes les factures sont payées !")
    else:
        pay_labels = df_unpaid["label"].tolist()
        pay_ids = df_unpaid["id_facture"].tolist()

        col_p1, col_p2 = st.columns([3, 1])
        with col_p1:
            sel_pay = st.selectbox("Facture à marquer comme payée", pay_labels, key="sel_pay_fact")
        with col_p2:
            date_paiement = st.date_input("Date de paiement", value=date.today(), key="date_paiement")

        if st.button("💳 Enregistrer le paiement", key="btn_pay_fact"):
            id_to_pay = pay_ids[pay_labels.index(sel_pay)]
            run_write(
                "UPDATE Facture SET statut_paiement = 'payee', date_facture = ? WHERE id_facture = ?",
                (date_paiement.isoformat(), id_to_pay)
            )
            st.success(f"✅ Facture #{id_to_pay} marquée comme payée !")
            st.rerun()

        # Paiement en masse
        with st.expander("💳 Marquer TOUTES les factures en attente comme payées", expanded=False):
            st.warning("Cette action marquera toutes les factures 'en_attente' comme payées.")
            date_masse = st.date_input("Date de paiement en masse", value=date.today(), key="date_paiement_masse")
            if st.button("✅ Tout payer", key="btn_pay_all", type="primary"):
                run_write(
                    "UPDATE Facture SET statut_paiement = 'payee', date_facture = ? WHERE statut_paiement = 'en_attente'",
                    (date_masse.isoformat(),)
                )
                st.success("Toutes les factures ont été marquées comme payées !")
                st.rerun()

    st.markdown("---")

    # ── Modifier le montant d'une facture ────────────────────────────────────
    with st.expander("✏️ Modifier une facture", expanded=False):
        df_fact_mod = run_query("""
            SELECT f.id_facture,
                   '#' || f.id_facture || ' — ' || u.nom || ' ' || u.prenom || ' (' || f.statut_paiement || ')' AS label,
                   f.montant, f.statut_paiement, f.date_facture
            FROM Facture f
            JOIN Location l ON f.id_location = l.id_location
            JOIN Utilisateurs u ON l.id_utilisateur = u.id_utilisateur
            ORDER BY f.id_facture DESC
        """)
        if not df_fact_mod.empty:
            mod_labels = df_fact_mod["label"].tolist()
            mod_ids = df_fact_mod["id_facture"].tolist()
            sel_mod_f = st.selectbox("Facture à modifier", mod_labels, key="mod_fact_sel")
            idx_mod_f = mod_labels.index(sel_mod_f)
            id_mod_f = mod_ids[idx_mod_f]
            row_f = df_fact_mod.iloc[idx_mod_f]

            c1, c2, c3 = st.columns(3)
            with c1:
                new_montant = st.number_input("Montant (€)", min_value=0.0,
                                              value=float(row_f["montant"]), step=10.0, key="mod_fact_montant")
            with c2:
                statuts_f = ["en_attente", "payee"]
                cur_s = row_f["statut_paiement"]
                new_statut_f = st.selectbox("Statut", statuts_f,
                                            index=statuts_f.index(cur_s) if cur_s in statuts_f else 0,
                                            key="mod_fact_statut")
            with c3:
                try:
                    cur_date_f = date.fromisoformat(row_f["date_facture"]) if row_f["date_facture"] else date.today()
                except Exception:
                    cur_date_f = date.today()
                new_date_f = st.date_input("Date facture", value=cur_date_f, key="mod_fact_date")

            if st.button("💾 Enregistrer", key="btn_mod_fact"):
                run_write(
                    "UPDATE Facture SET montant=?, statut_paiement=?, date_facture=? WHERE id_facture=?",
                    (float(new_montant), new_statut_f, new_date_f.isoformat(), id_mod_f)
                )
                st.success("Facture mise à jour !")
                st.rerun()

    st.markdown("---")

    # ── Supprimer une facture ────────────────────────────────────────────────
    with st.expander("🗑️ Supprimer une facture", expanded=False):
        df_fact_del = run_query("""
            SELECT f.id_facture,
                   '#' || f.id_facture || ' — ' || u.nom || ' ' || u.prenom || ' — ' || f.montant || '€' AS label
            FROM Facture f
            JOIN Location l ON f.id_location = l.id_location
            JOIN Utilisateurs u ON l.id_utilisateur = u.id_utilisateur
            ORDER BY f.id_facture DESC
        """)
        if not df_fact_del.empty:
            del_f_labels = df_fact_del["label"].tolist()
            del_f_ids = df_fact_del["id_facture"].tolist()
            sel_del_f = st.selectbox("Facture à supprimer", del_f_labels, key="del_fact_sel")
            confirm_del_f = st.checkbox("Je confirme la suppression", key="confirm_del_fact")
            if st.button("🗑️ Supprimer", key="btn_del_fact", type="primary"):
                if confirm_del_f:
                    id_del_f = del_f_ids[del_f_labels.index(sel_del_f)]
                    run_write("DELETE FROM Facture WHERE id_facture = ?", (id_del_f,))
                    st.success("Facture supprimée.")
                    st.rerun()
                else:
                    st.error("Veuillez cocher la case de confirmation.")

# ═══════════════════════════════════════════════════════════════════════════════
# ONGLET 2 — CRÉER UNE FACTURE MANUELLE
# ═══════════════════════════════════════════════════════════════════════════════
with tab_create:
    st.subheader("➕ Créer une facture manuellement")
    st.info("Les factures sont créées automatiquement lors d'une location. "
            "Utilisez cet onglet pour les locations sans facture.")

    # Locations sans facture
    df_loc_sans_fact = run_query("""
        SELECT l.id_location,
               '#' || l.id_location || ' — ' || u.nom || ' ' || u.prenom ||
               ' — ' || v.marque || ' ' || v.modele ||
               ' (' || l.date_debut || ' → ' || l.date_fin || ')' AS label,
               v.prix_journalier,
               COALESCE(o.prix_journalier, 0) AS prix_option,
               l.date_fin
        FROM Location l
        JOIN Utilisateurs u ON l.id_utilisateur = u.id_utilisateur
        JOIN Voitures v ON l.id_voiture = v.id_voiture
        LEFT JOIN Option o ON l.id_option = o.id_option
        WHERE l.id_location NOT IN (SELECT id_location FROM Facture)
        ORDER BY l.id_location DESC
    """)

    if df_loc_sans_fact.empty:
        st.success("✅ Toutes les locations ont déjà une facture.")
    else:
        loc_sf_labels = df_loc_sans_fact["label"].tolist()
        loc_sf_ids = df_loc_sans_fact["id_location"].tolist()

        sel_loc_sf = st.selectbox("Location sans facture", loc_sf_labels, key="create_fact_loc")
        idx_sf = loc_sf_labels.index(sel_loc_sf)
        row_sf = df_loc_sans_fact.iloc[idx_sf]
        id_loc_sf = loc_sf_ids[idx_sf]

        # Calcul automatique
        df_loc_detail = run_query(
            "SELECT date_debut, date_fin FROM Location WHERE id_location = ?", (id_loc_sf,)
        )
        montant_auto = 0.0
        if not df_loc_detail.empty:
            try:
                dd = date.fromisoformat(df_loc_detail.iloc[0]["date_debut"])
                df_ = date.fromisoformat(df_loc_detail.iloc[0]["date_fin"])
                nb_j = (df_ - dd).days
                montant_auto = round((float(row_sf["prix_journalier"]) + float(row_sf["prix_option"])) * nb_j, 2)
            except Exception:
                pass

        c1, c2, c3 = st.columns(3)
        with c1:
            nouveau_montant = st.number_input("Montant (€)", min_value=0.0,
                                              value=montant_auto, step=10.0, key="create_fact_montant")
        with c2:
            statuts_new = ["en_attente", "payee"]
            new_statut_new = st.selectbox("Statut", statuts_new, key="create_fact_statut")
        with c3:
            try:
                date_fact_def = date.fromisoformat(row_sf["date_fin"]) if row_sf["date_fin"] else date.today()
            except Exception:
                date_fact_def = date.today()
            new_date_fact = st.date_input("Date facture", value=date_fact_def, key="create_fact_date")

        if st.button("✅ Créer la facture", key="btn_create_fact"):
            fid = run_write(
                "INSERT INTO Facture (id_location, montant, date_facture, statut_paiement) VALUES (?,?,?,?)",
                (id_loc_sf, float(nouveau_montant), new_date_fact.isoformat(), new_statut_new)
            )
            if fid:
                st.success(f"✅ Facture #{fid} créée !")
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# ONGLET 3 — AVIS CLIENTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_avis:
    st.subheader("⭐ Avis clients")

    df_avis = run_query("""
        SELECT a.id_avis,
               u.nom || ' ' || u.prenom AS client,
               v.marque || ' ' || v.modele AS voiture,
               a.note, a.commentaire, a.date_avis
        FROM Avis a
        JOIN Utilisateurs u ON a.id_utilisateur = u.id_utilisateur
        JOIN Voitures v ON a.id_voiture = v.id_voiture
        ORDER BY a.date_avis DESC
    """)
    st.dataframe(df_avis, use_container_width=True, hide_index=True)

    # Note moyenne par voiture
    st.markdown("---")
    st.subheader("📊 Notes moyennes par voiture")
    df_notes = run_query("""
        SELECT v.marque || ' ' || v.modele AS voiture,
               ROUND(AVG(a.note), 2) AS note_moyenne,
               COUNT(*) AS nb_avis
        FROM Avis a
        JOIN Voitures v ON a.id_voiture = v.id_voiture
        GROUP BY v.id_voiture
        ORDER BY note_moyenne DESC
    """)
    st.dataframe(df_notes, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Ajouter un avis ───────────────────────────────────────────────────────
    with st.expander("➕ Ajouter un avis", expanded=False):
        df_users_av = run_query("SELECT id_utilisateur, nom || ' ' || prenom AS label FROM Utilisateurs ORDER BY nom")
        df_cars_av = run_query("SELECT id_voiture, marque || ' ' || modele AS label FROM Voitures ORDER BY marque")
        if df_users_av.empty or df_cars_av.empty:
            st.warning("Aucun client ou voiture enregistré.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                av_cli_labels = df_users_av["label"].tolist()
                av_cli_ids = df_users_av["id_utilisateur"].tolist()
                sel_av_cli = st.selectbox("Client *", av_cli_labels, key="add_av_cli")
                id_av_cli = av_cli_ids[av_cli_labels.index(sel_av_cli)]

                av_car_labels = df_cars_av["label"].tolist()
                av_car_ids = df_cars_av["id_voiture"].tolist()
                sel_av_car = st.selectbox("Voiture *", av_car_labels, key="add_av_car")
                id_av_car = av_car_ids[av_car_labels.index(sel_av_car)]

            with c2:
                note_av = st.slider("Note (1-5) *", min_value=1, max_value=5, value=4, key="add_av_note")
                date_av = st.date_input("Date de l'avis", value=date.today(), key="add_av_date")
                commentaire_av = st.text_area("Commentaire", key="add_av_comment", height=80)

            if st.button("✅ Ajouter l'avis", key="btn_add_av"):
                avid = run_write(
                    "INSERT INTO Avis (id_utilisateur, id_voiture, note, commentaire, date_avis) VALUES (?,?,?,?,?)",
                    (id_av_cli, id_av_car, note_av, commentaire_av.strip() or None, date_av.isoformat())
                )
                if avid:
                    st.success(f"✅ Avis #{avid} ajouté !")
                    st.rerun()

    st.markdown("---")

    # ── Supprimer un avis ─────────────────────────────────────────────────────
    with st.expander("🗑️ Supprimer un avis", expanded=False):
        df_avis_del = run_query("""
            SELECT a.id_avis,
                   '#' || a.id_avis || ' — ' || u.nom || ' ' || u.prenom || ' — ' || v.marque || ' ' || v.modele || ' (' || a.note || '/5)' AS label
            FROM Avis a
            JOIN Utilisateurs u ON a.id_utilisateur = u.id_utilisateur
            JOIN Voitures v ON a.id_voiture = v.id_voiture
            ORDER BY a.id_avis DESC
        """)
        if not df_avis_del.empty:
            del_av_labels = df_avis_del["label"].tolist()
            del_av_ids = df_avis_del["id_avis"].tolist()
            sel_del_av = st.selectbox("Avis à supprimer", del_av_labels, key="del_av_sel")
            confirm_del_av = st.checkbox("Je confirme la suppression", key="confirm_del_av")
            if st.button("🗑️ Supprimer", key="btn_del_av", type="primary"):
                if confirm_del_av:
                    id_del_av = del_av_ids[del_av_labels.index(sel_del_av)]
                    run_write("DELETE FROM Avis WHERE id_avis = ?", (id_del_av,))
                    st.success("Avis supprimé.")
                    st.rerun()
                else:
                    st.error("Veuillez cocher la case de confirmation.")

st.markdown("---")
st.subheader("📈 Argent encaissé par mois")
df_mensuel = run_query("""
    SELECT strftime('%Y-%m', date_facture) AS mois,
           ROUND(SUM(montant), 2) AS montant_encaisse
    FROM Facture
    WHERE statut_paiement = 'payee' AND date_facture IS NOT NULL
    GROUP BY strftime('%Y-%m', date_facture)
    ORDER BY mois
""")

if not df_mensuel.empty:
    df_mensuel["mois"] = pd.to_datetime(df_mensuel["mois"] + "-01")
    df_mensuel["mois"] = df_mensuel["mois"].dt.strftime("%m/%Y")
    st.bar_chart(df_mensuel.set_index("mois")["montant_encaisse"])
else:
    st.info("Pas encore de paiements enregistrés pour afficher ce graphique.")

