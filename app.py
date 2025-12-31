import streamlit as st
import json
import time
import datetime
import random
from pathlib import Path
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Mensajes Especiales 💖",
    page_icon="💌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ruta del archivo de datos
DATA_FILE = "mensajes_data.json"

# Inicializar datos si no existen
def inicializar_datos():
    if not Path(DATA_FILE).exists():
        datos_iniciales = {
            "mensajes": [],
            "usuarios": {
                "Aleja": {"ultimo_mensaje": None, "total_mensajes": 0},
                "Mimi": {"ultimo_recibido": None, "total_recibidos": 0},
                "Invitado": {"visto": False}
            }
        }
        guardar_datos(datos_iniciales)
    return cargar_datos()

def cargar_datos():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"mensajes": [], "usuarios": {}}

def guardar_datos(datos):
    with open(DATA_FILE, 'w') as f:
        json.dump(datos, f, indent=2)

# Efectos visuales
def mostrar_confeti():
    confeti_html = """
    <style>
    .confeti {
        position: fixed;
        width: 10px;
        height: 10px;
        background-color: #f00;
        top: -10px;
        animation: fall 5s linear infinite;
    }
    
    @keyframes fall {
        to {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
    </style>
    <script>
    // Crear confeti
    for(let i = 0; i < 150; i++) {
        let confeti = document.createElement('div');
        confeti.className = 'confeti';
        confeti.style.left = Math.random() * 100 + 'vw';
        confeti.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 60%)`;
        confeti.style.width = Math.random() * 10 + 5 + 'px';
        confeti.style.height = Math.random() * 10 + 5 + 'px';
        confeti.style.animationDelay = Math.random() * 5 + 's';
        document.body.appendChild(confeti);
        
        // Remover después de la animación
        setTimeout(() => confeti.remove(), 5000);
    }
    </script>
    """
    st.components.v1.html(confeti_html, height=0)

def mostrar_efecto_corazones():
    corazones_html = """
    <style>
    .corazon {
        position: fixed;
        font-size: 20px;
        animation: float 3s ease-in infinite;
        opacity: 0;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }
    }
    </style>
    <script>
    // Crear corazones
    const corazones = ['💖', '💗', '💓', '💞', '💕', '💘', '💝'];
    for(let i = 0; i < 50; i++) {
        let corazon = document.createElement('div');
        corazon.className = 'corazon';
        corazon.innerHTML = corazones[Math.floor(Math.random() * corazones.length)];
        corazon.style.left = Math.random() * 100 + 'vw';
        corazon.style.fontSize = (Math.random() * 30 + 20) + 'px';
        corazon.style.animationDelay = Math.random() * 2 + 's';
        document.body.appendChild(corazon);
        
        // Remover después de la animación
        setTimeout(() => corazon.remove(), 3000);
    }
    </script>
    """
    st.components.v1.html(corazones_html, height=0)

# Función principal
def main():
    # Cargar datos
    datos = inicializar_datos()
    
    # Sidebar para selección de usuario
    with st.sidebar:
        st.image("https://emojicdn.elk.sh/💌", width=100)
        st.title("💝 Selecciona quién eres")
        
        usuario = st.radio(
            "¿Quién está ingresando?",
            ["Aleja", "Mimi", "Invitado"],
            index=2
        )
        
        st.markdown("---")
        st.markdown("### 📊 Estadísticas")
        
        if usuario == "Aleja":
            st.metric("Mensajes enviados", datos["usuarios"].get("Aleja", {}).get("total_mensajes", 0))
        elif usuario == "Mimi":
            st.metric("Mensajes recibidos", datos["usuarios"].get("Mimi", {}).get("total_recibidos", 0))
        
        st.markdown("---")
        st.markdown("### 📜 Historial reciente")
        if datos["mensajes"]:
            for msg in datos["mensajes"][-3:]:
                st.caption(f"⏰ {msg['hora']}")
    
    # Contenido principal según el usuario
    if usuario == "Aleja":
        mostrar_pagina_aleja(datos)
    elif usuario == "Mimi":
        mostrar_pagina_mimi(datos)
    else:
        mostrar_pagina_invitado(datos)

def mostrar_pagina_aleja(datos):
    st.title("💖 Hola Aleja!")
    st.subheader("Envía un mensaje especial a Mimi")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Instrucciones:
        1. Escribe un mensaje personalizado (opcional)
        2. Elige un tipo de mensaje especial
        3. ¡Presiona el botón para enviar amor a Mimi! 💕
        """)
        
        mensaje_personalizado = st.text_area(
            "✨ Mensaje personalizado (opcional):",
            placeholder="Escribe algo especial para Mimi...",
            height=100
        )
        
        tipo_mensaje = st.selectbox(
            "🎁 Tipo de mensaje:",
            ["Te amo", "Eres especial", "Me haces feliz", "Sorpresa de amor", "Mensaje secreto"]
        )
        
        # Botón especial con efecto
        if st.button("💝 ENVIAR MENSAJE DE AMOR A MIMI", type="primary", use_container_width=True):
            # Actualizar datos
            hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            nuevo_mensaje = {
                "de": "Aleja",
                "para": "Mimi",
                "tipo": tipo_mensaje,
                "mensaje": mensaje_personalizado if mensaje_personalizado else tipo_mensaje,
                "hora": hora_actual
            }
            
            datos["mensajes"].append(nuevo_mensaje)
            
            # Actualizar estadísticas
            if "Aleja" not in datos["usuarios"]:
                datos["usuarios"]["Aleja"] = {}
            datos["usuarios"]["Aleja"]["ultimo_mensaje"] = hora_actual
            datos["usuarios"]["Aleja"]["total_mensajes"] = datos["usuarios"]["Aleja"].get("total_mensajes", 0) + 1
            
            if "Mimi" not in datos["usuarios"]:
                datos["usuarios"]["Mimi"] = {}
            datos["usuarios"]["Mimi"]["ultimo_recibido"] = hora_actual
            datos["usuarios"]["Mimi"]["total_recibidos"] = datos["usuarios"]["Mimi"].get("total_recibidos", 0) + 1
            
            guardar_datos(datos)
            
            # Mostrar efectos
            mostrar_confeti()
            mostrar_efecto_corazones()
            
            # Mensaje de éxito
            st.success("✅ ¡Mensaje enviado a Mimi con éxito!")
            st.balloons()
            
            # Auto-refresh después de 2 segundos
            time.sleep(2)
            st.rerun()
    
    with col2:
        st.markdown("### 📈 Tus estadísticas")
        st.metric("Total enviados", datos["usuarios"].get("Aleja", {}).get("total_mensajes", 0))
        
        if datos["usuarios"].get("Aleja", {}).get("ultimo_mensaje"):
            st.metric("Último envío", datos["usuarios"]["Aleja"]["ultimo_mensaje"])
        
        st.markdown("### 💌 Mensajes recientes")
        if datos["mensajes"]:
            for msg in reversed(datos["mensajes"][-5:]):
                if msg["de"] == "Aleja":
                    with st.expander(f"📨 {msg['hora']}"):
                        st.write(f"**Para:** {msg['para']}")
                        st.write(f"**Mensaje:** {msg['mensaje']}")

def mostrar_pagina_mimi(datos):
    st.title("🌸 Hola Mimi!")
    st.subheader("Tienes mensajes especiales esperándote")
    
    # Verificar si hay mensajes nuevos
    ultimo_mensaje = datos["usuarios"].get("Mimi", {}).get("ultimo_recibido")
    mensajes_para_mimi = [m for m in datos["mensajes"] if m["para"] == "Mimi"]
    
    if mensajes_para_mimi:
        # Mostrar el último mensaje de forma especial
        ultimo_msg = mensajes_para_mimi[-1]
        
        # Contenedor especial para el mensaje
        with st.container():
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #ffafcc, #ffc8dd); 
                border-radius: 20px; box-shadow: 0 10px 30px rgba(255, 0, 100, 0.3);">
                    <h1 style="color: #590d22; font-size: 3em;">{ultimo_msg['tipo']} 💕</h1>
                    <p style="font-size: 1.5em; color: #800f2f;">{ultimo_msg['mensaje']}</p>
                    <p style="color: #a4133c;">De: {ultimo_msg['de']}</p>
                    <p style="color: #c9184a;">{ultimo_msg['hora']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Efectos visuales
            mostrar_efecto_corazones()
            st.balloons()
        
        st.markdown("---")
        
        # Historial de mensajes
        st.markdown("### 📜 Historial de mensajes")
        
        for msg in reversed(mensajes_para_mimi):
            with st.expander(f"💌 Mensaje de {msg['de']} - {msg['hora']}"):
                st.write(f"**Tipo:** {msg['tipo']}")
                st.write(f"**Contenido:** {msg['mensaje']}")
                
                # Diferentes colores según el remitente
                if msg['de'] == 'Aleja':
                    st.markdown("💝 **Especial de Aleja**")
    else:
        # No hay mensajes aún
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h2 style="color: #ff758f;">💔 Aún no hay mensajes</h2>
            <p style="font-size: 1.2em;">Espera a que Aleja te envíe un mensaje especial...</p>
            <div style="font-size: 3em; margin: 20px;">💌</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Estadísticas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total recibidos", datos["usuarios"].get("Mimi", {}).get("total_recibidos", 0))
    with col2:
        if ultimo_mensaje:
            st.metric("Último mensaje", ultimo_mensaje)

def mostrar_pagina_invitado(datos):
    st.title("👋 Bienvenido/a")
    st.markdown("""
    ### Esta es una aplicación especial para Aleja y Mimi
    
    **Cómo funciona:**
    1. **Aleja** puede enviar mensajes especiales
    2. **Mimi** recibe los mensajes con efectos visuales
    3. Los mensajes se guardan en un historial
    
    ### 📊 Estadísticas generales
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_mensajes = len(datos["mensajes"])
        st.metric("Total mensajes", total_mensajes)
    
    with col2:
        mensajes_aleja = len([m for m in datos["mensajes"] if m["de"] == "Aleja"])
        st.metric("De Aleja", mensajes_aleja)
    
    with col3:
        mensajes_mimi = len([m for m in datos["mensajes"] if m["para"] == "Mimi"])
        st.metric("Para Mimi", mensajes_mimi)
    
    if datos["mensajes"]:
        st.markdown("### 📨 Últimos mensajes")
        for msg in reversed(datos["mensajes"][-5:]):
            st.info(f"**{msg['de']} → {msg['para']}** ({msg['hora']}): {msg['mensaje'][:50]}...")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Selecciona tu nombre en el menú lateral para continuar</p>
        <p>💝 Creado con amor para Aleja y Mimi 💝</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
