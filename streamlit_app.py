import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Mon Hub Multi-Projets", page_icon="🚀", layout="wide")

# Connexion à Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# ========================================
# CSS PERSONNALISÉ
# ========================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); }
    .stLinkButton > a {
        width: 100%; height: 100px;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important; color: white !important;
        display: flex; align-items: center; justify-content: center;
        text-decoration: none; font-weight: bold;
    }
    .stLinkButton > a:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-3px); border-color: #667eea !important;
    }
    h1, h3, p { color: white !important; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ========================================
# BARRE LATÉRALE (NAVIGATION)
# ========================================
with st.sidebar:
    st.title("📂 Mes Univers")
    
    # ATTENTION : Ces noms doivent être EXACTEMENT les mêmes que vos onglets Google Sheets
    univers_choisi = st.radio(
        "Choisir un univers :",
        ["General", "Finance", "Musique"], # Modifiez ces noms selon vos besoins
        index=0
    )
    
    st.divider()
    if st.button("🔄 Actualiser les données"):
        st.cache_data.clear()
        st.rerun()

# ========================================
# CHARGEMENT DES DONNÉES
# ========================================
@st.cache_data(ttl="1m")
def load_data(sheet_name):
    # On utilise l'URL des secrets et on précise l'onglet (worksheet)
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    return conn.read(spreadsheet=url, worksheet=sheet_name)

try:
    df = load_data(univers_choisi)
except Exception as e:
    st.error(f"Erreur : Impossible de trouver l'onglet nommé '{univers_choisi}' dans votre Google Sheet.")
    st.stop()

# ========================================
# INTERFACE PRINCIPALE
# ========================================
st.markdown(f"<h1>🚀 Univers {univers_choisi}</h1>", unsafe_allow_html=True)

# Barre de recherche
search = st.text_input("🔍 Rechercher une application...", label_visibility="collapsed")

if df is not None:
    if search:
        df = df[df['nom'].str.contains(search, case=False, na=False)]

    # Séparation par catégories (les onglets horizontaux au centre)
    categories = df['categorie'].unique()
    tabs = st.tabs(list(categories))

    for i, cat in enumerate(categories):
        with tabs[i]:
            apps_cat = df[df['categorie'] == cat]
            cols = st.columns(4)
            for idx, row in enumerate(apps_cat.itertuples()):
                with cols[idx % 4]:
                    st.link_button(
                        label=f"{row.icone} {row.nom}",
                        url=row.url,
                        use_container_width=True
                    )
