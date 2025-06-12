import streamlit as st
import pandas as pd

# Configuración general
st.set_page_config(page_title="Calculadora de Costos del Agente IA", layout="centered")
st.title("🧠 Calculadora de Costos Mensuales del Agente IA")

st.markdown("""
Ajusta los valores según el uso mensual estimado para calcular los costos de operación. 
Ideal para definir cuánto deberías cobrar a tus clientes.
""")

# Tasa de cambio
st.header("💱 Tasa de cambio")
tasa_cop = st.number_input("Tasa actual USD a COP", value=4100.0, step=1.0)

# 1. OpenAI (texto)
st.header("1. OpenAI (GPT-4 o GPT-3.5)")
modelo = st.selectbox("Modelo", ["GPT-3.5-turbo", "GPT-4"])

tokens_entrada = st.slider("Tokens de entrada por mes (en miles)", 0, 2000, 500)
tokens_salida = st.slider("Tokens de salida por mes (en miles)", 0, 2000, 500)

# Conversión de tokens a mensajes aproximados
mensajes_aprox_entrada = int((tokens_entrada * 1000) / 12)
mensajes_aprox_salida = int((tokens_salida * 1000) / 25)

st.markdown(f"🔹 Aproximadamente **{mensajes_aprox_entrada:,} mensajes de entrada** por mes.")
st.markdown(f"🔹 Aproximadamente **{mensajes_aprox_salida:,} mensajes de salida** generados por la IA.")

if modelo == "GPT-3.5-turbo":
    costo_entrada = tokens_entrada * 0.0015
    costo_salida = tokens_salida * 0.002
else:
    costo_entrada = tokens_entrada * 0.03
    costo_salida = tokens_salida * 0.06

costo_openai = costo_entrada + costo_salida

# 2. ElevenLabs (voz)
st.header("2. ElevenLabs (voz IA)")
minutos_audio = st.slider("Minutos de audio generados", 0, 500, 100)
costo_elevenlabs = minutos_audio * 0.30 / 100  # $5 por 100 min

# 3. OpenAI TTS (voz)
st.header("3. OpenAI TTS (voz IA)")
caracteres_voz_openai = st.slider("Caracteres de texto convertidos a voz", 0, 500_000, 100_000)
costo_openai_voice = caracteres_voz_openai * 0.015 / 1000  # $0.015 por 1000 caracteres

# 4. Whisper (transcripción)
st.header("4. Whisper (transcripción de audios)")
minutos_transcripcion = st.slider("Minutos de audio a transcribir", 0, 500, 100)
costo_whisper = minutos_transcripcion * 0.006  # $0.006 por minuto

# 5. Twilio (WhatsApp API)
st.header("5. Twilio (WhatsApp API)")
costo_numero = st.number_input("Costo número al mes", value=5.0)
conversaciones = st.slider("Conversaciones (ventanas de 24h) al mes", 0, 5000, 300)
mensajes_por_conversacion = st.slider("Mensajes promedio por conversación", 1, 100, 10)

costo_conversaciones = conversaciones * 0.0009 
mensajes_totales = conversaciones * mensajes_por_conversacion
costo_mensajes = mensajes_totales * 0.005
costo_twilio = costo_numero + costo_conversaciones + costo_mensajes

# 6. Render
st.header("6. Render (hosting backend)")
costo_render = st.number_input("Costo mensual en Render", value=7.0)

# 7. Base de datos
st.header("7. Base de datos MySQL (ej. Hostinger)")
costo_mysql = st.number_input("Costo mensual base de datos", value=0)

# 8. Extras
st.header("8. Extras opcionales")
costo_extra = st.number_input("Otros costos (email, dominios, almacenamiento...)", value=0)

# Calcular totales
total_usd = (
    costo_openai +
    costo_elevenlabs +
    costo_openai_voice +
    costo_whisper +
    costo_twilio +
    costo_render +
    costo_mysql +
    costo_extra
)
total_cop = total_usd * tasa_cop

# Mostrar resumen
st.subheader("💰 Resumen de costos")
st.metric("Costo mensual total (USD)", f"${total_usd:.2f}")
st.metric("Costo mensual total (COP)", f"${total_cop:,.0f} COP")

# Mostrar desglose
datos = {
    "Concepto": [
        "OpenAI entrada (texto)", 
        "OpenAI salida (texto)", 
        "ElevenLabs (voz)", 
        "OpenAI TTS (voz)", 
        "Whisper (transcripción)", 
        "Twilio número fijo", 
        "Twilio conversaciones (Meta)",
        "Twilio mensajes (Twilio)",
        "Render", 
        "Base de datos", 
        "Otros"
    ],
    "Costo (USD)": [
        round(costo_entrada, 2), 
        round(costo_salida, 2), 
        round(costo_elevenlabs, 2),
        round(costo_openai_voice, 2),
        round(costo_whisper, 2),
        round(costo_numero, 2),
        round(costo_conversaciones, 2),
        round(costo_mensajes, 2),
        round(costo_render, 2),
        round(costo_mysql, 2),
        round(costo_extra, 2)
    ]
}
df = pd.DataFrame(datos)
st.dataframe(df)

# 

st.caption("Calculadora para ayudarte a establecer precios rentables y justos para tu servicio. 🚀")


#✅ Entonces, si pones 20 en ese campo:
# Estás diciendo que el sistema va a procesar 20,000 tokens de entrada al mes.

# Suponiendo que cada mensaje del usuario tiene unos 10-15 tokens (bastante normal), eso equivale a:

# ~1,500 a 2,000 mensajes de entrada al mes.

# Esto puede representar ~60-70 conversaciones largas con múltiples mensajes.

#run dashboard_costos_agente.py