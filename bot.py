import os
import telebot
from flask import Flask, request
from telebot.types import Update

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# PRIMEROS 5 SOLO PARA PRUEBA
PLANTILLAS = {
    "p1-xr3f": "https://drive.google.com/uc?export=download&id=1b4LDpfC2PXdW2AIwq0Egf-WNacq_kMEu",
    "p2-9rt8": "https://drive.google.com/uc?export=download&id=1AP39WByiakUXay_aeXpRqF_y3LFZAMxe",
    "p3-kl4m": "https://drive.google.com/uc?export=download&id=120m8rK1dRnNnBG3_tSeELPMDLn6P-hj5",
    "p4-7d2b": "https://drive.google.com/uc?export=download&id=1icn0Uvk-2RVrc8S1J16jZ3Xk02IExWNI",
    "p5-v6n1": "https://drive.google.com/uc?export=download&id=1QsM99bGr28k6ap5a0chi4MF-L5g0GqXW",
}

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# Handler SIMPLE para cualquier comando /p...
@bot.message_handler(func=lambda m: m.text.startswith('/') and m.text[1:].lower() in PLANTILLAS)
def send_plantilla(message):
    comando = message.text[1:].lower()
    
    if comando in PLANTILLAS:
        enlace = PLANTILLAS[comando]
        respuesta = f"📦 **Plantilla {comando.upper()}**\n\n🔗 {enlace}"
        bot.reply_to(message, respuesta, parse_mode='Markdown')

# Handler para /start
@bot.message_handler(commands=['start'])
def send_start(message):
    if ' ' in message.text:
        partes = message.text.split()
        codigo = partes[1].lower()
        
        if codigo in PLANTILLAS:
            enlace = PLANTILLAS[codigo]
            respuesta = f"📦 **Plantilla {codigo.upper()}**\n\n🔗 {enlace}"
            bot.reply_to(message, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(message, "Error: código no válido")
    else:
        bot.reply_to(message, "Envía /p1-xr3f para descargar")

# Handler para texto simple
@bot.message_handler(func=lambda m: m.text.lower() in PLANTILLAS)
def send_plantilla_simple(message):
    codigo = message.text.lower()
    enlace = PLANTILLAS[codigo]
    respuesta = f"📦 **Plantilla {codigo.upper()}**\n\n🔗 {enlace}"
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
    return 'Bot funcionando'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
