import streamlit as st
import random
import time
from datetime import datetime
import json
from google_sheets import get_game_state, update_game_state

# Configuración
st.set_page_config(
    page_title="El Robo del Año Nuevo - Multijugador",
    page_icon="🎮",
    layout="wide"
)

# Estado del juego compartido
def sync_game_state():
    """Sincronizar estado con Google Sheets"""
    if 'last_sync' not in st.session_state:
        st.session_state.last_sync = 0
    
    # Sincronizar cada 5 segundos
    current_time = time.time()
    if current_time - st.session_state.last_sync > 5:
        shared_state = get_game_state()
        
        # Actualizar estado local
        for key, value in shared_state.items():
            if key not in st.session_state or key == 'last_update':
                st.session_state[key] = value
        
        st.session_state.last_sync = current_time

# ... resto del código similar pero usando sync_game_state()
