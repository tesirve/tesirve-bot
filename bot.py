import os
import telebot
from flask import Flask, request
from telebot.types import Update

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# SOLO LAS PRIMERAS 10 PLANTILLAS
PLANTILLAS = {
    "p1-xr3f": "https://drive.google.com/uc?export=download&id=1b4LDpfC2PXdW2AIwq0Egf-WNacq_kMEu",
    "p2-9rt8": "https://drive.google.com/uc?export=download&id=1AP39WByiakUXay_aeXpRqF_y3LFZAMxe",
    "p3-kl4m": "https://drive.google.com/uc?export=download&id=120m8rK1dRnNnBG3_tSeELPMDLn6P-hj5",
    "p4-7d2b": "https://drive.google.com/uc?export=download&id=1icn0Uvk-2RVrc8S1J16jZ3Xk02IExWNI",
    "p5-v6n1": "https://drive.google.com/uc?export=download&id=1QsM99bGr28k6ap5a0chi4MF-L5g0GqXW",
    "p6-a3x8": "https://drive.google.com/uc?export=download&id=1gIGZvRr27LLk_f8eIfl9xAkAM1qpLpw2",
    "p7-b9c2": "https://drive.google.com/uc?export=download&id=1idfU_hOgBoKQ0ouLSguYyPdqPRrw--6J",
    "p8-m5k7": "https://drive.google.com/uc?export=download&id=1Ww-oWmuff7_aEMdEms7YgELzJcC4Txxe",
    "p9-j4r1": "https://drive.google.com/uc?export=download&id=1teUloMeLoUL0rmFB8chPP8s_3Z-FqS9S",
    "p10-f8t3": "https://drive.google.com/uc?export=download&id=1DcvcZWHkP2a_dKFNCV98hz9Qt_VxRHW5",
}

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# UN SOLO HANDLER PARA TODO
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    texto = message.text.strip().lower()
    
    # Si es un comando con /p1-xr3f
    if texto.startswith('/'):
        comando = texto[1:]  # Quitar el /
        
        if comando in PLANTILLAS:
            enlace = PLANTILLAS[comando]
            respuesta = f"✅ **Enlace de descarga:**\n\n{enlace}"
            bot.reply_to(message, respuesta, parse_mode='Markdown')
            return
    
    # Si es /start con parámetro
    if texto.startswith('/start '):
        partes = texto.split()
        if len(partes) > 1:
            codigo = partes[1].lower()
            if codigo in PLANTILLAS:
                enlace = PLANTILLAS[codigo]
                respuesta = f"✅ **Enlace de descarga:**\n\n{enlace}"
                bot.reply_to(message, respuesta, parse_mode='Markdown')
                return
    
    # Si es solo el código sin / (p1-xr3f)
    if texto in PLANTILLAS:
        enlace = PLANTILLAS[texto]
        respuesta = f"✅ **Enlace de descarga:**\n\n{enlace}"
        bot.reply_to(message, respuesta, parse_mode='Markdown')
        return
    
    # Si es solo /start
    if texto == '/start':
        bot.reply_to(message, "👋 Envía /p1-xr3f para descargar.")
        return
    
    # Para cualquier otra cosa
    bot.reply_to(message, "❌ Envía un código como /p1-xr3f")

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
    return '✅ Bot funcionando'

if __name__ == '__main__':
    print("🤖 Bot iniciado")
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
