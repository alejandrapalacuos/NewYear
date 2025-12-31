import streamlit as st
import random
import time
from datetime import datetime
import json
from typing import Dict, List, Optional

# Configuración de página
st.set_page_config(
    page_title="El Robo del Año Nuevo",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado mejorado
st.markdown("""
<style>
    /* Estilos generales */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        text-align: center;
        color: white;
        font-size: 3.5em;
        margin-bottom: 20px;
        text-shadow: 0 4px 6px rgba(0,0,0,0.3);
        font-family: 'Arial Black', sans-serif;
        background: linear-gradient(45deg, #FF6B00, #FFD166);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px;
    }
    
    .welcome-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        max-width: 600px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
        border: 3px solid #FF6B00;
    }
    
    .player-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    
    .player-card:hover {
        transform: translateY(-5px);
    }
    
    .secret-role-card {
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        border: 3px dashed gold;
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        color: white;
        animation: pulse 2s infinite;
    }
    
    .phase-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border-left: 5px solid #FF6B00;
    }
    
    .timer-container {
        background: linear-gradient(135deg, #FF6B00 0%, #FF8E53 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(255,107,0,0.3);
    }
    
    .evidence-card {
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s;
    }
    
    .evidence-card:hover {
        background: #e9ecef;
        transform: scale(1.02);
    }
    
    .vote-card {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #FF6B00, #FF8E53);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.1em;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(255,107,0,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255,107,0,0.4);
    }
    
    .role-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px;
        font-size: 0.9em;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 107, 0, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 107, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 107, 0, 0); }
    }
    
    .login-container {
        max-width: 500px;
        margin: 50px auto;
        padding: 40px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .player-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin: 10px auto;
        background: linear-gradient(45deg, #667eea, #764ba2);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2em;
        font-weight: bold;
    }
    
    .game-progress {
        height: 10px;
        background: #e9ecef;
        border-radius: 5px;
        margin: 20px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(45deg, #FF6B00, #FF8E53);
        transition: width 0.5s;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Inicializar estado de sesión - CORREGIDO
def init_session_state():
    """Inicializar todas las variables de estado de sesión - VERSIÓN CORREGIDA"""
    # Estado de autenticación
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    # Estado del juego
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 1
    if 'timer_started' not in st.session_state:
        st.session_state.timer_started = False
    if 'timer_start_time' not in st.session_state:
        st.session_state.timer_start_time = None
    if 'timer_duration' not in st.session_state:
        st.session_state.timer_duration = 900
    
    # Estado de roles - CORREGIDO: Inicializar como diccionario vacío
    if 'roles' not in st.session_state:
        st.session_state.roles = {}
    if 'roles_assigned' not in st.session_state:
        st.session_state.roles_assigned = False
    if 'roles_revealed' not in st.session_state:  # Nueva variable
        st.session_state.roles_revealed = False
    
    # Estado de ladrón y cómplice
    if 'thief' not in st.session_state:
        st.session_state.thief = None
    if 'accomplice' not in st.session_state:
        st.session_state.accomplice = None
    
    # Estado de juego
    if 'accusations' not in st.session_state:
        st.session_state.accusations = {}
    if 'votes' not in st.session_state:
        st.session_state.votes = {}
    if 'evidence_found' not in st.session_state:
        st.session_state.evidence_found = {}
    if 'coartadas' not in st.session_state:
        st.session_state.coartadas = {}
    if 'current_object' not in st.session_state:
        st.session_state.current_object = None
    if 'thief_assigned' not in st.session_state:
        st.session_state.thief_assigned = False
    if 'accomplice_assigned' not in st.session_state:
        st.session_state.accomplice_assigned = False
    if 'show_twist' not in st.session_state:
        st.session_state.show_twist = False
    if 'voting_open' not in st.session_state:
        st.session_state.voting_open = False
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'game_results' not in st.session_state:
        st.session_state.game_results = None

init_session_state()

# Datos del juego
PLAYERS = {
    "Ingrid": {"avatar": "I", "color": "#FF6B6B"},
    "Evelina": {"avatar": "E", "color": "#4ECDC4"},
    "Tomás": {"avatar": "T", "color": "#45B7D1"},
    "Memo": {"avatar": "M", "color": "#96CEB4"},
    "Cami": {"avatar": "C", "color": "#FFEAA7"},
    "David": {"avatar": "D", "color": "#DDA0DD"},
    "Vivi": {"avatar": "V", "color": "#98D8C8"},
    "Aleja": {"avatar": "🎭", "color": "#F7DC6F", "is_narrator": True}
}

ROLES = [
    {
        "icon": "🕵️",
        "title": "INVESTIGADOR PRINCIPAL",
        "description": "Haces preguntas directas y ordenas turnos.",
        "mission": "• Dirige la investigación\n• Ordena los turnos de habla\n• Formula preguntas clave"
    },
    {
        "icon": "🧠", 
        "title": "ANALISTA LÓGICO",
        "description": "Buscas contradicciones y patrones.",
        "mission": "• Encuentra incoherencias\n• Analiza patrones\n• Conecta pistas"
    },
    {
        "icon": "👀",
        "title": "OBSERVADOR",
        "description": "Te fijas en detalles, silencios y cambios de versión.",
        "mission": "• Nota cambios en historias\n• Observa lenguaje corporal\n• Detecta silencios sospechosos"
    },
    {
        "icon": "🗣️",
        "title": "PORTAVOZ",
        "description": "Resumes teorías del grupo.",
        "mission": "• Sintetiza teorías\n• Resume discusiones\n• Clarifica conclusiones"
    },
    {
        "icon": "📚",
        "title": "ARCHIVISTA",
        "description": "Guardas pistas y lees lo que ya se sabe.",
        "mission": "• Registra todas las pistas\n• Lleva notas de coartadas\n• Organiza la información"
    },
    {
        "icon": "🤔",
        "title": "ESCÉPTICO",
        "description": "Dudas de todo, incluso de lo obvio.",
        "mission": "• Cuestiona todo\n• Busca ángulos alternativos\n• Propone teorías contrarias"
    },
    {
        "icon": "🧩",
        "title": "PERFILADOR",
        "description": "Analizas comportamientos y coartadas.",
        "mission": "• Analiza comportamientos\n• Evalúa coartadas\n• Crea perfiles psicológicos"
    }
]

OBJECTS = [
    {"name": "⌚ Reloj de Año Nuevo", "icon": "⌚", "description": "Un reloj que marca la cuenta regresiva"},
    {"name": "🥂 Copa de Champán", "icon": "🥂", "description": "La copa para el brindis de medianoche"},
    {"name": "🍾 Botella Especial", "icon": "🍾", "description": "Botella reservada para la celebración"},
    {"name": "🔔 Campanilla Dorada", "icon": "🔔", "description": "Campana para anunciar el año nuevo"}
]

EVIDENCE = [
    {"id": 1, "text": "📼 El objeto fue visto por última vez cerca de las 10:40 pm.", "is_real": True, "location": "Sala principal"},
    {"id": 2, "text": "👥 Dos personas coincidieron en un mismo lugar… pero no al mismo tiempo.", "is_real": True, "location": "Pasillo"},
    {"id": 3, "text": "🤥 Alguien mintió sobre lo que vio, no sobre dónde estaba.", "is_real": True, "location": "Biblioteca"},
    {"id": 4, "text": "❌ El Año Nuevo nunca salió de la mesa principal.", "is_real": False, "location": "Comedor"},
    {"id": 5, "text": "🚶 Solo una persona se movió por la casa esa noche.", "is_real": False, "location": "Escaleras"}
]

PHASES = [
    {"id": 1, "title": "🎭 Preparación", "duration": 10, "description": "Asignación de roles y preparación del juego"},
    {"id": 2, "title": "🗣️ Coartadas", "duration": 15, "description": "Cada jugador da su versión de los hechos"},
    {"id": 3, "title": "🔍 Búsqueda de Pistas", "duration": 15, "description": "Exploración y recolección de evidencia"},
    {"id": 4, "title": "🧠 Análisis", "duration": 20, "description": "Discusión y formación de teorías"},
    {"id": 5, "title": "🌀 Giro Especial", "duration": 5, "description": "Nueva información revelada"},
    {"id": 6, "title": "🗳️ Votación", "duration": 10, "description": "Acusaciones y votación final"}
]

# Funciones de utilidad - CORREGIDAS
def assign_roles():
    """Asignar roles aleatoriamente a los jugadores - VERSIÓN CORREGIDA"""
    try:
        regular_players = [p for p in PLAYERS.keys() if p != "Aleja"]
        if len(regular_players) < 7:
            st.error("No hay suficientes jugadores para asignar roles")
            return False
            
        random.shuffle(regular_players)
        
        # Seleccionar ladrón y cómplice
        thief = random.choice(regular_players)
        regular_players.remove(thief)
        accomplice = random.choice(regular_players)
        regular_players.remove(accomplice)
        
        # Asignar roles restantes
        available_roles = ROLES.copy()
        random.shuffle(available_roles)
        
        # Limpiar roles anteriores
        st.session_state.roles = {}
        
        # Asignar rol a Aleja
        st.session_state.roles["Aleja"] = {
            "role": "🎭 NARRADORA / JUEZA",
            "description": "Diriges el juego, conoces los secretos",
            "is_special": True,
            "secret": "Tú conoces toda la verdad del caso"
        }
        
        # Asignar rol al ladrón
        st.session_state.roles[thief] = {
            "role": "🟥 LADRÓN SECRETO",
            "description": "Tú robaste el Año Nuevo. ¡No dejes que te descubran!",
            "is_special": True,
            "secret": """🔴 TARJETA DEL LADRÓN:
• Tú robaste el Año Nuevo
• Sabes dónde está escondido
• Debes mentir con calma
• No puedes acusar directamente a tu cómplice
• Tu misión: convencer a todos de tu inocencia"""
        }
        
        # Asignar rol al cómplice
        st.session_state.roles[accomplice] = {
            "role": "🟧 CÓMPLICE SECRETO",
            "description": "Ayudaste al ladrón. Tu coartada es real pero incompleta.",
            "is_special": True,
            "secret": """🟠 TARJETA DEL CÓMPLICE:
• Ayudaste al ladrón sin saber dónde escondió el objeto
• Tu coartada es real, pero incompleta
• Si te acusan, muestra duda
• Tu misión: proteger al ladrón sin parecer sospechoso"""
        }
        
        # Asignar roles normales a los demás
        for i, player in enumerate(regular_players):
            role_idx = i % len(available_roles)
            st.session_state.roles[player] = {
                "role": available_roles[role_idx]["icon"] + " " + available_roles[role_idx]["title"],
                "description": available_roles[role_idx]["description"],
                "mission": available_roles[role_idx]["mission"],
                "is_special": False
            }
        
        # Guardar ladrón y cómplice en variables separadas
        st.session_state.thief = thief
        st.session_state.accomplice = accomplice
        
        # Seleccionar objeto si no hay
        if not st.session_state.current_object:
            st.session_state.current_object = random.choice(OBJECTS)
        
        # Marcar como asignado
        st.session_state.roles_assigned = True
        st.session_state.roles_revealed = False  # Los roles aún no se revelan a los jugadores
        
        st.success("✅ Roles asignados correctamente!")
        return True
        
    except Exception as e:
        st.error(f"Error al asignar roles: {e}")
        return False

def start_timer(duration_minutes):
    """Iniciar temporizador"""
    st.session_state.timer_started = True
    st.session_state.timer_start_time = time.time()
    st.session_state.timer_duration = duration_minutes * 60

def get_remaining_time():
    """Obtener tiempo restante del temporizador"""
    if not st.session_state.timer_started or not st.session_state.timer_start_time:
        return 0, 0
    
    elapsed = time.time() - st.session_state.timer_start_time
    remaining = max(0, st.session_state.timer_duration - elapsed)
    
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    
    return minutes, seconds

def format_time(minutes, seconds):
    """Formatear tiempo en formato MM:SS"""
    return f"{minutes:02d}:{seconds:02d}"

# Página de inicio de sesión
def login_page():
    """Mostrar página de inicio de sesión"""
    st.markdown("""
    <div class="login-container">
        <h1 style="text-align: center; color: #FF6B00; margin-bottom: 30px;">🎭 EL ROBO DEL AÑO NUEVO</h1>
        <p style="text-align: center; color: #666; margin-bottom: 40px;">
            Un juego de misterio interactivo<br>
            <small>8 jugadores, 1 objeto robado, muchos secretos</small>
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_player = st.selectbox(
            "👤 ¿Quién eres?",
            list(PLAYERS.keys()),
            key="player_select"
        )
        
        if st.button("🎮 ENTRAR AL JUEGO", use_container_width=True, type="primary"):
            st.session_state.logged_in = True
            st.session_state.current_user = selected_player
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Mostrar avatares de todos los jugadores
    st.markdown("<h3 style='text-align: center; color: white; margin-top: 50px;'>👥 JUGADORES</h3>", unsafe_allow_html=True)
    
    cols = st.columns(len(PLAYERS))
    for idx, (player, info) in enumerate(PLAYERS.items()):
        with cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px;">
                <div class="player-avatar" style="background: {info['color']};">
                    {info['avatar']}
                </div>
                <p style="color: white; margin-top: 10px; font-weight: bold;">{player}</p>
            </div>
            """, unsafe_allow_html=True)

# Panel principal del juego
def main_game():
    """Mostrar el juego principal"""
    user = st.session_state.current_user
    player_info = PLAYERS[user]
    
    # Barra lateral con información del jugador - CORREGIDA
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <div class="player-avatar" style="background: {player_info['color']}; width: 100px; height: 100px;">
                {player_info['avatar']}
            </div>
            <h2 style="color: white; margin-top: 10px;">{user}</h2>
            <p style="color: #ddd;">
                {st.session_state.roles.get(user, {}).get('role', 'Esperando asignación...') if st.session_state.roles_assigned and st.session_state.roles_revealed else 'Esperando asignación...'}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Progreso del juego
        progress = (st.session_state.current_phase - 1) / (len(PHASES) - 1) * 100 if len(PHASES) > 1 else 0
        st.markdown(f"""
        <div style="color: white;">
            <p><strong>Fase actual:</strong> {st.session_state.current_phase}/6</p>
            <div class="game-progress">
                <div class="progress-bar" style="width: {progress}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Botones de navegación (solo para la narradora)
        if user == "Aleja":
            st.markdown("### 🎭 Controles de Narradora")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Fase Anterior", use_container_width=True, disabled=st.session_state.current_phase <= 1):
                    st.session_state.current_phase = max(1, st.session_state.current_phase - 1)
                    st.rerun()
            with col2:
                if st.button("➡️ Siguiente Fase", use_container_width=True, disabled=st.session_state.current_phase >= len(PHASES)):
                    st.session_state.current_phase = min(len(PHASES), st.session_state.current_phase + 1)
                    st.rerun()
            
            if st.button("🔄 Reiniciar Juego", type="secondary", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                init_session_state()
                st.rerun()
        
        st.markdown("---")
        
        # Lista de jugadores conectados
        st.markdown("### 👥 Jugadores")
        for player in PLAYERS:
            status = "🟢" if player == user else "🟡"
            role_display = ""
            if st.session_state.roles_assigned and st.session_state.roles_revealed and player in st.session_state.roles:
                role_name = st.session_state.roles[player]["role"].split()[-1]
                if "LADRÓN" in st.session_state.roles[player]["role"]:
                    role_display = " 🟥"
                elif "CÓMPLICE" in st.session_state.roles[player]["role"]:
                    role_display = " 🟧"
                elif "NARRADORA" in st.session_state.roles[player]["role"]:
                    role_display = " 🎭"
                else:
                    role_display = f" {role_name[:3]}"
            st.markdown(f"{status} {player}{role_display}")
    
    # Contenido principal basado en la fase actual
    current_phase = PHASES[st.session_state.current_phase - 1] if 1 <= st.session_state.current_phase <= len(PHASES) else PHASES[0]
    
    # Mostrar temporizador si está activo
    if st.session_state.timer_started:
        mins, secs = get_remaining_time()
        if mins == 0 and secs == 0:
            st.session_state.timer_started = False
        
        st.markdown(f"""
        <div class="timer-container">
            <h2>⏰ TEMPORIZADOR</h2>
            <h1 style="font-size: 3em; margin: 10px 0;">{format_time(mins, secs)}</h1>
            <p>{current_phase['title']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Contenido específico de cada fase
    if st.session_state.current_phase == 1:
        show_phase_1(user)
    elif st.session_state.current_phase == 2:
        show_phase_2(user)
    elif st.session_state.current_phase == 3:
        show_phase_3(user)
    elif st.session_state.current_phase == 4:
        show_phase_4(user)
    elif st.session_state.current_phase == 5:
        show_phase_5(user)
    elif st.session_state.current_phase == 6:
        show_phase_6(user)

# Funciones para cada fase - CORREGIDAS
def show_phase_1(user):
    """Mostrar fase 1: Preparación - VERSIÓN CORREGIDA"""
    st.markdown(f'<h1 class="main-header">{PHASES[0]["title"]}</h1>', unsafe_allow_html=True)
    
    if user == "Aleja":
        # Vista de la narradora - CORREGIDA
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 PREPARACIÓN DEL JUEGO")
            
            if not st.session_state.roles_assigned:
                if st.button("🎲 ASIGNAR ROLES ALEATORIAMENTE", use_container_width=True, type="primary"):
                    if assign_roles():
                        st.rerun()
            else:
                st.success("✅ Roles ya asignados")
                
                # Mostrar información de roles asignados
                st.markdown("### 👤 ROLES ASIGNADOS")
                
                # Crear lista de jugadores sin Aleja
                other_players = [p for p in PLAYERS.keys() if p != "Aleja"]
                
                for player in other_players:
                    role_info = st.session_state.roles.get(player, {})
                    if role_info:
                        role_name = role_info.get("role", "Sin asignar")
                        if "LADRÓN" in role_name:
                            badge_color = "#FF0000"
                            badge_text = " (LADRÓN)"
                        elif "CÓMPLICE" in role_name:
                            badge_color = "#FF8C00"
                            badge_text = " (CÓMPLICE)"
                        else:
                            badge_color = player_info["color"]
                            badge_text = ""
                        
                        st.markdown(f"""
                        <div style="background: {badge_color}; color: white; padding: 10px; 
                                   border-radius: 10px; margin: 5px 0; display: flex; 
                                   justify-content: space-between; align-items: center;">
                            <span><strong>{player}</strong>{badge_text}</span>
                            <span>{role_name.split()[-1] if ' ' in role_name else role_name}</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Selección del objeto robado
                st.markdown("---")
                st.markdown("### 🎯 SELECCIÓN DEL OBJETO ROBADO")
                
                object_names = [obj["name"] for obj in OBJECTS]
                
                # Obtener índice actual
                if st.session_state.current_object:
                    current_index = object_names.index(st.session_state.current_object["name"])
                else:
                    current_index = 0
                
                selected_name = st.selectbox(
                    "Elige el objeto que será robado:",
                    object_names,
                    index=current_index,
                    key="object_select"
                )
                
                # Actualizar objeto seleccionado
                if selected_name:
                    selected_object = next(obj for obj in OBJECTS if obj["name"] == selected_name)
                    st.session_state.current_object = selected_object
                    
                    st.markdown(f"""
                    <div class="phase-card">
                        <h3>🎯 OBJETO ROBADO SELECCIONADO</h3>
                        <h2 style="color: #FF6B00;">{selected_object['icon']} {selected_object['name']}</h2>
                        <p>{selected_object['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Botón para revelar roles a jugadores
                st.markdown("---")
                if not st.session_state.roles_revealed:
                    if st.button("🔓 REVELAR ROLES A JUGADORES", use_container_width=True, type="primary"):
                        st.session_state.roles_revealed = True
                        st.session_state.game_started = True
                        st.success("✅ Roles revelados a los jugadores!")
                        st.rerun()
                else:
                    st.success("✅ Los roles ya han sido revelados a los jugadores")
        
        with col2:
            st.markdown("### 📝 INFORMACIÓN PARA LA NARRADORA")
            
            # Mostrar información secreta si los roles están asignados
            if st.session_state.roles_assigned:
                st.markdown(f"""
                <div class="secret-role-card">
                    <h3>🤫 INFORMACIÓN SECRETA</h3>
                    <p><strong>Ladrón:</strong> {st.session_state.thief}</p>
                    <p><strong>Cómplice:</strong> {st.session_state.accomplice}</p>
                    <p><strong>Objeto robado:</strong> {st.session_state.current_object['name'] if st.session_state.current_object else 'No seleccionado'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Instrucciones para la narradora
                st.markdown("""
                <div class="phase-card">
                    <h4>🎭 TUS RESPONSABILIDADES:</h4>
                    <ul>
                        <li>Dirigir el flujo del juego</li>
                        <li>Controlar los tiempos</li>
                        <li>Preparar el objeto físicamente</li>
                        <li>Esconder las pistas</li>
                        <li>Revelar información gradualmente</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Vista de jugadores normales - CORREGIDA
        if st.session_state.roles_assigned and st.session_state.roles_revealed and user in st.session_state.roles:
            role_info = st.session_state.roles[user]
            
            if role_info.get('is_special', False):
                # Mostrar tarjeta secreta para roles especiales
                st.markdown(f"""
                <div class="secret-role-card">
                    <h2>🤫 TU ROL SECRETO</h2>
                    <h1>{role_info['role']}</h1>
                    <p style="font-size: 1.2em;">{role_info['description']}</p>
                    <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin-top: 20px;">
                        <h3>📜 MISIÓN SECRETA:</h3>
                        <p style="white-space: pre-line;">{role_info.get('secret', '')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Mostrar rol normal
                st.markdown(f"""
                <div class="player-card">
                    <h2>🎭 TU ROL EN EL JUEGO</h2>
                    <h1>{role_info['role']}</h1>
                    <p style="font-size: 1.2em;">{role_info['description']}</p>
                    <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; margin-top: 20px;">
                        <h3>🎯 TU MISIÓN:</h3>
                        <p style="white-space: pre-line;">{role_info.get('mission', '')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Instrucciones para el jugador
            st.markdown("""
            <div class="phase-card">
                <h3>📋 CÓMO JUGAR:</h3>
                <ul style="font-size: 1.1em;">
                    <li><strong>🎭 Mantén tu rol en secreto</strong></li>
                    <li><strong>🗣️ Prepara tu coartada</strong> para la siguiente fase</li>
                    <li><strong>🔍 Busca pistas</strong> y observa a los demás jugadores</li>
                    <li><strong>🤔 Analiza contradicciones</strong> en las historias</li>
                    <li><strong>🎯 Descubre al ladrón y cómplice</strong></li>
                </ul>
                
                <h3>⏰ PRÓXIMA FASE:</h3>
                <p><strong>Coartadas</strong> - Cada jugador contará dónde estaba y qué vio entre las 10:30 y 11:00 PM.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Mostrar objeto robado si ya fue seleccionado
            if st.session_state.current_object:
                st.markdown(f"""
                <div class="phase-card">
                    <h3>🎯 EL OBJETO ROBADO</h3>
                    <p>Alguien ha robado el <strong>{st.session_state.current_object['name']}</strong>.</p>
                    <p><em>{st.session_state.current_object['description']}</em></p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            # Mensaje de espera
            st.markdown("""
            <div class="phase-card">
                <h2>⏳ ESPERANDO CONFIGURACIÓN</h2>
                <p style="font-size: 1.2em;">La narradora está configurando el juego y asignando los roles.</p>
                <p>Por favor, espera a que los roles sean revelados.</p>
                <div style="text-align: center; margin-top: 30px;">
                    <div class="player-avatar" style="background: #F7DC6F; margin: 0 auto;">
                        🎭
                    </div>
                    <p><strong>Aleja</strong> está preparando todo...</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Resto de las funciones de fase (sin cambios significativos)
def show_phase_2(user):
    """Mostrar fase 2: Coartadas"""
    st.markdown(f'<h1 class="main-header">{PHASES[1]["title"]}</h1>', unsafe_allow_html=True)
    
    # Solo Aleja puede iniciar el temporizador
    if user == "Aleja" and not st.session_state.timer_started:
        if st.button("⏱️ INICIAR TEMPORIZADOR (15 min)", use_container_width=True, type="primary"):
            start_timer(15)
            st.rerun()
    
    st.markdown(f"""
    <div class="phase-card">
        <h2>🗣️ FASE DE COARTADAS</h2>
        <p style="font-size: 1.2em;">Cada jugador debe dar su versión de los hechos entre las 10:30 y 11:00 PM</p>
        <p><strong>Tiempo:</strong> 15 minutos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulario para coartada
    with st.form(f"coartada_{user}", clear_on_submit=True):
        st.markdown("### 📝 TU COARTADA")
        
        ubicacion = st.text_area(
            "📍 ¿Dónde estabas entre 10:30 y 11:00 PM?",
            placeholder="Ej: En la sala principal, cerca del árbol de navidad...",
            height=100
        )
        
        viste = st.text_area(
            "👀 ¿Qué viste durante ese tiempo?",
            placeholder="Ej: Vi a Memo saliendo hacia la cocina...",
            height=150
        )
        
        personas = st.multiselect(
            "👥 ¿A quién recuerdas cerca?",
            [p for p in PLAYERS.keys() if p != user],
            help="Puedes seleccionar múltiples personas"
        )
        
        submitted = st.form_submit_button("✅ GUARDAR MI COARTADA", use_container_width=True, type="primary")
        
        if submitted:
            if ubicacion and viste:
                st.session_state.coartadas[user] = {
                    "ubicacion": ubicacion,
                    "viste": viste,
                    "personas": personas,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                st.success("✅ Coartada guardada exitosamente!")
            else:
                st.error("❌ Por favor completa al menos la ubicación y lo que viste")
    
    # Mostrar coartadas de otros jugadores (si la narradora lo permite)
    if user == "Aleja" and st.session_state.coartadas:
        st.markdown("---")
        st.markdown("### 📋 COARTADAS REGISTRADAS")
        
        for player, coartada in st.session_state.coartadas.items():
            with st.expander(f"📝 Coartada de {player}", expanded=False):
                st.markdown(f"""
                **📍 Ubicación:** {coartada['ubicacion']}
                
                **👀 Lo que vio:** {coartada['viste']}
                
                **👥 Personas cerca:** {', '.join(coartada['personas']) if coartada['personas'] else 'No recuerda a nadie'}
                
                *Registrado a las {coartada['timestamp']}*
                """)

# Las funciones show_phase_3, show_phase_4, show_phase_5, show_phase_6 permanecen similares
# Solo muestro show_phase_3 como ejemplo, las otras siguen la misma estructura

def show_phase_3(user):
    """Mostrar fase 3: Búsqueda de pistas"""
    st.markdown(f'<h1 class="main-header">{PHASES[2]["title"]}</h1>', unsafe_allow_html=True)
    
    if user == "Aleja" and not st.session_state.timer_started:
        if st.button("⏱️ INICIAR TEMPORIZADOR (15 min)", use_container_width=True, type="primary"):
            start_timer(15)
            st.rerun()
    
    st.markdown(f"""
    <div class="phase-card">
        <h2>🔍 BÚSQUEDA DE PISTAS</h2>
        <p style="font-size: 1.2em;">Encuentra las 5 pistas escondidas por la casa</p>
        <p><small>⚠️ Recuerda: 3 pistas son reales, 2 son falsas</small></p>
        <p><strong>Tiempo:</strong> 15 minutos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar pistas encontradas
    if st.session_state.evidence_found:
        st.markdown("### 📜 PISTAS ENCONTRADAS")
        
        cols = st.columns(2)
        for idx, (evidence_id, found_by) in enumerate(st.session_state.evidence_found.items()):
            evidence = next(e for e in EVIDENCE if e["id"] == evidence_id)
            with cols[idx % 2]:
                is_real_color = "#4CAF50" if evidence["is_real"] else "#F44336"
                is_real_text = "✅ REAL" if evidence["is_real"] else "❌ FALSA"
                
                st.markdown(f"""
                <div class="evidence-card">
                    <h4>🔍 Pista #{evidence_id} - {evidence['location']}</h4>
                    <p>{evidence['text']}</p>
                    <p><span style="color: {is_real_color}; font-weight: bold;">{is_real_text}</span></p>
                    <p><small>👤 Encontrada por: {found_by}</small></p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Aún no se han encontrado pistas. Usa el botón de abajo para buscar.")
    
    # Botones para "encontrar" pistas (simulado)
    if user != "Aleja":
        st.markdown("---")
        st.markdown("### 🔎 BUSCAR PISTAS")
        
        # Pistas no encontradas aún
        found_ids = list(st.session_state.evidence_found.keys())
        available_evidence = [e for e in EVIDENCE if e["id"] not in found_ids]
        
        if available_evidence:
            # Seleccionar una pista aleatoria disponible
            evidence = random.choice(available_evidence)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Lugar disponible para buscar:** {evidence['location']}")
            
            with col2:
                if st.button(f"🔍 BUSCAR", use_container_width=True, type="primary"):
                    if 'evidence_found' not in st.session_state:
                        st.session_state.evidence_found = {}
                    
                    st.session_state.evidence_found[evidence["id"]] = user
                    st.success(f"🎉 ¡Encontraste una pista en {evidence['location']}!")
                    st.rerun()
        else:
            st.success("✅ ¡Todas las pistas han sido encontradas!")

# Las otras fases siguen un patrón similar
def show_phase_4(user):
    """Mostrar fase 4: Análisis"""
    st.markdown(f'<h1 class="main-header">{PHASES[3]["title"]}</h1>', unsafe_allow_html=True)
    
    if user == "Aleja" and not st.session_state.timer_started:
        if st.button("⏱️ INICIAR TEMPORIZADOR (20 min)", use_container_width=True, type="primary"):
            start_timer(20)
            st.rerun()
    
    st.markdown(f"""
    <div class="phase-card">
        <h2>🧠 FASE DE ANÁLISIS</h2>
        <p style="font-size: 1.2em;">Discute con el grupo y forma teorías sobre el robo</p>
        <p><strong>Tiempo:</strong> 20 minutos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Área de discusión
    st.markdown("### 💭 TABLERO DE DISCUSIÓN")
    
    discussion_topics = [
        "🔍 Comparar coartadas y buscar contradicciones",
        "🎯 Identificar pistas falsas (2 de 5 son falsas)",
        "🤔 Formar teorías sobre el robo",
        "👥 Determinar posibles ladrones y cómplices"
    ]
    
    for topic in discussion_topics:
        st.markdown(f"• {topic}")
    
    # Formulario para teorías
    with st.form(f"teoria_{user}", clear_on_submit=True):
        teoria = st.text_area(
            "💡 Tu teoría sobre lo que pasó:",
            placeholder="Ej: Creo que el ladrón actuó con ayuda de alguien que...",
            height=150
        )
        
        sospechoso = st.selectbox(
            "🎯 Tu principal sospechoso:",
            [""] + [p for p in PLAYERS.keys() if p != user]
        )
        
        submitted = st.form_submit_button("📤 COMPARTIR TEORÍA", use_container_width=True, type="primary")
        
        if submitted:
            if teoria:
                st.success("✅ Teoría compartida. Discútela con el grupo!")
            else:
                st.warning("⚠️ Por favor escribe tu teoría antes de compartir")

def show_phase_5(user):
    """Mostrar fase 5: Giro especial"""
    st.markdown(f'<h1 class="main-header">{PHASES[4]["title"]}</h1>', unsafe_allow_html=True)
    
    if not st.session_state.show_twist and user == "Aleja":
        if st.button("🌀 REVELAR GIRO ESPECIAL", use_container_width=True, type="primary"):
            st.session_state.show_twist = True
            st.rerun()
    
    if st.session_state.show_twist:
        st.markdown("""
        <div class="secret-role-card" style="background: linear-gradient(135deg, #8A2387 0%, #E94057 50%, #F27121 100%);">
            <h1 style="text-align: center;">🌀 GIRO ESPECIAL REVELADO</h1>
            <h2 style="text-align: center; font-size: 2.5em;">"EL LADRÓN NO ACTUÓ SOLO"</h2>
            <p style="text-align: center; font-size: 1.5em; margin-top: 30px;">
            Alguien facilitó el robo…<br>
            <strong>sin tocar el objeto.</strong>
            </p>
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 30px;">
                <h3>🎯 ¿QUÉ SIGNIFICA ESTO?</h3>
                <ul style="font-size: 1.2em;">
                    <li>Hay <strong>DOS personas</strong> implicadas</li>
                    <li>El cómplice tiene una <strong>coartada real pero incompleta</strong></li>
                    <li>Busquen a alguien que <strong>cambió su historia</strong></li>
                    <li>Analicen <strong>quién protege a quién</strong></li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("⏳ Esperando a que la narradora revele el giro especial...")

def show_phase_6(user):
    """Mostrar fase 6: Votación"""
    st.markdown(f'<h1 class="main-header">{PHASES[5]["title"]}</h1>', unsafe_allow_html=True)
    
    if user == "Aleja" and not st.session_state.timer_started:
        if st.button("⏱️ INICIAR TEMPORIZADOR (10 min)", use_container_width=True, type="primary"):
            start_timer(10)
            st.session_state.voting_open = True
            st.rerun()
    
    if st.session_state.voting_open:
        st.markdown(f"""
        <div class="vote-card">
            <h2>🗳️ VOTACIÓN FINAL</h2>
            <p style="font-size: 1.2em;">Acusa a quien creas que es el LADRÓN y da tu razón</p>
            <p><small>⚠️ Recuerda: Hay un ladrón 🟥 y un cómplice 🟧</small></p>
            <p><strong>Tiempo:</strong> 10 minutos</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Formulario de votación
        with st.form(f"voto_{user}", clear_on_submit=True):
            acusado = st.selectbox(
                "🎯 Acuso a:",
                [p for p in PLAYERS.keys() if p != user]
            )
            
            razon = st.text_area(
                "📝 Mi razón lógica:",
                placeholder="Basándome en las pistas y coartadas, creo que es el ladrón porque...",
                height=150
            )
            
            submitted = st.form_submit_button("✅ ENVIAR MI VOTO", use_container_width=True, type="primary")
            
            if submitted:
                if acusado and razon:
                    st.session_state.votes[user] = {
                        "acusado": acusado,
                        "razon": razon,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }
                    st.success("✅ Voto registrado exitosamente!")
                else:
                    st.error("❌ Por favor selecciona un acusado y escribe tu razón")
        
        # Mostrar resultados de votación (solo narradora)
        if user == "Aleja" and st.session_state.votes:
            st.markdown("---")
            st.markdown("### 📊 RESULTADOS PARCIALES")
            
            # Contar votos
            conteo = {}
            for voto in st.session_state.votes.values():
                acusado = voto["acusado"]
                conteo[acusado] = conteo.get(acusado, 0) + 1
            
            # Mostrar conteo
            if conteo:
                total_votes = len(st.session_state.votes)
                for acusado, votos in sorted(conteo.items(), key=lambda x: x[1], reverse=True):
                    porcentaje = (votos / total_votes) * 100 if total_votes > 0 else 0
                    st.markdown(f"**{acusado}**: {votos} voto(s) ({porcentaje:.1f}%)")
                    st.progress(porcentaje / 100)
                
                # Botón para finalizar votación
                if total_votes >= len([p for p in PLAYERS if p != "Aleja"]):
                    if st.button("🏁 FINALIZAR VOTACIÓN Y REVELAR RESULTADOS", use_container_width=True, type="primary"):
                        reveal_results()
    else:
        st.info("⏳ Esperando a que la narradora abra la votación...")

def reveal_results():
    """Revelar resultados finales del juego"""
    st.session_state.game_over = True
    
    # Calcular puntajes
    puntajes = {}
    for jugador in PLAYERS:
        puntajes[jugador] = 0
    
    # Asignar puntos por votos correctos
    for votante, voto in st.session_state.votes.items():
        if voto["acusado"] == st.session_state.thief:
            puntajes[votante] += 3  # 3 puntos por acertar al ladrón
        elif voto["acusado"] == st.session_state.accomplice:
            puntajes[votante] += 2  # 2 puntos por acertar al cómplice
    
    # Puntos especiales
    puntajes[st.session_state.thief] += 5  # Ladrón gana puntos si no lo descubren
    puntajes[st.session_state.accomplice] += 3  # Cómplice gana puntos si no lo descubren
    
    st.session_state.game_results = {
        "thief": st.session_state.thief,
        "accomplice": st.session_state.accomplice,
        "scores": puntajes,
        "winner": max(puntajes, key=puntajes.get)
    }

# Mostrar resultados finales
def show_results():
    """Mostrar resultados finales del juego"""
    if not st.session_state.game_over or not st.session_state.game_results:
        return
    
    results = st.session_state.game_results
    
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: rgba(0,0,0,0.8); border-radius: 20px;">
        <h1 style="color: gold; font-size: 4em;">🏆 JUEGO TERMINADO</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="secret-role-card">
            <h2>🟥 EL LADRÓN ERA...</h2>
            <h1 style="font-size: 3em;">{results['thief']}</h1>
            <p>Rol: {st.session_state.roles.get(results['thief'], {}).get('role', 'Desconocido')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="secret-role-card">
            <h2>🟧 EL CÓMPLICE ERA...</h2>
            <h1 style="font-size: 3em;">{results['accomplice']}</h1>
            <p>Rol: {st.session_state.roles.get(results['accomplice'], {}).get('role', 'Desconocido')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabla de puntajes
    st.markdown("### 📊 PUNTAJES FINALES")
    
    sorted_scores = sorted(results['scores'].items(), key=lambda x: x[1], reverse=True)
    
    for idx, (jugador, puntos) in enumerate(sorted_scores, 1):
        emoji = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "🎯"
        st.markdown(f"""
        <div class="player-card" style="background: {'gold' if idx == 1 else 'silver' if idx == 2 else '#CD7F32' if idx == 3 else '#667eea'}">
            <h3>{emoji} {idx}. {jugador}: {puntos} puntos</h3>
            <p>Rol: {st.session_state.roles.get(jugador, {}).get('role', 'Desconocido')}</p>
            {f"<p>🎉 ¡GANADOR DEL JUEGO!</p>" if jugador == results['winner'] else ""}
        </div>
        """, unsafe_allow_html=True)
    
    # Botón para nuevo juego
    if st.button("🔄 JUGAR DE NUEVO", use_container_width=True, type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_session_state()
        st.rerun()

# Página principal
def main():
    """Función principal de la aplicación"""
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.game_over:
            show_results()
        else:
            main_game()
            
            # Botón para cerrar sesión
            if st.sidebar.button("🚪 CERRAR SESIÓN", type="secondary", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.rerun()

if __name__ == "__main__":
    main()
