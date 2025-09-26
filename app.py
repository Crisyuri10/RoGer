import streamlit as st
import pandas as pd
import pygsheets
import json

# Configuração da página
st.set_page_config(page_title="Google Sheets + Streamlit",
                   page_icon="📊", layout="wide")

# --- Autenticação via secrets ---
creds = st.secrets["gcp_service_account"]
creds_json = json.dumps(dict(creds))
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
        return pd.DataFrame(columns=["Nome", "Idade", "Profissão"])

# --- Lista de profissões ---
profissoes = [
    "Engenheiro", "Médico", "Professor", "Advogado", "Enfermeiro",
    "Analista de Sistemas", "Designer", "Arquiteto", "Contador",
    "Motorista", "Técnico", "Cozinheiro", "Vendedor", "Atendente"
]

# --- Formulário para adicionar novos dados ---
st.title("📊 APRENDENDO A CONECTAR GOOGLE SHEETS COM STREAMLIT")
st.subheader("📥 Adicionar novos dados")

with st.form(key="form_adicionar"):
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    profissao = st.selectbox("Profissão", options=profissoes)
    
    submit_button = st.form_submit_button(label="Enviar")

    if submit_button:
        if nome and profissao:
            aba.append_table(values=[nome, idade, profissao], start='A1', end=None, dimension='ROWS', overwrite=False)
            st.success("✅ Dados enviados com sucesso!")
        else:
            st.error("❌ Preencha todos os campos obrigatórios!")

# --- Exibir dados existentes ---
st.subheader("📋 Dados existentes no Google Sheets")
df = carregar_dados()
st.dataframe(df, use_container_width=True)
