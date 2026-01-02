import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Mon Dashboard", page_icon="🚀", layout="wide")

# 2. CSS Personnalisé (Style & Couleurs)
st.markdown("""
<style>
    /* Fond de l'application */
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); }
    
    /* Style de la barre latérale (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    
    /* FORCE LE TEXTE EN NOIR DANS LA SIDEBAR */
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    /* Style des tuiles au centre */
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
        border-color: #667eea !important;
    }
    h1, h3 { color: white !important; text-align: center; }
</style>
""", unsafe_allow_html=True)

# 3. Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. BARRE LATÉRALE
with st.sidebar:
    st.markdown("## 📂 Navigation")
    choix = st.radio(
        "Choisir l'univers :",
        ["General", "Finance", "Musique"],
        key="nav_radio"
    )
    st.divider()
    if st.button("🔄 Actualiser les données"):
        st.cache_data.clear()
        st.rerun()

# 5. CHARGEMENT DES DONNÉES
@st.cache_data(ttl=60)
def get_data(nom_onglet):
    # Récupération de l'URL depuis les secrets
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    # Lecture spécifique de l'onglet
    return conn.read(spreadsheet=url, worksheet=nom_onglet)

# 6. AFFICHAGE PRINCIPAL
st.markdown(f"<h1>🚀 Univers : {choix}</h1>", unsafe_allow_html=True)

try:
    df = get_data(choix)
    
    if df is not None and not df.empty:
        # Barre de recherche
        search = st.text_input("🔍 Rechercher...", label_visibility="collapsed", key="search_bar")
        
        if search:
            df = df[df['nom'].str.contains(search, case=False, na=False)]

        # Création des onglets par catégorie
        categories = df['categorie'].unique()
        if len(categories) > 0:
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
        else:
            st.info("Ajoutez une catégorie dans votre fichier Excel pour voir les applications.")
    else:
        st.warning(f"L'onglet '{choix}' semble vide ou n'est pas accessible.")

except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.info("Vérifiez que l'onglet dans Google Sheets s'appelle exactement comme dans le menu.")
