import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import altair as alt

# Carregar as credenciais a partir do secrets.toml via Streamlit
creds_dict = st.secrets["connections"]["gsheets"]

# Definir os scopes certos
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Usar as credenciais para autenticação COM os scopes
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

# Autorizar o cliente gspread com as credenciais
client = gspread.authorize(creds)

# URL da planilha do Google Sheets
sheet_url = creds_dict["spreadsheet"]

# Aceder à planilha
sheet = client.open_by_url(sheet_url)
worksheet = sheet.get_worksheet(0)  # Primeira aba

# Obter os dados
data = pd.DataFrame(worksheet.get_all_records())

# Limpeza e formatação dos dados
data['preco'] = data['preco'].replace({'€': '', ' ': ''}, regex=True).astype(float)
data['preco_unidade'] = data['preco_unidade'].replace({'€': '', ' ': ''}, regex=True).astype(float)
data['data'] = pd.to_datetime(data['data'], errors='coerce')

# Exibir os dados no Streamlit
st.title("Dados da Planilha do Google Sheets")
st.dataframe(data)

# Criar o gráfico de Altair
chart = alt.Chart(data).mark_line().encode(
    x='data:T',
    y='preco:Q'
).properties(
    title="Preço ao Longo do Tempo"
)

# Exibir o gráfico
st.altair_chart(chart, use_container_width=True)
