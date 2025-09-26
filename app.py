import streamlit as st
import pandas as pd
import pygsheets
import json

# Configuração da página
st.set_page_config(page_title="Google Sheets + Streamlit",
                   page_icon="📊", layout="wide")

# --- Autenticação via secrets ---
creds = st.secrets["gcp_service_account"]       # pega o bloco do secrets
creds_json = json.dumps(dict(creds))            # transforma dict em string JSON
client = pygsheets.authorize(service_account_json=creds_json)

# --- Conectar à planilha ---
sheet_url = "https://docs.google.com/spreadsheets/d/16d4yI58TXd0BbEXqGg4Ty7wx30iskWn2nxP5pxVeKeU/"
arquivo = client.open_by_url(sheet_url)
aba = arquivo.worksheet_by_title("streamlit")

# --- Ler dados ---
data = aba.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])  # assume primeira linha como header

# --- Exibir dados existentes ---
st.title("📊 APRENDENDO A CONECTAR GOOGLE SHEETS COM STREAMLIT")
st.subheader("Dados existentes no Google Sheets")
st.dataframe(df)

# --- Formulário para adicionar novos dados ---
st.subheader("📥 Adicionar novos dados")

with st.form(key="form_adicionar"):
    # Campos do formulário
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    departamento = st.text_input("Departamento")
    
    # Botão de envio
    submit_button = st.form_submit_button(label="Enviar")

    if submit_button:
        # Adicionar linha na planilha
        nova_linha = [nome, idade, departamento]
        aba.append_table(values=nova_linha, start='A1', end=None, dimension='ROWS', overwrite=False)
        st.success("✅ Dados enviados com sucesso!")
        
        # Atualizar dataframe exibido
        data = aba.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        st.dataframe(df)
