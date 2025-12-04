import os
import json
import telebot
import gspread
from flask import Flask, request
from google.oauth2.service_account import Credentials
from telebot.types import Update

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
SHEET_ID = '1umS0JFdYXu2f_x5zxzbnKfEf_fDZ7Hn5-Yt_sYQWpqg'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

def get_sheet():
    creds_json = os.environ.get('GOOGLE_CREDS_JSON')
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1

@bot.message_handler(regexp='^/plantilla\d{1,3}$')
def send_plantilla(message):
    try:
        num = message.text.replace('/plantilla', '')
        num_int = int(num)
        if num_int < 1 or num_int > 100:
            bot.reply_to(message, "❌ Solo tengo plantillas del 1 al 100")
            return
        
        sheet = get_sheet()
        row_num = num_int + 1
        enlace = sheet.cell(row_num, 3).value
        
        respuesta = f"✅ **Plantilla {num}**\nDescarga: {enlace}\n\n💡 _Ver video tutorial en YouTube_"
        bot.reply_to(message, respuesta, parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    respuesta = "👋 **¡Bot de Tesirve!**\n\nEscribe:\n`/plantilla1` a `/plantilla100`\n\n🌐 _https://tesirve.com_"
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
    return '✅ Bot funcionando - tesirve.com'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
