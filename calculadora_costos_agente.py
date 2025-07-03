import streamlit as st
import pandas as pd
from PIL import Image

# Configuración general
st.set_page_config(page_title="Calculadora de Costos del Agente IA", layout="centered")

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
st.header("1. OpenAI (Modelo)")
modelo = st.selectbox("Modelo", ["GPT-3.5-turbo", "GPT-3.5-turbo-1106", "GPT-4", "GPT-4-turbo", "GPT-4o"])

limites_contexto = {
    "GPT-3.5-turbo": 4096,
    "GPT-3.5-turbo-1106": 16385,
    "GPT-4": 8192,
    "GPT-4-turbo": 128000,
    "GPT-4o": 128000
}
st.markdown("""
| Modelo                | Límite de tokens | ≈ Caracteres (español) | Costo entrada (por 1K tokens) | Costo salida (por 1K tokens) |
|------------------------|------------------|-------------------------|-------------------------------|------------------------------|
| GPT-3.5-turbo          | 4,096 tokens     | ~14,336 caracteres      | $0.0015                       | $0.0020                      |
| GPT-3.5-turbo-1106     | 16,385 tokens    | ~57,348 caracteres      | $0.0010                       | $0.0020                      |
| GPT-4                  | 8,192 tokens     | ~28,672 caracteres      | $0.0300                       | $0.0600                      |
| GPT-4-turbo            | 128,000 tokens   | ~448,000 caracteres     | $0.0100                       | $0.0300                      |
| GPT-4o                 | 128,000 tokens   | ~448,000 caracteres     | $0.0050                       | $0.0150                      |
""", unsafe_allow_html=True)

#
st.markdown(f"🔹 Límite de contexto: **{limites_contexto[modelo]:,} tokens** (entrada + salida por mensaje)")

tokens_entrada = st.slider("Tokens totales de entrada por mes (en miles)", 0, 2000, 100)
tokens_salida = st.slider("Tokens totales de salida por mes (en miles)", 0, 2000, 200)

# Entrada promedio (usuario): 20 a 50 tokens.

# Respuesta promedio (IA): 100 a 300 tokens.

PROMEDIO_TOKENS_ENTRADA = 30
PROMEDIO_TOKENS_SALIDA = 150

mensajes_aprox_entrada = int((tokens_entrada * 1000) / PROMEDIO_TOKENS_ENTRADA)
mensajes_aprox_salida = int((tokens_salida * 1000) / PROMEDIO_TOKENS_SALIDA)

st.markdown(f"🔸 Aproximadamente **{mensajes_aprox_entrada:,} mensajes de entrada** al mes (usuario escribe).")
st.markdown(f"🔸 Aproximadamente **{mensajes_aprox_salida:,} mensajes de salida** al mes (respuesta de IA).")

if modelo == "GPT-3.5-turbo":
    costo_entrada = tokens_entrada * 0.0015
    costo_salida = tokens_salida * 0.002
elif modelo == "GPT-3.5-turbo-1106":
    costo_entrada = tokens_entrada * 0.0010
    costo_salida = tokens_salida * 0.002
elif modelo == "GPT-4":
    costo_entrada = tokens_entrada * 0.03
    costo_salida = tokens_salida * 0.06
elif modelo == "GPT-4-turbo":
    costo_entrada = tokens_entrada * 0.01
    costo_salida = tokens_salida * 0.03    
elif modelo == "GPT-4o":
    costo_entrada = tokens_entrada * 0.005
    costo_salida = tokens_salida * 0.015    

costo_openai = costo_entrada + costo_salida

# 2. ElevenLabs (voz IA)
st.header("2. ElevenLabs (voz IA)")
st.markdown("1,000 caracteres de texto ≈ 1 minuto de audio")
st.markdown("Plan Starter $0.30 por cada 1,000 caracteres extra")
st.markdown("Plan Creator $0.24 por cada 1,000 caracteres extra")
st.markdown("Plan Independent $0.20 por cada 1,000 caracteres extra")
plan_elevenlabs = st.selectbox("Plan ElevenLabs", ["Gratuito", "Starter ($5, 30K caracteres)", "Creator ($22, 100K caracteres)", "Independent ($99, 500K caracteres)"])
caracteres_voz_elevenlabs = st.slider("Caracteres de texto convertidos a voz con ElevenLabs", 0, 1_000_000, 31_000)

if plan_elevenlabs == "Gratuito":
    included = 10_000
    extra_cost = 0.0
    base_cost = 0
elif plan_elevenlabs == "Starter ($5, 30K caracteres)":
    included = 30_000
    extra_cost = 0.30 / 1000
    base_cost = 5
elif plan_elevenlabs == "Creator ($22, 100K caracteres)":
    included = 100_000
    extra_cost = 0.24 / 1000
    base_cost = 22
elif plan_elevenlabs == "Independent ($99, 500K caracteres)":
    included = 500_000
    extra_cost = 0.20 / 1000
    base_cost = 99    

if caracteres_voz_elevenlabs <= included:
    costo_elevenlabs = base_cost
else:
    excedente = caracteres_voz_elevenlabs - included
    costo_elevenlabs = base_cost + excedente * extra_cost

# 3. OpenAI TTS (voz)
st.header("3. OpenAI TTS (voz IA)")
st.markdown("1,000 caracteres de texto ≈ 1 minutos de audio")
st.markdown("100,000 caracteres de texto ≈ 1.4 h (100 min)")
caracteres_voz_openai = st.slider("Caracteres de texto convertidos a voz", 0, 500_000, 100_000)
costo_openai_voice = caracteres_voz_openai * 0.015 / 1000

# 4. Whisper (transcripción)
st.header("4. Whisper (transcripción de audios)")
minutos_transcripcion = st.slider("Minutos de audio a transcribir", 0, 500, 60)
costo_whisper = minutos_transcripcion * 0.006

# 5. WhatsApp API
st.header("5. WhatsApp API")
proveedor_whatsapp = st.radio("Proveedor de WhatsApp API", ["Twilio", "Meta API directa", "360diag (Meta BSP)"])

if proveedor_whatsapp == "Twilio":
    costo_numero = st.number_input("Costo número al mes (Twilio)", value=5.0)
    conversaciones = st.slider("Conversaciones (ventanas de 24h) al mes", 0, 5000, 300)
    mensajes_por_conversacion = st.slider("Mensajes promedio por conversación", 1, 100, 25)

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

elif proveedor_whatsapp == "Meta API directa":
    # st.markdown("**Nota**: Debes tener un proveedor BSP aprobado para usar la API directa de Meta.")
    costo_numero = st.number_input("Costo número al mes", value=0)    
    conversaciones_autenticacion = st.slider("Conversaciones de Autenticación", 0, 2000, 50)
    conversaciones_utilidad = st.slider("Conversaciones de Utilidad", 0, 2000, 100)
    conversaciones_servicio = st.slider("Conversaciones de Servicio", 0, 2000, 0)
    conversaciones_marketing = st.slider("Conversaciones de Marketing", 0, 2000, 50)

    costo_aut = conversaciones_autenticacion * 0.0002
    costo_util = conversaciones_utilidad * 0.0002
    costo_serv = conversaciones_servicio * 0
    costo_mark = conversaciones_marketing * 0.0125

    costo_whatsapp = costo_aut + costo_util + costo_serv + costo_mark + costo_numero

    detalle_wa = [
        round(costo_numero, 2),        
        round(costo_aut, 2),
        round(costo_util, 2),
        round(costo_serv, 2),
        round(costo_mark, 2)
    ]
    conceptos_wa = [
        "Meta número fijo",         
        "Meta Auth (verificación)", 
        "Meta Utilidad", 
        "Meta Servicio", 
        "Meta Marketing"
    ]

elif proveedor_whatsapp == "360diag (Meta BSP)":
    st.markdown("**360diag** es un BSP aprobado por Meta que ofrece un plan regular de 49 usd a esto hay que sumarle el cobro por parte de meta generado por cada mensaje.")
    costo_numero = st.number_input("Costo número al mes", value=49)        
    conversaciones_autenticacion = st.slider("Conversaciones de Autenticación (360diag)", 0, 2000, 50)
    conversaciones_utilidad = st.slider("Conversaciones de Utilidad (360diag)", 0, 2000, 100)
    conversaciones_servicio = st.slider("Conversaciones de Servicio (360diag)", 0, 2000, 0)
    conversaciones_marketing = st.slider("Conversaciones de Marketing (360diag)", 0, 2000, 50)

    costo_aut = conversaciones_autenticacion * 0.0002
    costo_util = conversaciones_utilidad * 0.0002
    costo_serv = conversaciones_servicio * 0
    costo_mark = conversaciones_marketing * 0.0125

    costo_whatsapp = costo_aut + costo_util + costo_serv + costo_mark + costo_numero

    detalle_wa = [
        round(costo_numero, 2),        
        round(costo_aut, 2),
        round(costo_util, 2),
        round(costo_serv, 2),
        round(costo_mark, 2)
    ]
    conceptos_wa = [
        "360diag Plan regular",      
        "360diag Auth (verificación)", 
        "360diag Utilidad", 
        "360diag Servicio", 
        "360diag Marketing"
    ]

# 6. Render
st.header("6. Servidor (alojamiento)")
costo_render = st.number_input("Costo mensual servidor", value=5)

# 7. Base de datos
st.header("7. Base de datos MySQL")
costo_mysql = st.number_input("Costo mensual base de datos", value=0)

# 8. Extras
st.header("8. Extras opcionales")
costo_extra = st.number_input("Otros costos (email, dominios, almacenamiento...)", value=0)

# 9. Plan del Cliente (IA Texto)
st.header("9. Plan del Cliente (IA Texto)")
st.markdown("**Plan Starter** 10 usd/mes")
st.markdown("**Plan Pro** 25 usd/mes")
plan_cliente = st.selectbox("Selecciona el plan ofrecido al cliente", ["Ninguno", "Starter", "Pro"])

# Calcular caracteres generados
caracteres_generados = tokens_salida * 1000 * 4  # 1 token ≈ 4 caracteres
costo_plan_fijo = 0
costo_exceso_texto = 0

if plan_cliente == "Starter":
    costo_plan_fijo = 10
    exceso_caracteres = max(0, caracteres_generados - 30_000)
    costo_exceso_texto = (exceso_caracteres / 1000) * 0.30

elif plan_cliente == "Pro":
    costo_plan_fijo = 25
    exceso_caracteres = max(0, caracteres_generados - 100_000)
    costo_exceso_texto = (exceso_caracteres / 1000) * 0.30

# Mostrar detalles del plan
if plan_cliente != "Ninguno":
    st.markdown(f"🔹 **Caracteres generados:** {caracteres_generados:,}")
    st.markdown(f"🔹 **Exceso:** {exceso_caracteres:,} caracteres")
    st.markdown(f"🔹 **Costo adicional por exceso:** ${costo_exceso_texto:.2f} USD")#


# Calcular totales
total_usd = (
    costo_openai +
    costo_elevenlabs +
    costo_openai_voice +
    costo_whisper +
    costo_whatsapp +
    costo_render +
    costo_mysql +
    costo_extra +
    costo_plan_fijo +
    costo_exceso_texto    
)
total_cop = total_usd * tasa_cop

# Mostrar resumen
st.subheader("💰 Resumen de costos")
st.metric("Costo mensual total (USD)", f"${total_usd:.2f}")
st.metric("Costo mensual total (COP)", f"${total_cop:,.0f} COP")

# Desglose de costos
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

conceptos_totales += ["Plan IA Texto (base)", "Exceso caracteres IA"]
costos_totales += [round(costo_plan_fijo, 2), round(costo_exceso_texto, 2)]


datos = {
    "Concepto": conceptos_totales,
    "Costo (USD)": costos_totales
}
df = pd.DataFrame(datos)
df["Participación (%)"] = (df["Costo (USD)"] / total_usd * 100).round(1)
st.dataframe(df, use_container_width=True, hide_index=True)

st.caption("Calculadora para ayudarte a establecer precios rentables y justos para tu servicio. 🚀")





# #streamlit run calculadora_costos_agente.py