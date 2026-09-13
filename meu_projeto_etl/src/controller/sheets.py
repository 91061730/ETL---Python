import gspread
import os
from pathlib import Path
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Carrega o .env da pasta raiz
load_dotenv()

class SheetsController:
    def __init__(self):
        # BASE_DIR será a pasta 'meu_projeto_etl'
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        # Aponta diretamente para o arquivo na raiz
        self.creds_path = BASE_DIR / 'credentials.json'

        if not self.creds_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado em: {self.creds_path}. Verifique se o nome é 'credentials.json'")

        scope = ['https://www.googleapis.com/auth/spreadsheets']
        # Converte o objeto Path para string, conforme exigido pela biblioteca
        creds = Credentials.from_service_account_file(str(self.creds_path), scopes=scope)
        client = gspread.authorize(creds)

        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        self.sheet = client.open_by_key(sheet_id).sheet1

    def testar_conexao(self):
        return f"Conectado com sucesso à planilha: {self.sheet.title}"

    def append_data(self, data):
        self.sheet.append_row(data)

    def append_data_lote(self, lista_de_linhas):
        self.sheet.append_rows(lista_de_linhas)

    def escrever_cabecalho(self,cabecalho):
        self.sheet.insert_row(cabecalho,1)