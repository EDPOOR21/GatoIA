import streamlit as st
from entorno import Gato
from agente import AgenteQLearning

# Configuración visual de la página y botones grandes
st.set_page_config(page_title="Gato con IA", layout="centered")
st.markdown("""
    <style>
    div.stButton > button { height: 100px; font-size: 32px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 1. INICIALIZAR EL CEREBRO Y EL TABLERO
if 'juego' not in st.session_state:
    st.session_state.juego = Gato()
    
if 'agente' not in st.session_state:
    st.session_state.agente = AgenteQLearning(epsilon=0.1)
    st.session_state.agente.cargar_memoria()
    
if 'estado_previo_ia' not in st.session_state:
    st.session_state.estado_previo_ia = None
    st.session_state.accion_previa_ia = None

if 'mensaje' not in st.session_state:
    st.session_state.mensaje = "Tu turno. Juegas con la X."
if 'juego_terminado' not in st.session_state:
    st.session_state.juego_terminado = False

def reiniciar_juego():
    st.session_state.juego = Gato()
    st.session_state.estado_previo_ia = None
    st.session_state.accion_previa_ia = None
    st.session_state.mensaje = "Nueva partida. ¡Tu turno!"
    st.session_state.juego_terminado = False

# 2. LÓGICA DE APRENDIZAJE EN CADA CLIC
def jugar_turno(posicion):
    juego = st.session_state.juego
    agente = st.session_state.agente
    
    # Turno del humano
    juego.hacer_movimiento(posicion)
    resultado = juego.revisar_ganador()
    
    if resultado is not None:
        st.session_state.juego_terminado = True
        if resultado == 1:
            st.session_state.mensaje = "¡Me ganaste! Acabo de registrar ese error para no repetirlo."
            # Castigo a la IA por perder
            if st.session_state.estado_previo_ia is not None:
                agente.aprender(st.session_state.estado_previo_ia, st.session_state.accion_previa_ia, -1, juego.estado_actual(), [])
        else:
            st.session_state.mensaje = "¡Empate!"
        agente.guardar_memoria()
        return

    # Turno de la IA
    estado_actual = juego.estado_actual()
    acciones_disponibles = juego.movimientos_disponibles()
    
    # La IA no perdió, recompensa neutral por sobrevivir este turno
    if st.session_state.estado_previo_ia is not None:
        agente.aprender(st.session_state.estado_previo_ia, st.session_state.accion_previa_ia, 0, estado_actual, acciones_disponibles)
        
    accion_ia = agente.elegir_accion(estado_actual, acciones_disponibles)
    juego.hacer_movimiento(accion_ia)
    
    st.session_state.estado_previo_ia = juego.estado_actual()
    st.session_state.accion_previa_ia = accion_ia
    
    resultado = juego.revisar_ganador()
    if resultado is not None:
        st.session_state.juego_terminado = True
        if resultado == -1:
            st.session_state.mensaje = "¡Te gané! Reforzando esta estrategia."
            # Premio a la IA por ganar
            agente.aprender(st.session_state.estado_previo_ia, st.session_state.accion_previa_ia, 1, juego.estado_actual(), [])
        else:
            st.session_state.mensaje = "¡Empate!"
        agente.guardar_memoria()

# 3. INTERFAZ GRÁFICA
st.title("Gato Adaptativo")

# Panel lateral para controlar el "defecto" de la IA
with st.sidebar:
    st.header("Ajustes del Motor")
    nuevo_epsilon = st.slider("Tasa de Error (Epsilon)", 0.0, 1.0, st.session_state.agente.epsilon, 0.05, 
                              help="0.0 = Juega perfecto según su memoria. 1.0 = Juega 100% al azar.")
    st.session_state.agente.epsilon = nuevo_epsilon
    st.metric("Estados en Memoria", len(st.session_state.agente.q_table))
    st.caption("Abre el archivo q_table.json en VS Code para ver cómo cambian los pesos matemáticos en vivo.")

st.info(st.session_state.mensaje)

# Renderizar la cuadrícula de 3x3
tablero = st.session_state.juego.tablero
simbolos = {0: " ", 1: "X", -1: "O"}

for fila in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = fila * 3 + col
        deshabilitado = tablero[idx] != 0 or st.session_state.juego_terminado
        
        if cols[col].button(simbolos[tablero[idx]], key=f"btn_{idx}", disabled=deshabilitado, use_container_width=True):
            jugar_turno(idx)
            st.rerun()

if st.session_state.juego_terminado:
    st.button("🔄 Jugar otra vez", on_click=reiniciar_juego, type="primary")