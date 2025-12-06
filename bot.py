import os
import telebot
from flask import Flask, request
from telebot.types import Update

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# DICCIONARIO COMPLETO DE 100 PLANTILLAS CON ENLACES DIRECTOS DE DESCARGA
COMANDOS_PLANTILLAS = {
    "P1-XR3F": (1, "https://drive.google.com/uc?export=download&id=1b4LDpfC2PXdW2AIwq0Egf-WNacq_kMEu"),
    "P2-9RT8": (2, "https://drive.google.com/uc?export=download&id=1AP39WByiakUXay_aeXpRqF_y3LFZAMxe"),
    "P3-KL4M": (3, "https://drive.google.com/uc?export=download&id=120m8rK1dRnNnBG3_tSeELPMDLn6P-hj5"),
    "P4-7D2B": (4, "https://drive.google.com/uc?export=download&id=1icn0Uvk-2RVrc8S1J16jZ3Xk02IExWNI"),
    "P5-V6N1": (5, "https://drive.google.com/uc?export=download&id=1QsM99bGr28k6ap5a0chi4MF-L5g0GqXW"),
    "P6-A3X8": (6, "https://drive.google.com/uc?export=download&id=1gIGZvRr27LLk_f8eIfl9xAkAM1qpLpw2"),
    "P7-B9C2": (7, "https://drive.google.com/uc?export=download&id=1idfU_hOgBoKQ0ouLSguYyPdqPRrw--6J"),
    "P8-M5K7": (8, "https://drive.google.com/uc?export=download&id=1Ww-oWmuff7_aEMdEms7YgELzJcC4Txxe"),
    "P9-J4R1": (9, "https://drive.google.com/uc?export=download&id=1teUloMeLoUL0rmFB8chPP8s_3Z-FqS9S"),
    "P10-F8T3": (10, "https://drive.google.com/uc?export=download&id=1DcvcZWHkP2a_dKFNCV98hz9Qt_VxRHW5"),
    "P11-D4H7": (11, "https://drive.google.com/uc?export=download&id=1f6dvGlTO96A2kg_bwnDGVXtPpkPMvwCq"),
    "P12-Q2S9": (12, "https://drive.google.com/uc?export=download&id=1OTLXFVDUrEsB9thXRy2Km5hO6rDtvXPd"),
    "P13-L6P4": (13, "https://drive.google.com/uc?export=download&id=1cMCvgZF6-2bxbVfbarQWsZ9adnWTKS-h"),
    "P14-W5T1": (14, "https://drive.google.com/uc?export=download&id=1N-GQUAgNfMjWeVer72frL_-7it8HC9lt"),
    "P15-C8R2": (15, "https://drive.google.com/uc?export=download&id=1hYPVD2EdzqS_rwpUYnnOs9rpCVtaztvq"),
    "P16-N3M9": (16, "https://drive.google.com/uc?export=download&id=1sYboE9wuRqyHUtwfzA3aNG9dlx4CkJqI"),
    "P17-Y7K5": (17, "https://drive.google.com/uc?export=download&id=1ZlpwCzzBBSHOlec2JlqrvgPX_EHbUQLr"),
    "P18-E1G6": (18, "https://drive.google.com/uc?export=download&id=1YTzsizXI-xq1Nma5MAjfc03LxrYAUOtl"),
    "P19-H9J3": (19, "https://drive.google.com/uc?export=download&id=15sy6YfNkF5-UKmuyXqiJRTwSANJDfra_"),
    "P20-Z4V8": (20, "https://drive.google.com/uc?export=download&id=1qV8eZtsfiEYK6HMXtMSwksI0QWAK5t3E"),
    "P21-U2X7": (21, "https://drive.google.com/uc?export=download&id=1E_Qju9pXHnMK3W7IOHKRQBsDL3me554S"),
    "P22-S5N6": (22, "https://drive.google.com/uc?export=download&id=1SadB7nuMv9Urn7hiJDHnifIcS5UteLGp"),
    "P23-P8B1": (23, "https://drive.google.com/uc?export=download&id=1CkzNkrzMZTcNdEGsfL_35eyA1kHQLueM"),
    "P24-T3K9": (24, "https://drive.google.com/uc?export=download&id=1D3e__ebm6tcq8TZlCPZR6uQ8IMx0b6tw"),
    "P25-R6F4": (25, "https://drive.google.com/uc?export=download&id=1vJb3MkAxbCAzFVgYkC5Ew5loD5kC8DiL"),
    "P26-I7C2": (26, "https://drive.google.com/uc?export=download&id=1tcqUozp2VYb7aDvrmhOCkkv0DwRsnqR7"),
    "P27-O9D5": (27, "https://drive.google.com/uc?export=download&id=14CM57Fvgh6VXzrDh318-FXBsOU3R402I"),
    "P28-G1H8": (28, "https://drive.google.com/uc?export=download&id=10EmWt3R1UvEi4dy5x9ZddCUrjHI4bhuI"),
    "P29-A5W3": (29, "https://drive.google.com/uc?export=download&id=1h26zz5EjQ_QpPdbv_ZJGhSCChbe80-wo"),
    "P30-M2J6": (30, "https://drive.google.com/uc?export=download&id=1KvIlATodPDcqZEQYnmi-klNUg_LYZ65G"),
    "P31-B4Q7": (31, "https://drive.google.com/uc?export=download&id=1UF7hlyANsKfyv2TkauBYR0RyuyPgPNKQ"),
    "P32-V9L1": (32, "https://drive.google.com/uc?export=download&id=1jXWKxo2kAHuIxYyE0MQqA9eK5ii3bvj_"),
    "P33-K8P2": (33, "https://drive.google.com/uc?export=download&id=1Cg3OuXlnSG-rL1sMQnVuM_06qHDZH-7C"),
    "P34-X3S4": (34, "https://drive.google.com/uc?export=download&id=1vGSORF4nV63PkJ9oDSgyMBS1swiJ_H-P"),
    "P35-F6T5": (35, "https://drive.google.com/uc?export=download&id=15nlmMNYUoVz7Ilj-2qH-3XPuY4ol355q"),
    "P36-D7R9": (36, "https://drive.google.com/uc?export=download&id=1CFD1s8VFDLeXevs_G9rkBvOze9bCtTkp"),
    "P37-J2N8": (37, "https://drive.google.com/uc?export=download&id=1NRYW4_53pYdKa5rdH7Pec5Nxe2fbdbC_"),
    "P38-H1C3": (38, "https://drive.google.com/uc?export=download&id=13-NZX5fx-kCkOZXbffkIB71v-5ZO6YOi"),
    "P39-L5G7": (39, "https://drive.google.com/uc?export=download&id=1619ZYglW30cwDBQsG0Tml5Rl-SEvIMap"),
    "P40-Z8M4": (40, "https://drive.google.com/uc?export=download&id=1WMTLKI6rYamf1F2UdXNrVoZtL_vovPTJ"),
    "P41-Q9X2": (41, "https://drive.google.com/uc?export=download&id=1j-7xPclVxk0ATzOaZ12QZH1W4e934DYw"),
    "P42-W3F6": (42, "https://drive.google.com/uc?export=download&id=1Ms5PBx2RonypHfQfIXKyPkOFPlv68W-3"),
    "P43-C4B5": (43, "https://drive.google.com/uc?export=download&id=1KisilHhSoA8x1NmnQtxezNYX3-nVPsvK"),
    "P44-E7V1": (44, "https://drive.google.com/uc?export=download&id=1OoU0dKzo-OU8ge5qc6UZwDIYbGPflqBQ"),
    "P45-T8K9": (45, "https://drive.google.com/uc?export=download&id=1CBF8hBhyYKAjtLuNJVVhZpQbmlVuVUG_"),
    "P46-N2P6": (46, "https://drive.google.com/uc?export=download&id=1V-FavGMwPamEkTBnvCz16Lyu-lawOpy3"),
    "P47-R1S3": (47, "https://drive.google.com/uc?export=download&id=1TNTp8h3ab2ZmpxFRBt6FtsQYF29nAwxK"),
    "P48-U5D4": (48, "https://drive.google.com/uc?export=download&id=1EhhnoEfDzrSYtWTw4Sggz_hAThnbwKCD"),
    "P49-Y6H2": (49, "https://drive.google.com/uc?export=download&id=1AEYvi_TKQmWmONTtGgU3kcdjh8GTI9N-"),
    "P50-O3J7": (50, "https://drive.google.com/uc?export=download&id=1axpuYEdYoyky7miIRI3vL8dcL0OHsiXa"),
    "P51-I9G8": (51, "https://drive.google.com/uc?export=download&id=1uLPNKmJWUtWKK3-8AEDyd2p0YI1bpaDT"),
    "P52-A2L5": (52, "https://drive.google.com/uc?export=download&id=1fixdRKmjQjUNyg28bhdRKwB6XLiza-r_"),
    "P53-B8M1": (53, "https://drive.google.com/uc?export=download&id=1ufsSUsbRYxWUq0bm0tQmUXtL9c-F1rww"),
    "P54-S4X6": (54, "https://drive.google.com/uc?export=download&id=1N5Agt-7PUgW-Z0ahzSTJnYx2sY6YE2tO"),
    "P55-F5T3": (55, "https://drive.google.com/uc?export=download&id=1UYbp--yNBdsfTIXrPFxpF487MI5OLGBI"),
    "P56-D9R7": (56, "https://drive.google.com/uc?export=download&id=1c8ImOyc0i2FMpaNn4FCTIiPfFQoutuqT"),
    "P57-G2C4": (57, "https://drive.google.com/uc?export=download&id=17VYITFCL1fIv5KFI6dWkUOfZw_rYkq0w"),
    "P58-V1N8": (58, "https://drive.google.com/uc?export=download&id=1eiKMku2a8syF8mivnNCSnZ4nPZ_73wur"),
    "P59-P7K5": (59, "https://drive.google.com/uc?export=download&id=1N1eT8bQ8eW5M7WlZDJmIYzLcHQKQrnJJ"),
    "P60-Q6H9": (60, "https://drive.google.com/uc?export=download&id=1jH4t0QwL70niOfynnIZBf9DaqoWO_cR9"),
    "P61-M3B2": (61, "https://drive.google.com/uc?export=download&id=1XHyQIlRLmcxqXKq75QIhRdpOxWY2sPY6"),
    "P62-W4F1": (62, "https://drive.google.com/uc?export=download&id=1PlO18p0hunxAg_y44xv1_x0QokuzJKc8"),
    "P63-J8L6": (63, "https://drive.google.com/uc?export=download&id=1wMfkC0nwA2jWqNn6V0z-JZiHjckQ0siR"),
    "P64-T2S7": (64, "https://drive.google.com/uc?export=download&id=1yuqAFgWf4VFbKBPp5dXvcofz-r4sfqfl"),
    "P65-R5X3": (65, "https://drive.google.com/uc?export=download&id=1RT0AK0vK_AIXQcvxAd84tsTkZNosu_GD"),
    "P66-N9D4": (66, "https://drive.google.com/uc?export=download&id=1DEf746mIsFO_VsGaFQz2cECOOG8ewVwG"),
    "P67-K1G8": (67, "https://drive.google.com/uc?export=download&id=1UyR-liiuhqU9NF_LPNywpf8xH_7sOv7W"),
    "P68-H7P2": (68, "https://drive.google.com/uc?export=download&id=16ff1BIdjGS3Sk114kTlYvn50TKtST4Qj"),
    "P69-E3M5": (69, "https://drive.google.com/uc?export=download&id=1uRBYf5AIxuC8RiCIDFofjk6SPIW6fVU8"),
    "P70-C6V9": (70, "https://drive.google.com/uc?export=download&id=1-PI0Aw-5SIfI6XOQ090cAvaXH_jKG5k1"),
    "P71-Z2T1": (71, "https://drive.google.com/uc?export=download&id=1C-a4XwIgRHCXhWaTZABJ-JgHYCWrFd1Z"),
    "P72-U8B4": (72, "https://drive.google.com/uc?export=download&id=1WQ_MKdGG86XZeXuNwLx4WT0bqzYUS8a0"),
    "P73-Y4F6": (73, "https://drive.google.com/uc?export=download&id=1tQrGL-ou8ZGG7SqewN6Q_tvzYLSqeu7v"),
    "P74-O1S3": (74, "https://drive.google.com/uc?export=download&id=1UIANDECC9z23TIwOh1Qy5NCbDzOTlDQA"),
    "P75-L7J8": (75, "https://drive.google.com/uc?export=download&id=11aMoNScFKKRxUdQCFXJSL9O9Uot8ohox"),
    "P76-I5C9": (76, "https://drive.google.com/uc?export=download&id=1G-bOIf6a0U_VZJ41SjfidYV6cKthAxgx"),
    "P77-A9N2": (77, "https://drive.google.com/uc?export=download&id=1rS1evLYbIXYA7mMIFYu3l4fHjgjh1W6n"),
    "P78-B3R1": (78, "https://drive.google.com/uc?export=download&id=1NsGn5h4cr7PCqBRDiwlP4kdX7U8RKoTd"),
    "P79-D8K5": (79, "https://drive.google.com/uc?export=download&id=10z_wzPCQoEPQy5pSpDfKDgkIvIv-Nnmi"),
    "P80-Q4X7": (80, "https://drive.google.com/uc?export=download&id=1PO_P6yfIW0RRk37Ap7Lz8Ity_nQB6EdQ"),
    "P81-M6H3": (81, "https://drive.google.com/uc?export=download&id=1UAlBpeZ_bYrnmLm8ba_Cz94ai1Nf3lg_"),
    "P82-S1F9": (82, "https://drive.google.com/uc?export=download&id=1VeTAkx4ZhgeHDTTdixUckfu16XbxLOh4"),
    "P83-P2D6": (83, "https://drive.google.com/uc?export=download&id=16BJ3FeoREVNwtLGliJKGBoqg8emwwI65"),
    "P84-R7L4": (84, "https://drive.google.com/uc?export=download&id=1E9YeWN6xlJVHadh_tQ8XVXol8lvp66Fm"),
    "P85-V5T2": (85, "https://drive.google.com/uc?export=download&id=1SPmCUHYY7yJcY7gCLoXHQ3eGD518bj2i"),
    "P86-J3B8": (86, "https://drive.google.com/uc?export=download&id=1uWP4h3fCLbjCQp14dzH1QwvKFJOLi9AQ"),
    "P87-N4G1": (87, "https://drive.google.com/uc?export=download&id=1gn18RB-QoDmfyZRNfgCwdo4a_BxESGxT"),
    "P88-T9M7": (88, "https://drive.google.com/uc?export=download&id=1xIuiUJ53063gms4ruhndGjvdEGj3W5RJ"),
    "P89-C2S5": (89, "https://drive.google.com/uc?export=download&id=1MzBV2AckN_sevGVbxcCCn1_rb1-5BrQL"),
    "P90-H8X6": (90, "https://drive.google.com/uc?export=download&id=1YLnyjdNtU8DCPnzgIL1KjLSrXcuCou76"),
    "P91-E4R3": (91, "https://drive.google.com/uc?export=download&id=1DU1KJyBkkR7Anvsy53IGrQnk0ANqg7_a"),
    "P92-W1K9": (92, "https://drive.google.com/uc?export=download&id=1O6j9sOugzMK1gHhDRASLKWuZ6JHzcMrH"),
    "P93-F7P2": (93, "https://drive.google.com/uc?export=download&id=1NJKD9eVkdVBHYT657AGCkYWMzYFxkji7"),
    "P94-Z5D8": (94, "https://drive.google.com/uc?export=download&id=1n2HW51PYeGK9jzgYzkVCo543IgLRvxHV"),
    "P95-U9L4": (95, "https://drive.google.com/uc?export=download&id=1D_aa-rjs9RtzYrRR3qrELCeW3p54rCeh"),
    "P96-Y2B6": (96, "https://drive.google.com/uc?export=download&id=1OoLeBOghNpgH80zUhC8mAMSo-zney_i3"),
    "P97-O8C1": (97, "https://drive.google.com/uc?export=download&id=1oqN0NOCzw8pELXU9WKnv17_ApFIA7ABw"),
    "P98-L3N7": (98, "https://drive.google.com/uc?export=download&id=1RgAK5vug0tFxXhSQaGpnzPQbgQqkbE0K"),
    "P99-I6S9": (99, "https://drive.google.com/uc?export=download&id=1BqgBI9VnFuctRpXH2wH1rEooi09fyMFL"),
    "P100-K5J2": (100, "https://drive.google.com/uc?export=download&id=1LTS8ljrBztvkJNzgdx6fW5_HylLRTuCF")
}

# También mantener diccionario viejo para transición
ENLACES_PLANTILLAS = {num: enlace for comando, (num, enlace) in COMANDOS_PLANTILLAS.items()}

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

# 3. NUEVO MENSAJE DE BIENVENIDA PROFESIONAL CON PARÁMETRO
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Si viene con parámetro: /start P1-XR3F
    if len(message.text.split()) > 1:
        param = message.text.split()[1]
        
        # Si es un código de plantilla como P1-XR3F
        if param in COMANDOS_PLANTILLAS:
            num, enlace = COMANDOS_PLANTILLAS[param]
            respuesta = f"✅ **Plantilla {num}**\n{enlace}\n\n💡 _Ver video tutorial en YouTube_"
            bot.reply_to(message, respuesta, parse_mode='Markdown')
            return
        # Si es plantilla vieja: /start plantilla1
        elif param.startswith('plantilla'):
            try:
                num = int(param.replace('plantilla', ''))
                if num in ENLACES_PLANTILLAS:
                    respuesta = f"⚠️ *Sistema antiguo*\n\n"
                    respuesta += f"**Plantilla {num}**: {ENLACES_PLANTILLAS[num]}\n\n"
                    respuesta += "_Usa los botones en https://tesirve.com para códigos nuevos_"
                    bot.reply_to(message, respuesta, parse_mode='Markdown')
                    return
            except:
                pass
    
    # Mensaje normal de bienvenida (si no hay parámetro o no es reconocido)
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
    respuesta += "• `/P1-XR3F` - Descargar plantilla (código específico)\n\n"
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
