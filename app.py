import streamlit as st
import pandas as pd
import pygsheets
import json

# Configuração da página
st.set_page_config(page_title="Google Sheets + Streamlit",
                   page_icon="📊", layout="wide")

# --- Autenticação via secrets ---
creds = st.secrets["gcp_service_account"]  # pega o bloco do secrets
creds_json = json.dumps(dict(creds))        # transforma dict em string JSON
client = pygsheets.authorize(service_account_json=creds_json)

# --- Conectar à planilha ---
sheet_url = "https://docs.google.com/spreadsheets/d/16d4yI58TXd0BbEXqGg4Ty7wx30iskWn2nxP5pxVeKeU/"
arquivo = client.open_by_url(sheet_url)
aba = arquivo.worksheet_by_title("streamlit")

# --- Função para renomear colunas duplicadas ---
def rename_duplicates(cols):
    counts = {}
    new_cols = []
    for c in cols:
        if c in counts:
            counts[c] += 1
            new_cols.append(f"{c}_{counts[c]}")
        else:
            counts[c] = 0
            new_cols.append(c)
    return new_cols

# --- Função para carregar dados da planilha ---
def carregar_dados():
    data = aba.get_all_values()
    if len(data) > 1:
        return pd.DataFrame(data[1:], columns=rename_duplicates(data[0]))
    else:
        return pd.DataFrame(columns=["Coluna1", "Coluna2", "Coluna3"])

# --- Formulário para adicionar novos dados ---
st.title("📊 APRENDENDO A CONECTAR GOOGLE SHEETS COM STREAMLIT")
st.subheader("📥 Adicionar novos dados")

with st.form(key="form_adicionar"):
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    departamento = st.text_input("Departamento")
    
    submit_button = st.form_submit_button(label="Enviar")

    if submit_button:
        if nome and departamento:  # validaç
