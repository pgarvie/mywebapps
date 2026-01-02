import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mon Dashboard Pro", page_icon="🚀", layout="wide")

SHEET_ID = "1nhlDCHOQbXWYVRuMfyCrA7tgTIuA_qtFy5HDkFvQqBk"
BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

# CSS pour le look Microsoft
st.markdown("""
<style>
    .stApp { background-color: #ffffff; } /* Fond blanc comme MS */
    
    [data-testid="stSidebar"] { background-color: #f3f2f1 !important; }
    [data-testid="stSidebar"] * { color: #323130 !important; }

    /* Conteneur de la tuile */
    .app-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 15px;
        border: 1px solid #edebe9;
        border-radius: 4px;
        background-color: #ffffff;
        text-decoration: none;
        transition: all 0.2s;
        height: 110px;
        margin-bottom: 10px;
    }
    .app-card:hover {
        background-color: #f3f2f1;
        border-color: #a19f9d;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .app-logo {
        width: 40px;
        height: 40px;
        margin-bottom: 10px;
        object-fit: contain;
    }
    .app-emoji {
        font-size: 30px;
        margin-bottom: 5px;
    }
    .app-name {
        color: #323130;
        font-size: 0.85rem;
        font-weight: 500;
        text-align: center;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    h1 { color: #323130 !important; font-weight: 600; font-size: 1.5rem !important; }
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
        st.markdown("## 📂 Mes Applications")
        choix = st.radio("Navigation", liste_onglets)
        if st.button("🔄 Actualiser"):
            st.cache_data.clear()
            st.rerun()

    st.markdown(f"<h1>{choix}</h1>", unsafe_allow_html=True)

    df = get_data_from_sheet(choix)
    
    if df is not None and not df.empty:
        # Onglets de catégories
        categories = df['categorie'].unique()
        tabs = st.tabs(list(categories))

        for i, cat in enumerate(categories):
            with tabs[i]:
                apps_cat = df[df['categorie'] == cat]
                nb_cols = 6
                cols = st.columns(nb_cols)
                
                for idx, row in enumerate(apps_cat.itertuples()):
                    with cols[idx % nb_cols]:
                        ico = str(getattr(row, 'icone', '🌐'))
                        nom = getattr(row, 'nom', 'App')
                        url = getattr(row, 'url', '#')
                        
                        # Déterminer si c'est une image URL ou un Emoji
                        if ico.startswith("http"):
                            icon_html = f'<img src="{ico}" class="app-logo">'
                        else:
                            icon_html = f'<div class="app-emoji">{ico}</div>'
                        
                        # Création de la tuile personnalisée en HTML/CSS
                        st.markdown(f"""
                            <a href="{url}" target="_blank" class="app-card">
                                {icon_html}
                                <div class="app-name">{nom}</div>
                            </a>
                        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erreur : {e}")
