import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Mon Dashboard Dynamique", page_icon="🚀", layout="wide")

# ID de votre Google Sheet
SHEET_ID = "1nhlDCHOQbXWYVRuMfyCrA7tgTIuA_qtFy5HDkFvQqBk"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

# 2. CSS Personnalisé pour des tuiles style "Microsoft Apps"
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); }
    
    /* SIDEBAR : Fond gris clair et texte noir */
    [data-testid="stSidebar"] { background-color: #f0f2f6 !important; }
    [data-testid="stSidebar"] * { color: #000000 !important; }

    /* CENTRE : Tuiles COMPACTES (Style Microsoft) */
    .stLinkButton > a {
        width: 100%; 
        height: 90px !important; /* Hauteur réduite */
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important; 
        color: white !important;
        display: flex !important;
        flex-direction: column !important; /* Icone au dessus du texte */
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        padding: 5px !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stLinkButton > a:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        border-color: #ffffff !important;
        transform: scale(1.02);
    }

    /* Ajustement de la taille de la police dans les boutons */
    .stLinkButton p {
        font-size: 0.85rem !important;
        line-height: 1.2 !important;
        text-align: center !important;
        margin-top: 5px !important;
    }

    h1, h3 { color: white !important; text-align: center; font-weight: 300; }
    
    /* Cacher les bordures inutiles des onglets */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(255,255,255,0.05); 
        border-radius: 5px; 
        color: white; 
    }
</style>
""", unsafe_allow_html=True)

# 3. FONCTIONS DE CHARGEMENT
@st.cache_data(ttl=60)
def get_all_sheet_names():
    xl = pd.ExcelFile(BASE_URL, engine='openpyxl')
    return xl.sheet_names

@st.cache_data(ttl=60)
def get_data_from_sheet(sheet_name):
    return pd.read_excel(BASE_URL, sheet_name=sheet_name, engine='openpyxl')

# 4. EXÉCUTION
try:
    liste_onglets = get_all_sheet_names()

    with st.sidebar:
        st.markdown("## 📂 Navigation")
        choix = st.radio("Choisir l'univers :", liste_onglets, key="nav_radio")
        st.divider()
        if st.button("🔄 Actualiser les données"):
            st.cache_data.clear()
            st.rerun()

    st.markdown(f"<h1>🚀 {choix}</h1>", unsafe_allow_html=True)

    df = get_data_from_sheet(choix)
    
    if df is not None and not df.empty:
        search = st.text_input("🔍 Rechercher...", label_visibility="collapsed", key="search_bar")
        
        if search and 'nom' in df.columns:
            df = df[df['nom'].str.contains(search, case=False, na=False)]

        if 'categorie' in df.columns:
            categories = df['categorie'].unique()
            tabs = st.tabs(list(categories))

            for i, cat in enumerate(categories):
                with tabs[i]:
                    apps_cat = df[df['categorie'] == cat]
                    # GRILLE DE 8 COLONNES pour des tuiles plus petites
                    nb_cols = 8
                    cols = st.columns(nb_cols)
                    for idx, row in enumerate(apps_cat.itertuples()):
                        with cols[idx % nb_cols]:
                            ico = getattr(row, 'icone', '🌐')
                            nom = getattr(row, 'nom', 'App')
                            url = getattr(row, 'url', '#')
                            st.link_button(label=f"{ico}\n{nom}", url=url, use_container_width=True)
        else:
            st.warning("Colonne 'categorie' manquante.")
    else:
        st.info(f"L'onglet '{choix}' est vide.")

except Exception as e:
    st.error(f"Erreur : {e}")
