import streamlit as st
import pandas as pd
import pygsheets
import json

st.set_page_config(page_title="Google Sheets + Streamlit",
                   page_icon="📊", layout="wide")

# --- Autenticação via secrets ---
creds = st.secrets["gcp_service_account"]       # pega o bloco do secrets
# transforma dict em string JSON
creds_json = json.dumps(dict(creds))
client = pygsheets.authorize(service_account_json=creds_json)

# --- Conectar à planilha ---
sheet_url = "https://docs.google.com/spreadsheets/d/16d4yI58TXd0BbEXqGg4Ty7wx30iskWn2nxP5pxVeKeU/"
arquivo = client.open_by_url(sheet_url)
aba = arquivo.worksheet_by_title("streamlit")

# --- Ler dados ---
data = aba.get_all_values()
df = pd.DataFrame(data)

# --- Exibir no Streamlit ---
st.title("📊 APRENDENDO A CONECTAR GOOGLE SHEETS COM STREAMLIT")
st.subheader("Importando dados do Google Sheets")

st.write(df)