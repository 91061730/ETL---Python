import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Escopo de permissões que a API vai usar
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Carrega as credenciais do arquivo JSON
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

# Autoriza o cliente gspread com essas credenciais
client = gspread.authorize(creds)

print("Autenticado com sucesso!")

df = pd.read_csv("vendas.csv")

print("Dados brutos:")
print(df)