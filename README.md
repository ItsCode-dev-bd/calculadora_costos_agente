# 📊 Calculadora de Costos del Agente IA (ItsCode)

Esta app en **Streamlit** permite calcular los costos mensuales de operación de un agente de inteligencia artificial que atiende por WhatsApp, ya sea usando Twilio o directamente la API de Meta.

## ✅ Características

- Estimación de costos por tokens GPT (entrada/salida).
- Cálculo de uso de voz IA con ElevenLabs y OpenAI TTS.
- Transcripción automática con Whisper.
- Costos mensuales por proveedor de WhatsApp (Twilio o Meta API).
- Costos adicionales como hosting, base de datos, email, etc.
- Conversión automática de dólares a pesos colombianos (COP).
- Visualización detallada de participación por rubro (%).

## 🚀 Cómo ejecutar

1. Instala las dependencias:
```bash
pip install streamlit pandas pillow


2.Ejecuta la app
streamlit run calculadora_costos_agente.py

3.Abre el enlace que se genera (generalmente: http://localhost:8501).

📞 WhatsApp API – Tipos de conversación
Meta (WhatsApp Business) clasifica las conversaciones en 4 categorías con distintos precios:

Autenticación: Validación de usuarios mediante OTPs, accesos, códigos, etc.

Utilidad: Mensajes transaccionales (estado de pedidos, pagos, recordatorios).

Servicio: Respuesta a mensajes iniciados por el usuario.

Marketing: Promociones, novedades, campañas de ventas.

Cada categoría tiene un precio diferente y se factura por "ventanas de 24h".

✨ Autor
Desarrollado por ItsCode 🚀