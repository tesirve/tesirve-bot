import os
import telebot
from flask import Flask, request
from telebot.types import Update

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# TODAS LAS 100 PLANTILLAS
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
    "p11-d4h7": "https://drive.google.com/uc?export=download&id=1f6dvGlTO96A2kg_bwnDGVXtPpkPMvwCq",
    "p12-q2s9": "https://drive.google.com/uc?export=download&id=1OTLXFVDUrEsB9thXRy2Km5hO6rDtvXPd",
    "p13-l6p4": "https://drive.google.com/uc?export=download&id=1cMCvgZF6-2bxbVfbarQWsZ9adnWTKS-h",
    "p14-w5t1": "https://drive.google.com/uc?export=download&id=1N-GQUAgNfMjWeVer72frL_-7it8HC9lt",
    "p15-c8r2": "https://drive.google.com/uc?export=download&id=1hYPVD2EdzqS_rwpUYnnOs9rpCVtaztvq",
    "p16-n3m9": "https://drive.google.com/uc?export=download&id=1sYboE9wuRqyHUtwfzA3aNG9dlx4CkJqI",
    "p17-y7k5": "https://drive.google.com/uc?export=download&id=1ZlpwCzzBBSHOlec2JlqrvgPX_EHbUQLr",
    "p18-e1g6": "https://drive.google.com/uc?export=download&id=1YTzsizXI-xq1Nma5MAjfc03LxrYAUOtl",
    "p19-h9j3": "https://drive.google.com/uc?export=download&id=15sy6YfNkF5-UKmuyXqiJRTwSANJDfra_",
    "p20-z4v8": "https://drive.google.com/uc?export=download&id=1qV8eZtsfiEYK6HMXtMSwksI0QWAK5t3E",
    "p21-u2x7": "https://drive.google.com/uc?export=download&id=1E_Qju9pXHnMK3W7IOHKRQBsDL3me554S",
    "p22-s5n6": "https://drive.google.com/uc?export=download&id=1SadB7nuMv9Urn7hiJDHnifIcS5UteLGp",
    "p23-p8b1": "https://drive.google.com/uc?export=download&id=1CkzNkrzMZTcNdEGsfL_35eyA1kHQLueM",
    "p24-t3k9": "https://drive.google.com/uc?export=download&id=1D3e__ebm6tcq8TZlCPZR6uQ8IMx0b6tw",
    "p25-r6f4": "https://drive.google.com/uc?export=download&id=1vJb3MkAxbCAzFVgYkC5Ew5loD5kC8DiL",
    "p26-i7c2": "https://drive.google.com/uc?export=download&id=1tcqUozp2VYb7aDvrmhOCkkv0DwRsnqR7",
    "p27-o9d5": "https://drive.google.com/uc?export=download&id=14CM57Fvgh6VXzrDh318-FXBsOU3R402I",
    "p28-g1h8": "https://drive.google.com/uc?export=download&id=10EmWt3R1UvEi4dy5x9ZddCUrjHI4bhuI",
    "p29-a5w3": "https://drive.google.com/uc?export=download&id=1h26zz5EjQ_QpPdbv_ZJGhSCChbe80-wo",
    "p30-m2j6": "https://drive.google.com/uc?export=download&id=1KvIlATodPDcqZEQYnmi-klNUg_LYZ65G",
    "p31-b4q7": "https://drive.google.com/uc?export=download&id=1UF7hlyANsKfyv2TkauBYR0RyuyPgPNKQ",
    "p32-v9l1": "https://drive.google.com/uc?export=download&id=1jXWKxo2kAHuIxYyE0MQqA9eK5ii3bvj_",
    "p33-k8p2": "https://drive.google.com/uc?export=download&id=1Cg3OuXlnSG-rL1sMQnVuM_06qHDZH-7C",
    "p34-x3s4": "https://drive.google.com/uc?export=download&id=1vGSORF4nV63PkJ9oDSgyMBS1swiJ_H-P",
    "p35-f6t5": "https://drive.google.com/uc?export=download&id=15nlmMNYUoVz7Ilj-2qH-3XPuY4ol355q",
    "p36-d7r9": "https://drive.google.com/uc?export=download&id=1CFD1s8VFDLeXevs_G9rkBvOze9bCtTkp",
    "p37-j2n8": "https://drive.google.com/uc?export=download&id=1NRYW4_53pYdKa5rdH7Pec5Nxe2fbdbC_",
    "p38-h1c3": "https://drive.google.com/uc?export=download&id=13-NZX5fx-kCkOZXbffkIB71v-5ZO6YOi",
    "p39-l5g7": "https://drive.google.com/uc?export=download&id=1619ZYglW30cwDBQsG0Tml5Rl-SEvIMap",
    "p40-z8m4": "https://drive.google.com/uc?export=download&id=1WMTLKI6rYamf1F2UdXNrVoZtL_vovPTJ",
    "p41-q9x2": "https://drive.google.com/uc?export=download&id=1j-7xPclVxk0ATzOaZ12QZH1W4e934DYw",
    "p42-w3f6": "https://drive.google.com/uc?export=download&id=1Ms5PBx2RonypHfQfIXKyPkOFPlv68W-3",
    "p43-c4b5": "https://drive.google.com/uc?export=download&id=1KisilHhSoA8x1NmnQtxezNYX3-nVPsvK",
    "p44-e7v1": "https://drive.google.com/uc?export=download&id=1OoU0dKzo-OU8ge5qc6UZwDIYbGPflqBQ",
    "p45-t8k9": "https://drive.google.com/uc?export=download&id=1CBF8hBhyYKAjtLuNJVVhZpQbmlVuVUG_",
    "p46-n2p6": "https://drive.google.com/uc?export=download&id=1V-FavGMwPamEkTBnvCz16Lyu-lawOpy3",
    "p47-r1s3": "https://drive.google.com/uc?export=download&id=1TNTp8h3ab2ZmpxFRBt6FtsQYF29nAwxK",
    "p48-u5d4": "https://drive.google.com/uc?export=download&id=1EhhnoEfDzrSYtWTw4Sggz_hAThnbwKCD",
    "p49-y6h2": "https://drive.google.com/uc?export=download&id=1AEYvi_TKQmWmONTtGgU3kcdjh8GTI9N-",
    "p50-o3j7": "https://drive.google.com/uc?export=download&id=1axpuYEdYoyky7miIRI3vL8dcL0OHsiXa",
    "p51-i9g8": "https://drive.google.com/uc?export=download&id=1uLPNKmJWUtWKK3-8AEDyd2p0YI1bpaDT",
    "p52-a2l5": "https://drive.google.com/uc?export=download&id=1fixdRKmjQjUNyg28bhdRKwB6XLiza-r_",
    "p53-b8m1": "https://drive.google.com/uc?export=download&id=1ufsSUsbRYxWUq0bm0tQmUXtL9c-F1rww",
    "p54-s4x6": "https://drive.google.com/uc?export=download&id=1N5Agt-7PUgW-Z0ahzSTJnYx2sY6YE2tO",
    "p55-f5t3": "https://drive.google.com/uc?export=download&id=1UYbp--yNBdsfTIXrPFxpF487MI5OLGBI",
    "p56-d9r7": "https://drive.google.com/uc?export=download&id=1c8ImOyc0i2FMpaNn4FCTIiPfFQoutuqT",
    "p57-g2c4": "https://drive.google.com/uc?export=download&id=17VYITFCL1fIv5KFI6dWkUOfZw_rYkq0w",
    "p58-v1n8": "https://drive.google.com/uc?export=download&id=1eiKMku2a8syF8mivnNCSnZ4nPZ_73wur",
    "p59-p7k5": "https://drive.google.com/uc?export=download&id=1N1eT8bQ8eW5M7WlZDJmIYzLcHQKQrnJJ",
    "p60-q6h9": "https://drive.google.com/uc?export=download&id=1jH4t0QwL70niOfynnIZBf9DaqoWO_cR9",
    "p61-m3b2": "https://drive.google.com/uc?export=download&id=1XHyQIlRLmcxqXKq75QIhRdpOxWY2sPY6",
    "p62-w4f1": "https://drive.google.com/uc?export=download&id=1PlO18p0hunxAg_y44xv1_x0QokuzJKc8",
    "p63-j8l6": "https://drive.google.com/uc?export=download&id=1wMfkC0nwA2jWqNn6V0z-JZiHjckQ0siR",
    "p64-t2s7": "https://drive.google.com/uc?export=download&id=1yuqAFgWf4VFbKBPp5dXvcofz-r4sfqfl",
    "p65-r5x3": "https://drive.google.com/uc?export=download&id=1RT0AK0vK_AIXQcvxAd84tsTkZNosu_GD",
    "p66-n9d4": "https://drive.google.com/uc?export=download&id=1DEf746mIsFO_VsGaFQz2cECOOG8ewVwG",
    "p67-k1g8": "https://drive.google.com/uc?export=download&id=1UyR-liiuhqU9NF_LPNywpf8xH_7sOv7W",
    "p68-h7p2": "https://drive.google.com/uc?export=download&id=16ff1BIdjGS3Sk114kTlYvn50TKtST4Qj",
    "p69-e3m5": "https://drive.google.com/uc?export=download&id=1uRBYf5AIxuC8RiCIDFofjk6SPIW6fVU8",
    "p70-c6v9": "https://drive.google.com/uc?export=download&id=1-PI0Aw-5SIfI6XOQ090cAvaXH_jKG5k1",
    "p71-z2t1": "https://drive.google.com/uc?export=download&id=1C-a4XwIgRHCXhWaTZABJ-JgHYCWrFd1Z",
    "p72-u8b4": "https://drive.google.com/uc?export=download&id=1WQ_MKdGG86XZeXuNwLx4WT0bqzYUS8a0",
    "p73-y4f6": "https://drive.google.com/uc?export=download&id=1tQrGL-ou8ZGG7SqewN6Q_tvzYLSqeu7v",
    "p74-o1s3": "https://drive.google.com/uc?export=download&id=1UIANDECC9z23TIwOh1Qy5NCbDzOTlDQA",
    "p75-l7j8": "https://drive.google.com/uc?export=download&id=11aMoNScFKKRxUdQCFXJSL9O9Uot8ohox",
    "p76-i5c9": "https://drive.google.com/uc?export=download&id=1G-bOIf6a0U_VZJ41SjfidYV6cKthAxgx",
    "p77-a9n2": "https://drive.google.com/uc?export=download&id=1rS1evLYbIXYA7mMIFYu3l4fHjgjh1W6n",
    "p78-b3r1": "https://drive.google.com/uc?export=download&id=1NsGn5h4cr7PCqBRDiwlP4kdX7U8RKoTd",
    "p79-d8k5": "https://drive.google.com/uc?export=download&id=10z_wzPCQoEPQy5pSpDfKDgkIvIv-Nnmi",
    "p80-q4x7": "https://drive.google.com/uc?export=download&id=1PO_P6yfIW0RRk37Ap7Lz8Ity_nQB6EdQ",
    "p81-m6h3": "https://drive.google.com/uc?export=download&id=1UAlBpeZ_bYrnmLm8ba_Cz94ai1Nf3lg_",
    "p82-s1f9": "https://drive.google.com/uc?export=download&id=1VeTAkx4ZhgeHDTTdixUckfu16XbxLOh4",
    "p83-p2d6": "https://drive.google.com/uc?export=download&id=16BJ3FeoREVNwtLGliJKGBoqg8emwwI65",
    "p84-r7l4": "https://drive.google.com/uc?export=download&id=1E9YeWN6xlJVHadh_tQ8XVXol8lvp66Fm",
    "p85-v5t2": "https://drive.google.com/uc?export=download&id=1SPmCUHYY7yJcY7gCLoXHQ3eGD518bj2i",
    "p86-j3b8": "https://drive.google.com/uc?export=download&id=1uWP4h3fCLbjCQp14dzH1QwvKFJOLi9AQ",
    "p87-n4g1": "https://drive.google.com/uc?export=download&id=1gn18RB-QoDmfyZRNfgCwdo4a_BxESGxT",
    "p88-t9m7": "https://drive.google.com/uc?export=download&id=1xIuiUJ53063gms4ruhndGjvdEGj3W5RJ",
    "p89-c2s5": "https://drive.google.com/uc?export=download&id=1MzBV2AckN_sevGVbxcCCn1_rb1-5BrQL",
    "p90-h8x6": "https://drive.google.com/uc?export=download&id=1YLnyjdNtU8DCPnzgIL1KjLSrXcuCou76",
    "p91-e4r3": "https://drive.google.com/uc?export=download&id=1DU1KJyBkkR7Anvsy53IGrQnk0ANqg7_a",
    "p92-w1k9": "https://drive.google.com/uc?export=download&id=1O6j9sOugzMK1gHhDRASLKWuZ6JHzcMrH",
    "p93-f7p2": "https://drive.google.com/uc?export=download&id=1NJKD9eVkdVBHYT657AGCkYWMzYFxkji7",
    "p94-z5d8": "https://drive.google.com/uc?export=download&id=1n2HW51PYeGK9jzgYzkVCo543IgLRvxHV",
    "p95-u9l4": "https://drive.google.com/uc?export=download&id=1D_aa-rjs9RtzYrRR3qrELCeW3p54rCeh",
    "p96-y2b6": "https://drive.google.com/uc?export=download&id=1OoLeBOghNpgH80zUhC8mAMSo-zney_i3",
    "p97-o8c1": "https://drive.google.com/uc?export=download&id=1oqN0NOCzw8pELXU9WKnv17_ApFIA7ABw",
    "p98-l3n7": "https://drive.google.com/uc?export=download&id=1RgAK5vug0tFxXhSQaGpnzPQbgQqkbE0K",
    "p99-i6s9": "https://drive.google.com/uc?export=download&id=1BqgBI9VnFuctRpXH2wH1rEooi09fyMFL",
    "p100-k5j2": "https://drive.google.com/uc?export=download&id=1LTS8ljrBztvkJNzgdx6fW5_HylLRTuCF"
}

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# UN SOLO HANDLER PARA TODO
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    texto = message.text.strip().lower()
    
    # Si es un comando con / (ej: /p1-xr3f)
    if texto.startswith('/'):
        comando = texto[1:]  # Quitar el /
        
        if comando in PLANTILLAS:
            enlace = PLANTILLAS[comando]
            respuesta = f"Plantilla {comando.upper()}\n\n🔗 {enlace}"
            bot.reply_to(message, respuesta, parse_mode='Markdown')
            return
    
    # Si es /start con parámetro (ej: /start p1-xr3f)
    if texto.startswith('/start '):
        partes = texto.split()
        if len(partes) > 1:
            codigo = partes[1]
            if codigo in PLANTILLAS:
                enlace = PLANTILLAS[codigo]
                respuesta = f"Plantilla {codigo.upper()}\n\n🔗 {enlace}"
                bot.reply_to(message, respuesta, parse_mode='Markdown')
                return
    
    # Si es solo el código sin / (ej: p1-xr3f)
    if texto in PLANTILLAS:
        enlace = PLANTILLAS[texto]
        respuesta = f"Plantilla {texto.upper()}\n\n🔗 {enlace}"
        bot.reply_to(message, respuesta, parse_mode='Markdown')
        return
    
    # Si es solo /start
    if texto == '/start':
        bot.reply_to(message, "Envía /p1-xr3f para descargar plantillas")
        return
    
    # Si no es ninguna de las anteriores, no responder (mantiene el silencio)

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
    return 'Bot funcionando - 100 plantillas disponibles'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
