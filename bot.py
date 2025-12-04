import os
import telebot
from flask import Flask, request
from telebot.types import Update

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# LISTA FIJA de 100 enlaces (usa los primeros 3 como ejemplo, luego completas)
ENLACES_PLANTILLAS = {
    1: "https://drive.google.com/file/d/1TPayTVWU4dMqE14mbYHAbys1t17UGXko/view",
    2: "https://drive.google.com/file/d/1KurC6cLqy-b5RTP5nOe8-7ixlN12xQvO/view",
    3: "https://drive.google.com/file/d/1s9dknopKqWe5D_3DZ5LErWfqYqRRtlQz/view",
    # ... agregar los otros 97 manualmente
}

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@bot.message_handler(regexp='^/plantilla\d{1,3}$')
def send_plantilla(message):
    try:
        num = int(message.text.replace('/plantilla', ''))
        
        if num in ENLACES_PLANTILLAS:
            respuesta = f"✅ **Plantilla {num}**\n{ENLACES_PLANTILLAS[num]}"
            bot.reply_to(message, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(message, f"❌ Plantilla {num} no disponible aún")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)[:50]}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    respuesta = "👋 **Bot de Tesirve**\nEscribe: `/plantilla1` a `/plantilla100`\n\n🌐 _tesirve.com_"
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
