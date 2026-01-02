import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Mon Dashboard", page_icon="🚀", layout="wide")

# 2. CSS Personnalisé (Texte noir à gauche et tuiles blanches au centre)
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); }
    
    /* SIDEBAR : Fond gris clair et TEXTE NOIR */
    [data-testid="stSidebar"] { background-color: #f0f2f6 !important; }
    [data-testid="stSidebar"] * { color: #000000 !important; }

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

# 3. BARRE LATÉRALE
with st.sidebar:
    st.markdown("## 📂 Navigation")
    choix = st.radio(
        "Choisir l'univers :",
        ["General", "SMART Trading", "Finance", "Musique"],
        key="nav_radio"
    )
    st.divider()
    if st.button("🔄 Actualiser les données"):
        st.cache_data.clear()
        st.rerun()

# 4. FONCTION DE CHARGEMENT (Méthode CSV Directe)
@st.cache_data(ttl=60)
def get_data(sheet_name):
    # ID de votre document extrait de votre URL
    SHEET_ID = "1nhlDCHOQbXWYVRuMfyCrA7tgTIuA_qtFy5HDkFvQqBk"
    # Construction de l'URL d'export CSV pour l'onglet spécifique
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)

# 5. AFFICHAGE
st.markdown(f"<h1>🚀 Univers : {choix}</h1>", unsafe_allow_html=True)

try:
    df = get_data(choix)
    
    if df is not None and not df.empty:
        # Barre de recherche
        search = st.text_input("🔍 Rechercher...", label_visibility="collapsed", key="search_bar")
        
        if search:
            # Filtrage sur la colonne 'nom'
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
                            st.link_button(
                                label=f"{row.icone} {row.nom}", 
                                url=row.url, 
                                use_container_width=True
                            )
        else:
            st.error("La colonne 'categorie' est manquante dans votre fichier Google Sheets.")
    else:
        st.warning(f"L'onglet '{choix}' semble vide.")

except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.info("Vérifiez que votre Google Sheet est partagé avec 'Anyone with the link'.")
