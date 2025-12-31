import streamlit as st
import random
import time
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="El Robo del Año Nuevo",
    page_icon="🎭",
    layout="wide"
)

# Inicializar estado de sesión
if 'paso_actual' not in st.session_state:
    st.session_state.paso_actual = 1
if 'roles_asignados' not in st.session_state:
    st.session_state.roles_asignados = False
if 'acusaciones' not in st.session_state:
    st.session_state.acusaciones = {}
if 'votos' not in st.session_state:
    st.session_state.votos = {}
if 'timer_iniciado' not in st.session_state:
    st.session_state.timer_iniciado = False
if 'inicio_tiempo' not in st.session_state:
    st.session_state.inicio_tiempo = None

# Lista de jugadores
jugadores = ["Ingrid", "Evelina", "Tomás", "Memo", "Cami", "David", "Vivi", "Aleja (YO)"]

# Roles disponibles
roles = [
    "🕵️ INVESTIGADOR PRINCIPAL",
    "🧠 ANALISTA LÓGICO", 
    "👀 OBSERVADOR",
    "🗣️ PORTAVOZ",
    "📚 ARCHIVISTA",
    "🤔 ESCÉPTICO",
    "🧩 PERFILADOR"
]

# Objetos para robar
objetos = ["⌚ reloj", "🥂 copa", "🍾 botella", "🔔 campanita"]

# Pistas
pistas_reales = [
    "📩 PISTA 1 (REAL): El objeto fue visto por última vez cerca de las 10:40 pm.",
    "📩 PISTA 2 (REAL): Dos personas coincidieron en un mismo lugar… pero no al mismo tiempo.",
    "📩 PISTA 3 (REAL): Alguien mintió sobre lo que vio, no sobre dónde estaba."
]

pistas_falsas = [
    "📩 PISTA 4 (FALSA): El Año Nuevo nunca salió de la mesa principal.",
    "📩 PISTA 5 (FALSA): Solo una persona se movió por la casa esa noche."
]

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B00;
        font-size: 3em;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .sub-header {
        color: #2E86C1;
        border-left: 5px solid #FF6B00;
        padding-left: 15px;
        margin-top: 30px;
    }
    .card {
        background-color: #F8F9F9;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .secret-card {
        background-color: #FFE5CC;
        border: 2px dashed #FF6B00;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    .timer {
        font-size: 2em;
        font-weight: bold;
        color: #E74C3C;
        text-align: center;
        padding: 15px;
        background-color: #FDEDEC;
        border-radius: 10px;
        margin: 20px 0;
    }
    .phase-box {
        background-color: #D5F4E6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .stButton button {
        background-color: #FF6B00;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #E85A00;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">🎭 El Robo del Año Nuevo</h1>', unsafe_allow_html=True)

# Barra lateral para navegación
st.sidebar.title("🎮 Navegación del Juego")
st.sidebar.markdown(f"**Paso actual:** {st.session_state.paso_actual}/5")

for i in range(1, 6):
    if st.sidebar.button(f"Paso {i}", key=f"nav_{i}"):
        st.session_state.paso_actual = i
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### Jugadores")
for jugador in jugadores:
    st.sidebar.markdown(f"• {jugador}")

# Función para temporizador
def temporizador(minutos):
    if not st.session_state.timer_iniciado:
        st.session_state.inicio_tiempo = time.time()
        st.session_state.timer_iniciado = True
    
    tiempo_transcurrido = time.time() - st.session_state.inicio_tiempo
    tiempo_restante = max(0, minutos * 60 - tiempo_transcurrido)
    
    minutos_restantes = int(tiempo_restante // 60)
    segundos_restantes = int(tiempo_restante % 60)
    
    return minutos_restantes, segundos_restantes

# Paso 1: Asignación de roles
if st.session_state.paso_actual == 1:
    st.markdown('<h2 class="sub-header">🧾 PASO 1: ASIGNACIÓN DE ROLES</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Instrucciones:
        1. **Aleja (YO)** es la 🎭 NARRADORA/JUEZA
        2. Los otros 7 jugadores reciben un rol cada uno
        3. Imprime o escribe cada rol en un papel
        4. Reparte los roles al azar
        """)
        
        if st.button("🔀 Asignar Roles Aleatoriamente", key="asignar_roles"):
            jugadores_sin_aleja = [j for j in jugadores if j != "Aleja (YO)"]
            random.shuffle(jugadores_sin_aleja)
            random.shuffle(roles)
            
            st.session_state.roles_aleatorios = dict(zip(jugadores_sin_aleja, roles))
            st.session_state.roles_asignados = True
            st.rerun()
        
        if st.session_state.roles_asignados:
            st.markdown("### 📋 Roles Asignados:")
            for jugador, rol in st.session_state.roles_aleatorios.items():
                st.markdown(f'<div class="card">👤 **{jugador}** → {rol}</div>', unsafe_allow_html=True)
            
            if st.button("📄 Imprimir Tarjetas de Rol", key="imprimir_roles"):
                st.info("Imprime estas asignaciones o escríbelas en tarjetas individuales.")
    
    with col2:
        st.markdown("### 📝 Descripción de Roles:")
        for rol in roles:
            with st.expander(f"{rol.split()[1]}"):
                if "INVESTIGADOR" in rol:
                    st.write("Haces preguntas directas y ordenas turnos.")
                elif "ANALISTA" in rol:
                    st.write("Buscas contradicciones y patrones.")
                elif "OBSERVADOR" in rol:
                    st.write("Te fijas en detalles, silencios y cambios de versión.")
                elif "PORTAVOZ" in rol:
                    st.write("Resumes teorías del grupo.")
                elif "ARCHIVISTA" in rol:
                    st.write("Guardas pistas y lees lo que ya se sabe.")
                elif "ESCÉPTICO" in rol:
                    st.write("Dudas de todo, incluso de lo obvio.")
                elif "PERFILADOR" in rol:
                    st.write("Analizas comportamientos y coartadas.")

# Paso 2: Tarjetas secretas
elif st.session_state.paso_actual == 2:
    st.markdown('<h2 class="sub-header">🔐 PASO 2: TARJETAS SECRETAS</h2>', unsafe_allow_html=True)
    
    st.warning("⚠️ **SOLO PARA ALEJA (NARRADORA)** - Estas tarjetas son secretas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="secret-card">', unsafe_allow_html=True)
        st.markdown("### 🟥 TARJETA DEL LADRÓN")
        st.markdown("""
        - Tú robaste el Año Nuevo
        - Sabes dónde está escondido
        - Debes mentir con calma
        - No puedes acusar directamente a tu cómplice
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.info("📝 **Instrucción:** Escribe esto en una tarjeta roja y entrégala doblada al LADRÓN.")
    
    with col2:
        st.markdown('<div class="secret-card">', unsafe_allow_html=True)
        st.markdown("### 🟧 TARJETA DEL CÓMPLICE")
        st.markdown("""
        - Tú ayudaste al ladrón
        - No sabes dónde se escondió el objeto
        - Tu coartada es real, pero incompleta
        - Si te acusan, duda
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.info("📝 **Instrucción:** Escribe esto en una tarjeta naranja y entrégala doblada al CÓMPLICE.")
    
    st.markdown("---")
    
    st.markdown("### 🎯 ELECCIÓN DEL OBJETO ROBADO")
    objeto_elegido = st.selectbox("Elige el objeto 'Año Nuevo' que será robado:", objetos)
    
    if objeto_elegido:
        st.success(f"✅ Objeto seleccionado: **{objeto_elegido}**")
        st.info(f"📌 **Instrucción:** Escóndelo físicamente antes de empezar el juego.")

# Paso 3: Preparación de pistas
elif st.session_state.paso_actual == 3:
    st.markdown('<h2 class="sub-header">🔎 PASO 3: PREPARACIÓN DE PISTAS</h2>', unsafe_allow_html=True)
    
    st.markdown("### 📩 PISTAS REALES (3)")
    for pista in pistas_reales:
        st.markdown(f'<div class="card">{pista}</div>', unsafe_allow_html=True)
    
    st.markdown("### 🎭 PISTAS FALSAS (2)")
    for pista in pistas_falsas:
        st.markdown(f'<div class="card">{pista}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📋 LISTA COMPLETA DE PISTAS")
    
    todas_pistas = pistas_reales + pistas_falsas
    random.shuffle(todas_pistas)
    
    for i, pista in enumerate(todas_pistas, 1):
        st.markdown(f"**Sobre {i}:** {pista}")
    
    st.info("""
    📌 **Instrucciones:**
    1. Escribe cada pista en un sobre numerado (1 al 5)
    2. Mezcla los sobres para que no se sepa cuáles son reales y cuáles falsas
    3. Escóndelos por la casa antes de empezar el juego
    """)

# Paso 4: Desarrollo del juego
elif st.session_state.paso_actual == 4:
    st.markdown('<h2 class="sub-header">🧩 PASO 4: DESARROLLO DEL JUEGO</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["FASE 1 - COARTADAS", "FASE 2 - BÚSQUEDA", "FASE 3 - ANÁLISIS", "🌀 GIRO ESPECIAL"])
    
    with tab1:
        st.markdown('<div class="phase-box">', unsafe_allow_html=True)
        st.markdown("### ⏰ FASE 1 – COARTADAS (15 minutos)")
        
        # Temporizador
        if st.button("⏱️ Iniciar Temporizador 15 min", key="timer_fase1"):
            st.session_state.timer_iniciado = True
            st.session_state.inicio_tiempo = time.time()
        
        if st.session_state.timer_iniciado:
            mins, secs = temporizador(15)
            st.markdown(f'<div class="timer">⏳ Tiempo restante: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 📝 Preguntas para cada jugador:
        1. **¿Dónde estabas entre 10:30 y 11:00?**
        2. **¿Qué viste?**
        3. **¿A quién recuerdas cerca?**
        
        ### 👥 Orden de turnos:
        """)
        
        jugadores_sin_aleja = [j for j in jugadores if j != "Aleja (YO)"]
        for i, jugador in enumerate(jugadores_sin_aleja, 1):
            st.write(f"{i}. {jugador}")
        
        st.markdown("""
        ### 📌 Reglas:
        - No se interrumpe al que habla
        - Todos deben responder las 3 preguntas
        - El Investigador Principal dirige los turnos
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="phase-box">', unsafe_allow_html=True)
        st.markdown("### 🔍 FASE 2 – BÚSQUEDA DE PISTAS (15 minutos)")
        
        if st.button("⏱️ Iniciar Temporizador 15 min", key="timer_fase2"):
            st.session_state.timer_iniciado = True
            st.session_state.inicio_tiempo = time.time()
        
        if st.session_state.timer_iniciado:
            mins, secs = temporizador(15)
            st.markdown(f'<div class="timer">⏳ Tiempo restante: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 🔎 Instrucciones:
        - Los jugadores pueden moverse por la casa (físicamente)
        - Buscan los 5 sobres con pistas
        - Cada sobre encontrado se lleva al Archivista
        - El Archivista guarda y registra todas las pistas encontradas
        
        ### 📚 Rol del Archivista:
        1. Anotar qué pistas se han encontrado
        2. Leer en voz alta cada pista cuando se encuentra
        3. Mantener un registro de todas las pistas
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="phase-box">', unsafe_allow_html=True)
        st.markdown("### 🤔 FASE 3 – ANÁLISIS (20 minutos)")
        
        if st.button("⏱️ Iniciar Temporizador 20 min", key="timer_fase3"):
            st.session_state.timer_iniciado = True
            st.session_state.inicio_tiempo = time.time()
        
        if st.session_state.timer_iniciado:
            mins, secs = temporizador(20)
            st.markdown(f'<div class="timer">⏳ Tiempo restante: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 🧠 Mesa redonda de análisis:
        
        **Temas a discutir:**
        1. Comparar coartadas y buscar contradicciones
        2. Identificar pistas falsas (2 de 5 son falsas)
        3. Formar teorías sobre el robo
        4. Determinar posibles ladrones y cómplices
        
        **Roles en acción:**
        - 🗣️ Portavoz: Resume las teorías del grupo
        - 🧠 Analista Lógico: Busca patrones y contradicciones
        - 🤔 Escéptico: Cuestiona todas las suposiciones
        - 🧩 Perfilador: Analiza comportamientos y coartadas
        - 👀 Observador: Señala detalles y cambios de versión
        
        **🎯 Objetivo:** Llegar a un consenso sobre quiénes son el ladrón y el cómplice
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="phase-box">', unsafe_allow_html=True)
        st.markdown("### 🌀 GIRO ESPECIAL")
        
        if st.button("🎭 Revelar Giro Especial", key="giro"):
            st.markdown("""
            <div class="secret-card">
            <h3>🌀 NUEVA INFORMACIÓN REVELADA:</h3>
            <h2>"El ladrón no actuó solo.</h2>
            <h2>Alguien facilitó el robo… sin tocar el objeto."</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("""
            📢 **Cómo usar este giro:**
            - Léelo en voz alta cuando quieras (puede ser al inicio o durante el análisis)
            - Cambia completamente las dinámicas de sospecha
            - Confirma que hay DOS personas implicadas (ladrón + cómplice)
            """)
        else:
            st.info("Presiona el botón para revelar el giro especial cuando lo desees durante el juego.")
        st.markdown('</div>', unsafe_allow_html=True)

# Paso 5: Acusación final
else:
    st.markdown('<h2 class="sub-header">🗳️ PASO 5: ACUSACIÓN FINAL</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="phase-box">', unsafe_allow_html=True)
    st.markdown("### ⏰ FASE FINAL – VOTACIÓN (10 minutos)")
    
    if st.button("⏱️ Iniciar Temporizador 10 min", key="timer_final"):
        st.session_state.timer_iniciado = True
        st.session_state.inicio_tiempo = time.time()
    
    if st.session_state.timer_iniciado:
        mins, secs = temporizador(10)
        st.markdown(f'<div class="timer">⏳ Tiempo restante: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📝 Instrucciones para cada jugador:
    1. **Acusa a alguien** (puede ser el ladrón o el cómplice)
    2. **Da una razón lógica** basada en las pistas y coartadas
    3. **Vota en secreto** (puede ser con papel o mostrando tarjetas)
    
    ### 🎯 Objetivo final:
    - Descubrir quién es el **LADRÓN** 🟥
    - Descubrir quién es el **CÓMPLICE** 🟧
    - Ganar puntos por acertar cualquiera de los dos
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sistema de votación interactivo
    st.markdown("### 🗳️ REGISTRO DE VOTACIONES (Opcional)")
    
    jugadores_votantes = [j for j in jugadores if j != "Aleja (YO)"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        votante = st.selectbox("Jugador que vota:", jugadores_votantes, key="votante")
        acusado = st.selectbox("A quién acusa:", jugadores_votantes, key="acusado")
        razon = st.text_area("Razón lógica:", key="razon")
        
        if st.button("✅ Registrar Voto", key="registrar_voto"):
            if votante and acusado and razon:
                st.session_state.acusaciones[votante] = {
                    "acusado": acusado,
                    "razon": razon,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                st.success(f"Voto de {votante} registrado contra {acusado}")
                st.rerun()
    
    with col2:
        if st.session_state.acusaciones:
            st.markdown("### 📊 Votos Registrados")
            for votante, datos in st.session_state.acusaciones.items():
                st.markdown(f"""
                <div class="card">
                **{votante}** → 🎯 **{datos['acusado']}**
                <br>📝 *{datos['razon'][:100]}...*
                </div>
                """, unsafe_allow_html=True)
            
            # Contar votos
            if st.session_state.acusaciones:
                conteo = {}
                for datos in st.session_state.acusaciones.values():
                    acusado = datos['acusado']
                    conteo[acusado] = conteo.get(acusado, 0) + 1
                
                if conteo:
                    st.markdown("### 📈 Conteo de Votos")
                    for acusado, votos in sorted(conteo.items(), key=lambda x: x[1], reverse=True):
                        st.progress(min(votos/len(jugadores_votantes), 1.0))
                        st.write(f"**{acusado}**: {votos} voto(s)")
        else:
            st.info("No hay votos registrados aún.")

# Pie de página
st.markdown("---")
st.markdown("🎭 **Desarrollado para Aleja y sus amigos** | *El Robo del Año Nuevo* © 2024")
