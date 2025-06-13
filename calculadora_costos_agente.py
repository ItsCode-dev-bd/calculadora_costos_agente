import streamlit as st
import pandas as pd


from PIL import Image


# Configuración general
st.set_page_config(page_title="Calculadora de Costos del Agente IA", layout="centered")


# logo = Image.open("Logo_ItsCodev7.png")  # Cambia el nombre si tu imagen tiene otro
# st.image(logo, width=150)  # Puedes ajustar el tamaño con el parámetro width

st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://itscode.dev/wp-content/uploads/2025/06/Logo_ItsCodev7.png" alt="Logo" width="200">
    </div>
    """,
    unsafe_allow_html=True
)


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

tokens_entrada = st.slider("Tokens de entrada por mes (en miles)", 0, 2000, 20)
tokens_salida = st.slider("Tokens de salida por mes (en miles)", 0, 2000, 20)

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
minutos_transcripcion = st.slider("Minutos de audio a transcribir", 0, 500, 30)
costo_whisper = minutos_transcripcion * 0.006  # $0.006 por minuto

# 5. WhatsApp API
st.header("5. WhatsApp API")
proveedor_whatsapp = st.radio("Proveedor de WhatsApp API", ["Twilio", "Meta API directa", "360diag (Meta BSP)"])

if proveedor_whatsapp == "Twilio":
    costo_numero = st.number_input("Costo número al mes (Twilio)", value=5.0)
    conversaciones = st.slider("Conversaciones (ventanas de 24h) al mes", 0, 5000, 300)
    mensajes_por_conversacion = st.slider("Mensajes promedio por conversación", 1, 100, 10)

    costo_conversaciones = conversaciones * 0.0009 
    mensajes_totales = conversaciones * mensajes_por_conversacion
    costo_mensajes = mensajes_totales * 0.005
    costo_whatsapp = costo_numero + costo_conversaciones + costo_mensajes

    detalle_wa = [
        round(costo_numero, 2),
        round(costo_conversaciones, 2),
        round(costo_mensajes, 2)
    ]
    conceptos_wa = [
        "Twilio número fijo", 
        "Twilio conversaciones (Meta)", 
        "Twilio mensajes (Twilio)"
    ]

elif proveedor_whatsapp == "Meta API directa":##
    st.markdown("**Nota**: Debes tener un proveedor BSP aprobado para usar la API directa de Meta.")
    costo_numero = st.number_input("Costo número al mes", value=0)    
    conversaciones_autenticacion = st.slider("Conversaciones de Autenticación", 0, 2000, 50)
    conversaciones_utilidad = st.slider("Conversaciones de Utilidad", 0, 2000, 100)
    conversaciones_servicio = st.slider("Conversaciones de Servicio", 0, 2000, 100)
    conversaciones_marketing = st.slider("Conversaciones de Marketing", 0, 2000, 50)

    costo_aut = conversaciones_autenticacion * 0.018
    costo_util = conversaciones_utilidad * 0.014
    costo_serv = conversaciones_servicio * 0.014
    costo_mark = conversaciones_marketing * 0.026

    costo_whatsapp = costo_aut + costo_util + costo_serv + costo_mark + costo_numero

    detalle_wa = [
        round(costo_aut, 2),
        round(costo_util, 2),
        round(costo_serv, 2),
        round(costo_mark, 2)
    ]
    conceptos_wa = [
        "Meta Auth (verificación)", 
        "Meta Utilidad", 
        "Meta Servicio", 
        "Meta Marketing"
    ]

elif proveedor_whatsapp == "360diag (Meta BSP)":
    st.markdown("**360diag** es un BSP aprobado por Meta que ofrece precios personalizados.")
    costo_numero = st.number_input("Costo número al mes", value=0)        
    conversaciones_autenticacion = st.slider("Conversaciones de Autenticación (360diag)", 0, 2000, 50)
    conversaciones_utilidad = st.slider("Conversaciones de Utilidad (360diag)", 0, 2000, 100)
    conversaciones_servicio = st.slider("Conversaciones de Servicio (360diag)", 0, 2000, 100)
    conversaciones_marketing = st.slider("Conversaciones de Marketing (360diag)", 0, 2000, 50)

    # Ajusta aquí las tarifas específicas de 360diag si son diferentes
    costo_aut = conversaciones_autenticacion * 0.015
    costo_util = conversaciones_utilidad * 0.011
    costo_serv = conversaciones_servicio * 0.011
    costo_mark = conversaciones_marketing * 0.023

    costo_whatsapp = costo_aut + costo_util + costo_serv + costo_mark + costo_numero

    detalle_wa = [
        round(costo_aut, 2),
        round(costo_util, 2),
        round(costo_serv, 2),
        round(costo_mark, 2)
    ]
    conceptos_wa = [
        "360diag Auth (verificación)", 
        "360diag Utilidad", 
        "360diag Servicio", 
        "360diag Marketing"
    ]


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
    costo_whatsapp +
    costo_render +
    costo_mysql +
    costo_extra
)
total_cop = total_usd * tasa_cop

# Mostrar resumen
st.subheader("💰 Resumen de costos")
st.metric("Costo mensual total (USD)", f"${total_usd:.2f}")
st.metric("Costo mensual total (COP)", f"${total_cop:,.0f} COP")

# Construcción dinámica del desglose final
conceptos_generales = [
    "OpenAI entrada (texto)", 
    "OpenAI salida (texto)", 
    "ElevenLabs (voz)", 
    "OpenAI TTS (voz)", 
    "Whisper (transcripción)"
]

costos_generales = [
    round(costo_entrada, 2), 
    round(costo_salida, 2), 
    round(costo_elevenlabs, 2),
    round(costo_openai_voice, 2),
    round(costo_whisper, 2)
]

# Combinar conceptos generales + WhatsApp + infraestructura
conceptos_totales = (
    conceptos_generales + 
    conceptos_wa + 
    ["Render", "Base de datos", "Otros"]
)

costos_totales = (
    costos_generales + 
    detalle_wa + 
    [round(costo_render, 2), round(costo_mysql, 2), round(costo_extra, 2)]
)

# Crear DataFrame final
datos = {
    "Concepto": conceptos_totales,
    "Costo (USD)": costos_totales
}
df = pd.DataFrame(datos)
# Nueva columna: participación porcentual
df["Participación (%)"] = (df["Costo (USD)"] / total_usd * 100).round(1)
st.dataframe(df, use_container_width=True, hide_index=True)


# 

st.caption("Calculadora para ayudarte a establecer precios rentables y justos para tu servicio. 🚀")


#✅ Entonces, si pones 20 en ese campo:
# Estás diciendo que el sistema va a procesar 20,000 tokens de entrada al mes.

# Suponiendo que cada mensaje del usuario tiene unos 10-15 tokens (bastante normal), eso equivale a:

# ~1,500 a 2,000 mensajes de entrada al mes.

# Esto puede representar ~60-70 conversaciones largas con múltiples mensajes.

#streamlit run calculadora_costos_agente.py