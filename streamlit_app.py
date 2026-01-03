import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Mon Dashboard Sécurisé", page_icon="🔒", layout="wide")

# ========================================
# SYSTÈME DE VERROUILLAGE (SERRURE)
# ========================================
def check_password():
    """Retourne True si l'utilisateur a saisi le bon mot de passe."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<h2 style='text-align: center; color: white;'>🔒 Accès Restreint</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            pwd_input = st.text_input("Entrez le mot de passe pour continuer :", type="password")
            if st.button("Se connecter"):
                if pwd_input == st.secrets["MOT_DE_PASSE"]:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Mot de passe incorrect")
        return False
    return True

# Si le mot de passe n'est pas bon, on arrête l'exécution ici
if not check_password():
    st.stop()

# ========================================
# LE RESTE DE VOTRE APPLICATION (LE HUB)
# ========================================

# ID de votre Google Sheet
SHEET_ID = "1nhlDCHOQbXWYVRuMfyCrA7tgTIuA_qtFy5HDkFvQqBk"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

# CSS (Le même que précédemment)
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); }
    [data-testid="stSidebar"] { background-color: #f3f2f1 !important; }
    [data-testid="stSidebar"] * { color: #323130 !important; }
    .app-card {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        padding: 10px; border: 1px solid #edebe9; border-radius: 4px;
        background-color: #ffffff; text-decoration: none !important; transition: all 0.2s;
        height: 110px; margin-bottom: 15px;
    }
    .app-card:hover { background-color: #f3f2f1; border-color: #a19f9d; transform: translateY(-2px); }
    .app-logo { width: 42px; height: 42px; margin-bottom: 10px; object-fit: contain; border-radius: 4px; }
    .app-emoji { font-size: 32px; margin-bottom: 8px; }
    .app-name { color: #323130 !important; font-size: 0.85rem; font-weight: 500; text-align: center; }
    h1 { color: white !important; text-align: center; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_all_sheet_names():
    xl = pd.ExcelFile(BASE_URL, engine='openpyxl')
    return xl.sheet_names

@st.cache_data(ttl=60)
def get_data_from_sheet(sheet_name):
    return pd.read_excel(BASE_URL, sheet_name=sheet_name, engine='openpyxl')

try:
    liste_onglets = get_all_sheet_names()
    with st.sidebar:
        st.markdown("### 📂 Navigation")
        choix = st.radio("Univers", liste_onglets)
        st.divider()
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

    st.markdown(f"<h1>🚀 {choix}</h1>", unsafe_allow_html=True)
    df = get_data_from_sheet(choix)
    
    if df is not None and not df.empty:
        categories = df['categorie'].unique()
        tabs = st.tabs(list(categories))
        for i, cat in enumerate(categories):
            with tabs[i]:
                apps_cat = df[df['categorie'] == cat]
                cols = st.columns(6)
                for idx, row in enumerate(apps_cat.itertuples()):
                    with cols[idx % 6]:
                        ico = str(getattr(row, 'icone', '🌐')).strip()
                        nom = getattr(row, 'nom', 'App')
                        url = getattr(row, 'url', '#')
                        if ico.startswith("http"):
                            icon_html = f'<img src="{ico}" class="app-logo" onerror="this.src=\'https://www.google.com/s2/favicons?sz=64&domain={url}\'">'
                        else:
                            icon_html = f'<div class="app-emoji">{ico}</div>'
                        st.markdown(f'<a href="{url}" target="_blank" class="app-card">{icon_html}<div class="app-name">{nom}</div></a>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erreur : {e}")
