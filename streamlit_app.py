import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Mon Dashboard Pro", page_icon="🚀", layout="wide")

# ========================================
# CSS PERSONNALISÉ (Style "Tuiles")
# ========================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); }
    .stLinkButton > a {
        width: 100%;
        height: 100px;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        transition: all 0.3s ease;
        display: flex; align-items: center; justify-content: center;
        text-decoration: none; font-weight: bold;
    }
    .stLinkButton > a:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-3px);
        border-color: #667eea !important;
    }
    h1, h3 { color: white !important; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ========================================
# CONNEXION GOOGLE SHEETS
# ========================================
# On utilise la connexion native de Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # Remplacez l'URL ci-dessous par celle de votre Google Sheet
    # Ou configurez-la dans les secrets (recommandé)
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    return conn.read(spreadsheet=url, ttl="1m") # ttl="1m" rafraîchit les données toutes les minutes

try:
    df = load_data()
except Exception as e:
    st.error("Erreur de connexion au Google Sheet. Vérifiez l'URL dans les secrets.")
    st.stop()

# ========================================
# INTERFACE PRINCIPALE
# ========================================
st.title("🚀 Mon Dashboard")

# Barre de recherche
search = st.text_input("🔍 Rechercher...", label_visibility="collapsed")

if df is not None:
    # Filtrer par recherche
    if search:
        df = df[df['nom'].str.contains(search, case=False, na=False)]

    # Séparation par catégories
    categories = df['categorie'].unique()
    tabs = st.tabs(list(categories))

    for i, cat in enumerate(categories):
        with tabs[i]:
            apps_cat = df[df['categorie'] == cat]
            # Créer une grille de 4 colonnes
            cols = st.columns(4)
            for idx, row in enumerate(apps_cat.itertuples()):
                with cols[idx % 4]:
                    st.link_button(
                        label=f"{row.icone} {row.nom}",
                        url=row.url,
                        use_container_width=True
                    )

# Petit bouton de rafraîchissement manuel
if st.sidebar.button("🔄 Actualiser les données"):
    st.cache_data.clear()
    st.rerun()
