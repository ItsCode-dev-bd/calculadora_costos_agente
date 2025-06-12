import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Configuración general de la app
st.set_page_config(page_title="Calculadora de Costos del Agente IA", layout="centered")
st.title("🧠 Calculadora de Costos Mensuales del Agente IA")

st.markdown("""
Ajusta los valores según el uso mensual estimado para calcular los costos de operación. 
Ideal para definir cuánto deberías cobrar a tus clientes.
""")

st.header("💱 Tasa de cambio")
tasa_cop = st.number_input("Tasa actual USD a COP", value=4000.0, step=1.0)



# 1. OpenAI python -m show xlsxwriter
st.header("1. OpenAI (GPT-4 o GPT-3.5)")
tokens = st.slider("Tokens por mes (en miles)", 50, 2000, 500)
modelo = st.selectbox("Modelo", ["GPT-3.5-turbo ($0.0015 por 1K)", "GPT-4 ($0.03 por 1K)"])
costo_openai = tokens * (0.0015 if "3.5" in modelo else 0.03)

# 2. ElevenLabs (voz)
st.header("2. ElevenLabs (voz IA)")
minutos_audio = st.slider("Minutos de audio generados", 0, 500, 100)
costo_audio = minutos_audio * 0.30 / 100  # 100 minutos por $5

# 3. Whisper (transcripción)
st.header("3. Whisper (transcripción de audios)")
minutos_transcripcion = st.slider("Minutos de audio a transcribir", 0, 500, 100)
costo_whisper = minutos_transcripcion * 0.006 / 1  # $0.006 por minuto

# 4. Twilio
st.header("4. Twilio (número y mensajes)")
costo_numero = 5.00
mensajes = st.slider("Mensajes al mes", 100, 5000, 1000)
costo_mensaje = mensajes * 0.0075
costo_twilio = costo_numero + costo_mensaje

# 5. Render
st.header("5. Render (hosting backend)")
costo_render = st.number_input("Costo mensual en Render", value=7.0)

# 6. Base de datos
st.header("6. Base de datos MySQL (ej. Hostinger)")
costo_mysql = st.number_input("Costo mensual base de datos", value=5.0)

# 7. Extras
st.header("7. Extras opcionales")
costo_extra = st.number_input("Otros costos (email, dominios, almacenamiento...)", value=3.0)

# Calcular total
total_usd = costo_openai + costo_audio + costo_whisper + costo_twilio + costo_render + costo_mysql + costo_extra
total_cop = total_usd * tasa_cop

# Mostrar resultados
st.subheader("💰 Resumen de costos")
st.metric("Costo mensual total (USD)", f"${total_usd:.2f}")
st.metric("Costo mensual total (COP)", f"${total_cop:,.0f} COP")

# Mostrar desglose
datos = {
    "Concepto": [
        "OpenAI (texto)", "ElevenLabs (voz)", "Whisper (transcripción)",
        "Twilio", "Render", "Base de datos", "Otros"
    ],
    "Costo (USD)": [
        round(costo_openai, 2), round(costo_audio, 2), round(costo_whisper, 2),
        round(costo_twilio, 2), round(costo_render, 2), round(costo_mysql, 2), round(costo_extra, 2)
    ]
}
df = pd.DataFrame(datos)
st.dataframe(df)


st.caption("Calculadora para ayudarte a establecer precios rentables y justos para tu servicio. 🚀")



#streamlit run dashboard_costos_agente.py
