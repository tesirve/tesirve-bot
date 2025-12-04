import os
import json
import telebot
import requests
from flask import Flask, request
from telebot.types import Update

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
SHEET_ID = '1umS0JFdYXu2f_x5zxzbnKfEf_fDZ7Hn5-Yt_sYQWpqg'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

def get_plantilla_url(num):
    """Obtener enlace directamente de Sheets API"""
    try:
        # Obtener JSON de credenciales
        creds_json = os.environ.get('GOOGLE_CREDS_JSON')
        creds = json.loads(creds_json)
        
        # Obtener token de acceso
        from google.oauth2 import service_account
        credentials = service_account.Credentials.from_service_account_info(creds)
        scoped_credentials = credentials.with_scopes([
            'https://www.googleapis.com/auth/spreadsheets.readonly'
        ])
        
        # Hacer request directa a Sheets API
        import google.auth.transport.requests
        auth_req = google.auth.transport.requests.Request()
        scoped_credentials.refresh(auth_req)
        
        # Leer la fila específica
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/A{num+1}:C{num+1}'
        headers = {'Authorization': f'Bearer {scoped_credentials.token}'}
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'values' in data:
            # Columna C es el enlace
            return data['values'][0][2] if len(data['values'][0]) > 2 else None
        return None
        
    except Exception as e:
        print(f"Error Sheets API: {e}")
        return None

@bot.message_handler(regexp='^/plantilla\d{1,3}$')
def send_plantilla(message):
    try:
        num = int(message.text.replace('/plantilla', ''))
        if num < 1 or num > 100:
            bot.reply_to(message, "❌ Solo plantillas 1-100")
            return
        
        enlace = get_plantilla_url(num)
        
        if enlace:
            respuesta = f"✅ **Plantilla {num}**\n{enlace}"
            bot.reply_to(message, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(message, f"❌ No encontré plantilla {num}")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)[:100]}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    respuesta = "👋 **Bot de Tesirve**\nEscribe: `/plantilla1` a `/plantilla100`"
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
    return '✅ Bot tesirve.com'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
