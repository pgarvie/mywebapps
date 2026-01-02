import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Mon Dashboard", page_icon="🚀", layout="wide")

# 2. Connexion
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. CSS
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
    h1, h3, p, label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# 4. BARRE LATÉRALE
with st.sidebar:
    st.write("✅ Version du code : Multi-Univers") # Pour vérifier que le code est à jour
    st.title("📂 Navigation")
    
    # Liste sans accents pour éviter les bugs
    choix = st.radio(
        "Choisir l'univers :",
        ["General", "Finance", "Musique"],
        key="navigation_radio"
    )
    
    st.divider()
    if st.button("🔄 Forcer l'actualisation"):
        st.cache_data.clear()
        st.rerun()

# 5. CHARGEMENT DES DONNÉES
@st.cache_data(ttl=60)
def get_data(nom_onglet):
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    return conn.read(spreadsheet=url, worksheet=nom_onglet)

# 6. AFFICHAGE
st.markdown(f"<h1>🚀 Univers : {choix}</h1>", unsafe_allow_html=True)

try:
    df = get_data(choix)
    
    search = st.text_input("🔍 Rechercher...", label_visibility="collapsed")
    
    if search:
        df = df[df['nom'].str.contains(search, case=False, na=False)]

    if not df.empty:
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
        st.warning(f"L'onglet '{choix}' semble vide.")

except Exception as e:
    st.error(f"Erreur de lecture de l'onglet '{choix}'.")
    st.info("Vérifiez que le nom de l'onglet dans Google Sheets est exactement le même que dans le menu à gauche.")
    st.write(e)
