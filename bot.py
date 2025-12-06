import os
import telebot
from flask import Flask, request
from telebot.types import Update

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# DICCIONARIO EN MINÚSCULAS
COMANDOS_PLANTILLAS = {
    "p1-xr3f": (1, "https://drive.google.com/uc?export=download&id=1b4LDpfC2PXdW2AIwq0Egf-WNacq_kMEu"),
    "p2-9rt8": (2, "https://drive.google.com/uc?export=download&id=1AP39WByiakUXay_aeXpRqF_y3LFZAMxe"),
    "p3-kl4m": (3, "https://drive.google.com/uc?export=download&id=120m8rK1dRnNnBG3_tSeELPMDLn6P-hj5"),
    "p4-7d2b": (4, "https://drive.google.com/uc?export=download&id=1icn0Uvk-2RVrc8S1J16jZ3Xk02IExWNI"),
    "p5-v6n1": (5, "https://drive.google.com/uc?export=download&id=1QsM99bGr28k6ap5a0chi4MF-L5g0GqXW"),
    "p6-a3x8": (6, "https://drive.google.com/uc?export=download&id=1gIGZvRr27LLk_f8eIfl9xAkAM1qpLpw2"),
    "p7-b9c2": (7, "https://drive.google.com/uc?export=download&id=1idfU_hOgBoKQ0ouLSguYyPdqPRrw--6J"),
    "p8-m5k7": (8, "https://drive.google.com/uc?export=download&id=1Ww-oWmuff7_aEMdEms7YgELzJcC4Txxe"),
    "p9-j4r1": (9, "https://drive.google.com/uc?export=download&id=1teUloMeLoUL0rmFB8chPP8s_3Z-FqS9S"),
    "p10-f8t3": (10, "https://drive.google.com/uc?export=download&id=1DcvcZWHkP2a_dKFNCV98hz9Qt_VxRHW5"),
    # ... (mantén el resto igual)
}

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# 1. Handler SIMPLE para TODO
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        print(f"Mensaje recibido: '{message.text}'")  # Para debug
        
        texto = message.text.strip().lower()  # Convertir a minúsculas
        
        # Si es un comando con / (o código sin /)
        if texto.startswith('/'):
            comando = texto[1:]  # Quitar el /
        else:
            comando = texto  # Si no tiene /, usar el texto directamente
        
        # PRIMERO: Verificar si es un comando de plantilla
        if comando in COMANDOS_PLANTILLAS:
            num, enlace = COMANDOS_PLANTILLAS[comando]
            respuesta = f"✅ **Plantilla {num} - Descarga Directa**\n\n"
            respuesta += f"🔗 *Enlace:* {enlace}\n\n"
            respuesta += "💡 *Instrucciones:*\n"
            respuesta += "1. Haz clic en el enlace de arriba\n"
            respuesta += "2. Se descargará automáticamente el archivo ZIP\n"
            respuesta += "3. Si Google Drive muestra advertencia, haz clic en 'Descargar de todos modos'\n\n"
            respuesta += "🎬 *Video tutorial:* https://youtube.com/tesirve"
            bot.reply_to(message, respuesta, parse_mode='Markdown')
            return
        
        # SEGUNDO: Comando /start con parámetro
        elif texto.startswith('/start '):
            param = texto.split()[1].lower()  # Obtener parámetro y convertir a minúsculas
            print(f"Parámetro /start: '{param}'")
            
            if param in COMANDOS_PLANTILLAS:
                num, enlace = COMANDOS_PLANTILLAS[param]
                respuesta = f"✅ **Plantilla {num} - Descarga Directa**\n\n"
                respuesta += f"🔗 *Enlace:* {enlace}\n\n"
                respuesta += "💡 *Instrucciones:*\n"
                respuesta += "1. Haz clic en el enlace de arriba\n"
                respuesta += "2. Se descargará automáticamente el archivo ZIP\n"
                respuesta += "3. Si Google Drive muestra advertencia, haz clic en 'Descargar de todos modos'\n\n"
                respuesta += "🎬 *Video tutorial:* https://youtube.com/tesirve"
                bot.reply_to(message, respuesta, parse_mode='Markdown')
                return
            else:
                # Si es /start con parámetro no reconocido
                send_welcome(message)
                return
        
        # TERCERO: Comandos especiales
        elif texto == '/start':
            send_welcome(message)
            return
            
        elif texto in ['/ayuda', '/help']:
            send_help(message)
            return
            
        elif texto == '/plantillas':
            send_plantillas_list(message)
            return
        
        # CUARTO: Si no es ninguna de las anteriores
        else:
            # Verificar si parece un código (p1-xr3f, etc.)
            if any(codigo in texto for codigo in ['p1-', 'p2-', 'p3-', 'p4-', 'p5-', 'p6-', 'p7-', 'p8-', 'p9-', 'p10-']):
                respuesta = f"🤔 *¿Quieres descargar una plantilla?*\n\n"
                respuesta += f"Usa el comando con barra: `/{texto}`\n\n"
                respuesta += f"Por ejemplo, escribe: `/{texto}`"
                bot.reply_to(message, respuesta, parse_mode='Markdown')
            else:
                respuesta = "🤖 *Bot Tesirve*\n\n"
                respuesta += "Escribe `/ayuda` para ver opciones.\n"
                respuesta += "O usa un código como `/p1-xr3f` para descargar plantillas."
                bot.reply_to(message, respuesta, parse_mode='Markdown')
            
    except Exception as e:
        print(f"Error: {str(e)}")
        bot.reply_to(message, "❌ Error procesando tu solicitud.")

# 2. Función de bienvenida
def send_welcome(message):
    respuesta = "👋 **¡Hola! Soy el bot de Tesirve** 🌐\n\n"
    respuesta += "📁 *¿Qué puedo hacer?*\n"
    respuesta += "• Enviarte plantillas HTML/CSS\n"
    respuesta += "• Proporcionar enlaces de descarga directa\n"
    respuesta += "• Ayuda básica con tus proyectos\n\n"
    respuesta += "🔗 *Para descargar plantillas:*\n"
    respuesta += "Usa: `/p1-xr3f` (ejemplo)\n"
    respuesta += "O visita: https://tesirve.com\n\n"
    respuesta += "❓ *Ayuda:* `/ayuda`\n"
    respuesta += "📚 *Lista:* `/plantillas`"
    bot.reply_to(message, respuesta, parse_mode='Markdown')

# 3. Función de ayuda
def send_help(message):
    respuesta = "🆘 **Ayuda - Bot Tesirve**\n\n"
    respuesta += "📌 *Comandos disponibles:*\n"
    respuesta += "• `/start` - Mensaje de bienvenida\n"
    respuesta += "• `/ayuda` - Esta información\n"
    respuesta += "• `/p1-xr3f` - Descargar plantilla (ejemplo)\n"
    respuesta += "• `/plantillas` - Ver lista de plantillas\n\n"
    respuesta += "🔧 *¿Cómo descargar?*\n"
    respuesta += "1. Escribe `/p1-xr3f` (o cualquier código)\n"
    respuesta += "2. Recibirás un enlace de descarga directa\n"
    respuesta += "3. Haz clic y se descargará automáticamente\n\n"
    respuesta += "🌐 *Sitio web:* https://tesirve.com"
    bot.reply_to(message, respuesta, parse_mode='Markdown')

# 4. Función para listar algunas plantillas
def send_plantillas_list(message):
    respuesta = "📚 **Plantillas disponibles**\n\n"
    respuesta += "📌 *Ejemplos de códigos:*\n"
    
    # Mostrar primeros 10
    count = 0
    for comando, (num, _) in COMANDOS_PLANTILLAS.items():
        if count < 10:
            respuesta += f"• `/{comando}` - Plantilla {num}\n"
            count += 1
        else:
            break
    
    respuesta += "\n📋 *Hay 100 plantillas en total*\n\n"
    respuesta += "🔗 *Visita:* https://tesirve.com para ver todas con botones de descarga"
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
    # Verificar que el token esté configurado
    if not TELEGRAM_TOKEN:
        print("ERROR: TELEGRAM_TOKEN no está configurado")
        exit(1)
    
    print("🤖 Bot iniciado correctamente")
    print(f"Token: {TELEGRAM_TOKEN[:15]}..." if TELEGRAM_TOKEN else "NO TOKEN")
    print(f"Plantillas cargadas: {len(COMANDOS_PLANTILLAS)}")
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
