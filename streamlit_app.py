import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Mon Dashboard Dynamique", page_icon="🚀", layout="wide")

# ID de votre Google Sheet
SHEET_ID = "1nhlDCHOQbXWYVRuMfyCrA7tgTIuA_qtFy5HDkFvQqBk"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

# 2. CSS Personnalisé
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); }
    
    /* SIDEBAR : Fond gris clair */
    [data-testid="stSidebar"] { background-color: #f0f2f6 !important; }
    
    /* TEXTE NOIR DANS LA SIDEBAR (Titres, Radio boutons, labels) */
    [data-testid="stSidebar"] * { 
        color: #000000 !important; 
    }

    /* CENTRE : Tuiles blanches translucides */
    .stLinkButton > a {
        width: 100%; height: 100px;
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important; color: white !important;
        display: flex; align-items: center; justify-content: center;
        text-decoration: none; font-weight: bold; font-size: 1.1rem;
    }
    .stLinkButton > a:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: #ffffff !important;
        transform: translateY(-2px);
    }
    h1, h3 { color: white !important; text-align: center; }
</style>
""", unsafe_allow_html=True)

# 3. FONCTIONS DE CHARGEMENT (CORRIGÉES)

@st.cache_data(ttl=60)
def get_all_sheet_names():
    """Récupère uniquement la liste des noms d'onglets"""
    # On utilise pd.ExcelFile mais on ne retourne que la liste des noms (serialisable)
    xl = pd.ExcelFile(BASE_URL, engine='openpyxl')
    return xl.sheet_names

@st.cache_data(ttl=60)
def get_data_from_sheet(sheet_name):
    """Récupère les données d'un onglet spécifique"""
    return pd.read_excel(BASE_URL, sheet_name=sheet_name, engine='openpyxl')

# 4. EXÉCUTION
try:
    # Récupération automatique des onglets
    liste_onglets = get_all_sheet_names()

    # BARRE LATÉRALE
    with st.sidebar:
        st.markdown("## 📂 Navigation")
        choix = st.radio(
            "Choisir l'univers :",
            liste_onglets,
            key="nav_radio"
        )
        st.divider()
        if st.button("🔄 Actualiser les données"):
            st.cache_data.clear()
            st.rerun()

    # AFFICHAGE DE L'UNIVERS
    st.markdown(f"<h1>🚀 Univers : {choix}</h1>", unsafe_allow_html=True)

    # Chargement des données de l'onglet choisi
    df = get_data_from_sheet(choix)
    
    if df is not None and not df.empty:
        # Barre de recherche
        search = st.text_input("🔍 Rechercher...", label_visibility="collapsed", key="search_bar")
        
        if search:
            # Filtrage sans erreur si la colonne 'nom' existe
            if 'nom' in df.columns:
                df = df[df['nom'].str.contains(search, case=False, na=False)]

        # Groupement par catégories
        if 'categorie' in df.columns:
            categories = df['categorie'].unique()
            tabs = st.tabs(list(categories))

            for i, cat in enumerate(categories):
                with tabs[i]:
                    apps_cat = df[df['categorie'] == cat]
                    cols = st.columns(4)
                    for idx, row in enumerate(apps_cat.itertuples()):
                        with cols[idx % 4]:
                            # Gestion des liens
                            url_app = getattr(row, 'url', 'https://google.com')
                            nom_app = getattr(row, 'nom', 'Inconnu')
                            ico_app = getattr(row, 'icone', '🌐')
                            
                            st.link_button(
                                label=f"{ico_app} {nom_app}", 
                                url=url_app, 
                                use_container_width=True
                            )
        else:
            st.warning("La colonne 'categorie' est absente de cet onglet.")
    else:
        st.info(f"L'onglet '{choix}' ne contient pas encore de données.")

except Exception as e:
    st.error(f"Oups ! Une erreur est survenue : {e}")
