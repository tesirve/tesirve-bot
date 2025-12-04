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
    4: "https://drive.google.com/file/d/1N9HLkcya5q7Ad5Y_1Dl8BHDfTD9KqXtl/view",
    5: "https://drive.google.com/file/d/1s8V2DSSUNBd2SukGOGDftN73kszZzxkV/view",
    6: "https://drive.google.com/file/d/1HHXXppKob2K6v_dqAlrkvFqOg-9bUnHA/view",
    7: "https://drive.google.com/file/d/1ldX7Gd2scJHhZ4OYs30JhKx3QLiJ8bmC/view",
    8: "https://drive.google.com/file/d/1og9A-nfT-z0oIsCcrImh2kqK7OX9i-nC/view",
    9: "https://drive.google.com/file/d/1gqg0Tcc9rrdt4EXInZSOznhAz5f_qivh/view",
    10: "https://drive.google.com/file/d/1QdIpsL33RazRkCN0rE8Xj27DgM7u5OXw/view",
    11: "https://drive.google.com/file/d/1eMQItlzMfAFkBrPx4nq1fMsJ5a2xVVVl/view",
    12: "https://drive.google.com/file/d/1WjLwGKh8Ff0WgDms-dMYsTvP7iB6uWxW/view",
    13: "https://drive.google.com/file/d/19x9AEnIh-P8B34_UXwS5fQYqPP_Dmjhw/view",
    14: "https://drive.google.com/file/d/1fsbQhDGD6itCSW8ljd6fdu93vXz4gOiq/view",
    15: "https://drive.google.com/file/d/1w1C9ClPDh8F2T1LQOZzQ1y63qL1VqMfA/view",
    16: "https://drive.google.com/file/d/1ekutGeBluEKB2N-vrAakL0sibUw4_nvE/view",
    17: "https://drive.google.com/file/d/1Shl_px8N2u_8lQkfy_V8Uu6B0qj4a00v/view",
    18: "https://drive.google.com/file/d/1nW2G3pIrrLM2Olgv7iPr4Ckl7HtYf0R_/view",
    19: "https://drive.google.com/file/d/1tf3cL1P8_tX7JDT__ypIDmUQ1eO68nHd/view",
    20: "https://drive.google.com/file/d/16ojz4MzmryMJjkGLT0rGIl66IJl0WStI/view",
    21: "https://drive.google.com/file/d/1c1vXo4bl7t_8AUaefSItl3hQgYrBB58Y/view",
    22: "https://drive.google.com/file/d/1C7icdQ1L1xXvI7z8fD8iHYpsCy1gqAG9/view",
    23: "https://drive.google.com/file/d/1EBeSmgI7hYtU-7M4W_44SLqS-T2Mc5rC/view",
    24: "https://drive.google.com/file/d/1VtQ3ELrKrhZ-UMf58hB5pY_p2WXlSzzL/view",
    25: "https://drive.google.com/file/d/1-1hKKCMCOQQfG9pzqwOg03ezc9f6cK6T/view",
    26: "https://drive.google.com/file/d/1ZaLglXZR5cpVrMYN_jGrYFzDr3lNk-IZ/view",
    27: "https://drive.google.com/file/d/1VMFq2VQqqQa2cNQe0sazwvLJ69BSfsUu/view",
    28: "https://drive.google.com/file/d/1AYFl5MqAqp_pk1Y_dlksW6x92qEQT5P9/view",
    29: "https://drive.google.com/file/d/1AfRhj1P_JgO0Xl9ySpzYpVbXz6d0FpDf/view",
    30: "https://drive.google.com/file/d/1oeknR1My4ckFgbAJf2beZPLM2Iqo5lWT/view",
    31: "https://drive.google.com/file/d/1GvqDovWJhQ0_NmQn62K9Cbm-pUZNWvZj/view",
    32: "https://drive.google.com/file/d/19Ox3BYEYB5ZfCNSz_pep9hAq-dI9v4V5/view",
    33: "https://drive.google.com/file/d/1cnfqJDRdgqG1nYQ6yxoNYNKBbFCkRKYU/view",
    34: "https://drive.google.com/file/d/18SVJ6HvF9qowxAn4sHax9NQDQWYFvX-v/view",
    35: "https://drive.google.com/file/d/10AvPdcADdFJ9Wfwx4J7ejl3t4nM4PVqa/view",
    36: "https://drive.google.com/file/d/1mmt85bNbp9QQOwT92_2N0q3VOVjqN6d5/view",
    37: "https://drive.google.com/file/d/1lPhhfg94vLq0B5d4qHSvVUo3P2btyrQz/view",
    38: "https://drive.google.com/file/d/1H9TqyVsvU7ZgPp02QLtIh-Z02C2UTyGk/view",
    39: "https://drive.google.com/file/d/1RSvB1TrH_t0e4nU4yfCobQ_NzGzyFe82/view",
    40: "https://drive.google.com/file/d/1O6iI0GsQCPMfbTnfzS3Y9s7l8bB2z7Hb/view",
    41: "https://drive.google.com/file/d/1OkqgMygjzNV-9ob23JN7XeYlCVt_CF4D/view",
    42: "https://drive.google.com/file/d/19T4JMVZ8bnyMxKtbhHjGfRQUXkIKU5DK/view",
    43: "https://drive.google.com/file/d/19otq1F8o8zvnXe-nGHr_YrHk3obpK4nS/view",
    44: "https://drive.google.com/file/d/1IEWu2NF5gAfucRouAJqE6n8R87CjAxfJ/view",
    45: "https://drive.google.com/file/d/1UAZoX9cltXYNkpy1b3qW6eOcSMCjAB7R/view",
    46: "https://drive.google.com/file/d/1hRre2E6BQuyXwKB1OYp1J5GipgI3psKq/view",
    47: "https://drive.google.com/file/d/1HzQYogQw7C5X5K9_Gj7lPjSwX7BP7tQb/view",
    48: "https://drive.google.com/file/d/1Snk_B3sDBqoZv5SCvDqCqy-bx61sID6w/view",
    49: "https://drive.google.com/file/d/1MeUQpMJISW6fHECf2bN9iqnQ04kEEn_n/view",
    50: "https://drive.google.com/file/d/10pWrO6n3e26DyH0iCSx62ShxP9dYdHYm/view",
    51: "https://drive.google.com/file/d/1C__hC1cv8a5-bqoRz5Em6H3YF1u2pBVT/view",
    52: "https://drive.google.com/file/d/1k7rC0wyCQxLT3h2Chm44OnIV9J2Y5o-G/view",
    53: "https://drive.google.com/file/d/1nj6U70q5XhYfSn0E-Z1HHX2iyvjR3tK5/view",
    54: "https://drive.google.com/file/d/11iQKq4l29iymoSHnyyFFAmB5AmGX8C-F/view",
    55: "https://drive.google.com/file/d/10LmDb4wU42KkW5V4xwh_4VVMKg51ynMU/view",
    56: "https://drive.google.com/file/d/1T4C8jUQ8f3x7VK7D8CNy2bOFdmpcv9f7/view",
    57: "https://drive.google.com/file/d/1LZQocslikJj-b4LtruPwV3YODkEwM4b6/view",
    58: "https://drive.google.com/file/d/11rgC46m8sE7h16b-JbUQwWV7A-DJ3fZP/view",
    59: "https://drive.google.com/file/d/1h3eY3DqWazfA6rK_DJ_PztA-y9bf-lR5/view",
    60: "https://drive.google.com/file/d/1j0ub3-Gbw8XJ8Ayz9J2yRr79Uss3Ie26/view",
    61: "https://drive.google.com/file/d/1Mbrw44VR0lnXp7cM8lHD4B-wnu-NuBz0/view",
    62: "https://drive.google.com/file/d/1p8qOvbYQyVQLr4K7ANqCwW9VRF2VJpS6/view",
    63: "https://drive.google.com/file/d/1Ac0y6enwQqy7dfgO2rT3a13Nzz2Dm5KP/view",
    64: "https://drive.google.com/file/d/1aRGQQ0Xh3b8mEWH0qoECv0v5Z1aQ3LxT/view",
    65: "https://drive.google.com/file/d/1CKWryR0EmSdOOTsTyDgy28ETVr-fUyQV/view",
    66: "https://drive.google.com/file/d/1CjN4Oc1V5_PSOJyTT-cDDHgsrcIxTQyX/view",
    67: "https://drive.google.com/file/d/1THCSBvFuvMMJFOX_HIh4Q19m7yaj7srd/view",
    68: "https://drive.google.com/file/d/1eH3ctwY2wzSFbZ6MBIs2lTUG8bZMBVJW/view",
    69: "https://drive.google.com/file/d/1T4ojEfGR13FljchNx9bGbtq3w8l5wNgH/view",
    70: "https://drive.google.com/file/d/1_7JYdSnb_UbTj6lEQbX92lxgC9bVFL8X/view",
    71: "https://drive.google.com/file/d/1YvuzqMx_EMUWeVz02QlC9-BGzhf6AV8t/view",
    72: "https://drive.google.com/file/d/1y8GpEpnAn8ru51WYLLTEGW58_Zk2kRkD/view",
    73: "https://drive.google.com/file/d/15Ab5yNfKMFcW1Dek0vqgLOn8U0_eX0rd/view",
    74: "https://drive.google.com/file/d/11FoS4QaNDW4U_MoQYhJMTaG6ygRr90W5/view",
    75: "https://drive.google.com/file/d/1Q7zPR9T2m8ZvNZZYIOVYdG8h7GByIktT/view",
    76: "https://drive.google.com/file/d/1lhfsLXJbJVQNipr2g-D0_b7E8JKmS-pN/view",
    77: "https://drive.google.com/file/d/19xr2NGJ-QSWj5GHD8A8xIx1xWwSpW-WO/view",
    78: "https://drive.google.com/file/d/1r14UR2kEoKf2lNQv7UJpb-3PLkPCLGfO/view",
    79: "https://drive.google.com/file/d/1WqJ7FFWqjSObmDh-qf0GgYF6ajaw7rq5/view",
    80: "https://drive.google.com/file/d/1fQWk88-OPNupCjgYJwYSIGmqoSUtFdDN/view",
    81: "https://drive.google.com/file/d/1W_S6A48FORe9BP3D0Ifoy_qB4i0SPbQD/view",
    82: "https://drive.google.com/file/d/1yj7R5k_gmMsPYQ5MS5JOGGQ_9C0duSdP/view",
    83: "https://drive.google.com/file/d/1RFfCFRN44i2us5G0usJ5L8W7IP4yXSKZ/view",
    84: "https://drive.google.com/file/d/1mzLbIyn7PTMqASF00vyuK0fD12gGTq8J/view",
    85: "https://drive.google.com/file/d/1S5_sBEPtUNUR7bT_CU_1m5kFc15FmXfe/view",
    86: "https://drive.google.com/file/d/1QIO-NSXXadN27DzDoh5RNP2Yql2Rc-4P/view",
    87: "https://drive.google.com/file/d/1jEh80nQnRjRfD8XpUmgABG3Mtfgg-nzZ/view",
    88: "https://drive.google.com/file/d/1u9jQw1t1zGJ_fr37YhPJ2lqQ2xxZ79_M/view",
    89: "https://drive.google.com/file/d/1QtV9TRJmUpp23MTUps6WQ-Jk3yImHsmX/view",
    90: "https://drive.google.com/file/d/1S-zg6-MpDgs7c0m_sOgHSIJWqI6Tzn3i/view",
    91: "https://drive.google.com/file/d/1iW_kM_2_ucR3_x-3h3sW_92-Q86tfY7R/view",
    92: "https://drive.google.com/file/d/1O-s2pnvOYayVp9D-8yLkssU9O12tHQqj/view",
    93: "https://drive.google.com/file/d/1JcTn2vqzyD4CjwhZNLr7WnEDhGQkfsGw/view",
    94: "https://drive.google.com/file/d/1TlFbMQo1yrHSr6ErcIE6ETM4NJCnN3Mh/view",
    95: "https://drive.google.com/file/d/18THgV0Dugmg8PH7Gsy1tPrI-93s_l3ru/view",
    96: "https://drive.google.com/file/d/1cB-73Yl8P-jIAQoRXQyYt-w_XEObWX-5/view",
    97: "https://drive.google.com/file/d/1Sx-yfL9aHdDEl4vq0JECaX-0ml16J47W/view",
    98: "https://drive.google.com/file/d/1cRqQeQdDL02GURvTTW-PP7nthwQxAM3t/view",
    99: "https://drive.google.com/file/d/1nwAJ3gSPyhp1W4M_r6wVU7H8Nq0DZJ8m/view",
    100: "https://drive.google.com/file/d/1dZxSeumvXgkyN4k2G0iZzSNpNZz3Ljez/view",
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
