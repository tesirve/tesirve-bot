import os
import telebot
from flask import Flask, request
from telebot.types import Update

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# NUEVO: COMANDOS ALEATORIOS CON IDENTIFICADOR P1, P2, P3...
COMANDOS_PLANTILLAS = {
    # Formato: "P1-XR3F": (número_plantilla, enlace)
    "P1-XR3F": (1, "https://drive.google.com/file/d/1b4LDpfC2PXdW2AIwq0Egf-WNacq_kMEu/view"),
    "P2-9RT8": (2, "https://drive.google.com/file/d/1AP39WByiakUXay_aeXpRqF_y3LFZAMxe/view"),
    "P3-KL4M": (3, "https://drive.google.com/file/d/120m8rK1dRnNnBG3_tSeELPMDLn6P-hj5/view"),
    "P4-7D2B": (4, "https://drive.google.com/file/d/1icn0Uvk-2RVrc8S1J16jZ3Xk02IExWNI/view"),
    "P5-V6N1": (5, "https://drive.google.com/file/d/1QsM99bGr28k6ap5a0chi4MF-L5g0GqXW/view"),
    # Los otros 95 mantienen enlaces viejos por ahora
    "P6-A3X8": (6, "https://drive.google.com/file/d/1HHXXppKob2K6v_dqAlrkvFqOg-9bUnHA/view"),
    "P7-B9C2": (7, "https://drive.google.com/file/d/1ldX7Gd2scJHhZ4OYs30JhKx3QLiJ8bmC/view"),
    "P8-M5K7": (8, "https://drive.google.com/file/d/1og9A-nfT-z0oIsCcrImh2kqK7OX9i-nC/view"),
    "P9-J4R1": (9, "https://drive.google.com/file/d/1gqg0Tcc9rrdt4EXInZSOznhAz5f_qivh/view"),
    "P10-F8T3": (10, "https://drive.google.com/file/d/1QdIpsL33RazRkCN0rE8Xj27DgM7u5OXw/view"),
    # Continuar hasta P100...
}

# También mantener diccionario viejo para transición
ENLACES_PLANTILLAS = {
    1: "https://drive.google.com/file/d/1b4LDpfC2PXdW2AIwq0Egf-WNacq_kMEu/view",
    2: "https://drive.google.com/file/d/1AP39WByiakUXay_aeXpRqF_y3LFZAMxe/view",
    3: "https://drive.google.com/file/d/120m8rK1dRnNnBG3_tSeELPMDLn6P-hj5/view",
    4: "https://drive.google.com/file/d/1icn0Uvk-2RVrc8S1J16jZ3Xk02IExWNI/view",
    5: "https://drive.google.com/file/d/1QsM99bGr28k6ap5a0chi4MF-L5g0GqXW/view",
    6: "https://drive.google.com/file/d/1HHXXppKob2K6v_dqAlrkvFqOg-9bUnHA/view",
    7: "https://drive.google.com/file/d/1ldX7Gd2scJHhZ4OYs30JhKx3QLiJ8bmC/view",
    8: "https://drive.google.com/file/d/1og9A-nfT-z0oIsCcrImh2kqK7OX9i-nC/view",
    9: "https://drive.google.com/file/d/1gqg0Tcc9rrdt4EXInZSOznhAz5f_qivh/view",
    10: "https://drive.google.com/file/d/1QdIpsL33RazRkCN0rE8Xj27DgM7u5OXw/view",
    # ... resto igual que antes
}

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# 1. Manejar NUEVOS comandos aleatorios (P1-XR3F, P2-9RT8, etc.)
@bot.message_handler(regexp='^/P\d{1,3}-[A-Z0-9]{4}$')
def send_plantilla_nueva(message):
    try:
        comando = message.text[1:]  # Quita el "/"
        
        if comando in COMANDOS_PLANTILLAS:
            num, enlace = COMANDOS_PLANTILLAS[comando]
            respuesta = f"✅ **Plantilla {num}**\n{enlace}\n\n💡 _Recuerda ver el video tutorial en YouTube_"
            bot.reply_to(message, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ Código no válido. Usa los botones de https://tesirve.com")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)[:50]}")

# 2. Mantener VIEJOS comandos (/plantilla1) por compatibilidad
@bot.message_handler(regexp='^/plantilla\d{1,3}$')
def send_plantilla_vieja(message):
    try:
        num = int(message.text.replace('/plantilla', ''))
        
        if num in ENLACES_PLANTILLAS:
            respuesta = f"⚠️ *Sistema antiguo*\n\n"
            respuesta += f"**Plantilla {num}**: {ENLACES_PLANTILLAS[num]}\n\n"
            respuesta += "_Usa los botones en https://tesirve.com para códigos nuevos_"
            bot.reply_to(message, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(message, f"❌ Plantilla {num} no disponible")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)[:50]}")

# 3. NUEVO MENSAJE DE BIENVENIDA PROFESIONAL
@bot.message_handler(commands=['start'])
def send_welcome(message):
    respuesta = "👋 **¡Hola! Soy el asistente de Tesirve** 🌐\n\n"
    respuesta += "🌱 *¿En qué puedo servirte?*\n"
    respuesta += "• Soporte técnico de plantillas HTML/CSS\n"
    respuesta += "• Preguntas sobre diseño web\n"
    respuesta += "• Ayuda con código básico\n\n"
    respuesta += "📁 *Para descargar plantillas:*\n"
    respuesta += "Visita https://tesirve.com y usa los botones de descarga.\n\n"
    respuesta += "💬 *Pregúntame lo que necesites...*"
    bot.reply_to(message, respuesta, parse_mode='Markdown')

# 4. Comando de ayuda general
@bot.message_handler(commands=['help', 'ayuda'])
def send_help(message):
    respuesta = "🆘 **Ayuda - Tesirve Bot**\n\n"
    respuesta += "📌 *Comandos disponibles:*\n"
    respuesta += "• `/start` - Mensaje de bienvenida\n"
    respuesta += "• `/ayuda` - Esta información\n"
    respuesta += "• `/pregunta [texto]` - Próximamente: pregúntame algo\n\n"
    respuesta += "🌐 *Recursos:* https://tesirve.com"
    bot.reply_to(message, respuesta, parse_mode='Markdown')

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('UTF-8')
        update = Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Error', 403

@app.route('/')
def home():
    return '✅ Bot tesirve.com funcionando'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
