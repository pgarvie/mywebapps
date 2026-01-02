import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Config
st.set_page_config(page_title="Mon Dashboard", page_icon="🚀", layout="wide")

# 2. CSS Personnalisé
st.markdown("""
<style>
    /* Fond de l'application */
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); }
    
    /* Style de la barre latérale (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    /* TEXTE EN NOIR DANS LA SIDEBAR */
    [data-testid="stSidebar"] .stText, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] .stMarkdown {
        color: black !important;
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
    h1, h3 { color: white !important; }
</style>
""", unsafe_allow_html=True)

# 3. Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. BARRE LATÉRALE
with st.sidebar:
    st.markdown("### 📂 Navigation")
    choix = st.radio(
        "Choisir l'univers :",
        ["General", "Finance", "Musique"],
        key="nav"
    )
    st.divider()
    if st.button("🔄 Forcer l'actualisation"):
        st.cache_data.clear()
        st.rerun()

# 5. CHARGEMENT DES DONNÉES (Version Robuste)
@st.cache_data(ttl=60)
def get_data(nom_onglet):
    try:
        # Tentative avec la méthode worksheet directe
        url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        return conn.read(spreadsheet=url, worksheet=nom_onglet)
    except Exception:
        # Méthode de secours si le worksheet name cause une erreur 400
        # On lit tout et on filtre manuellement par onglet si nécessaire
        return conn.read(spreadsheet=url)

# 6. AFFICHAGE
st.markdown(f"<h1>🚀 Univers : {choix}</h1>", unsafe_allow_html=True)

try:
    df = get_data(choix)
    
    if df is not None and not df.empty:
        # Barre de recherche
        search = st.text_input("🔍 Rechercher...", label_visibility="collapsed")
        if search:
            df = df[df['nom'].str.contains(search, case=False, na=False)]

        # Onglets de catégories
        categories = df['categorie'].unique()
        tabs = st.tabs(list(categories))

        for i, cat in enumerate(categories):
            with tabs[i]:
                apps_cat = df[df['categorie'] == cat]
                cols = st.columns(4)
                for idx, row in enumerate(apps_cat.itertuples()):
                    with cols[idx % 4]:
                        st.link_button(f"{row.icone} {row.nom}", row.url, use_container_width=True)
    else:
        st.warning(f"Aucune donnée trouvée dans l'onglet '{choix}'.")

except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.info("Vérifiez que votre Google Sheet est partagé en 'Anyone with the link' (Viewer).")}' semble vide.")

except Exception as e:
    st.error(f"Erreur de lecture de l'onglet '{choix}'.")
    st.info("Vérifiez que le nom de l'onglet dans Google Sheets est exactement le même que dans le menu à gauche.")
    st.write(e)
