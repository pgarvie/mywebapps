import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mon Dashboard Pro", page_icon="🚀", layout="wide")

SHEET_ID = "1nhlDCHOQbXWYVRuMfyCrA7tgTIuA_qtFy5HDkFvQqBk"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

# CSS amélioré pour un look identique à Microsoft
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #f3f2f1 !important; }
    [data-testid="stSidebar"] * { color: #323130 !important; }

    /* Conteneur de la tuile */
    .app-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 10px;
        border: 1px solid #edebe9;
        border-radius: 4px;
        background-color: #ffffff;
        text-decoration: none !important; /* Enlever le soulignement */
        transition: all 0.2s;
        height: 110px;
        margin-bottom: 15px;
    }
    .app-card:hover {
        background-color: #f3f2f1;
        border-color: #a19f9d;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    /* Image du logo */
    .app-logo {
        width: 42px;
        height: 42px;
        margin-bottom: 10px;
        object-fit: contain;
        border-radius: 4px;
    }
    
    /* Emoji si pas d'image */
    .app-emoji {
        font-size: 32px;
        margin-bottom: 8px;
    }
    
    /* Nom de l'application */
    .app-name {
        color: #323130 !important;
        font-size: 0.85rem;
        font-weight: 500;
        text-align: center;
        text-decoration: none !important;
        line-height: 1.2;
    }
    
    /* Enlever les soulignements des liens par défaut */
    a { text-decoration: none !important; }
    
    h1 { color: #323130 !important; font-weight: 600; font-size: 1.4rem !important; margin-bottom: 20px; }
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
        st.markdown("### 📂 Mes Applications")
        choix = st.radio("Navigation", liste_onglets)
        st.divider()
        if st.button("🔄 Actualiser"):
            st.cache_data.clear()
            st.rerun()

    st.markdown(f"<h1>{choix}</h1>", unsafe_allow_html=True)

    df = get_data_from_sheet(choix)
    
    if df is not None and not df.empty:
        categories = df['categorie'].unique()
        tabs = st.tabs(list(categories))

        for i, cat in enumerate(categories):
            with tabs[i]:
                apps_cat = df[df['categorie'] == cat]
                nb_cols = 6
                cols = st.columns(nb_cols)
                
                for idx, row in enumerate(apps_cat.itertuples()):
                    with cols[idx % nb_cols]:
                        # Nettoyage de la valeur de l'icône (enlève les espaces)
                        ico = str(getattr(row, 'icone', '🌐')).strip()
                        nom = getattr(row, 'nom', 'App')
                        url = getattr(row, 'url', '#')
                        
                        # Détection : Image ou Emoji
                        if ico.startswith("http"):
                            icon_html = f'<img src="{ico}" class="app-logo" onerror="this.src=\'https://www.google.com/s2/favicons?sz=64&domain={url}\'">'
                        else:
                            icon_html = f'<div class="app-emoji">{ico}</div>'
                        
                        st.markdown(f"""
                            <a href="{url}" target="_blank" class="app-card">
                                {icon_html}
                                <div class="app-name">{nom}</div>
                            </a>
                        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erreur : {e}")
