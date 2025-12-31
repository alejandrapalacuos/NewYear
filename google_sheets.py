# google_sheets.py
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Configuración
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = 'TU_ID_DE_GOOGLE_SHEET'

def init_google_sheets():
    """Inicializar conexión con Google Sheets"""
    creds = Credentials.from_service_account_file(
        'service_account.json',
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client

def get_game_state():
    """Obtener estado del juego desde Google Sheets"""
    client = init_google_sheets()
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    
    # Convertir a diccionario
    data = sheet.get_all_records()
    return data[0] if data else {}

def update_game_state(updates):
    """Actualizar estado del juego en Google Sheets"""
    client = init_google_sheets()
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    
    # Obtener datos actuales
    current = get_game_state()
    current.update(updates)
    
    # Actualizar
    sheet.update('A1', [list(current.keys())])
    sheet.update('A2', [list(current.values())])
