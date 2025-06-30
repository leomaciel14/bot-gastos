import os
import telebot
import gspread
from datetime import datetime
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# CONFIGURAÇÃO DO GOOGLE SHEETS
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_path = os.getenv("GOOGLE_CREDENTIALS_JSON")
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(creds)
sheet = client.open("Controle de Gastos").sheet1

# TOKEN DO SEU BOT TELEGRAM
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# FUNÇÃO QUE TRATA TODAS AS MENSAGENS
@bot.message_handler(func=lambda message: True)
def registrar_gasto(message):
    try:
        texto = message.text.strip()
        categoria, valor = texto.rsplit(" ", 1)
        valor = float(valor.replace(",", "."))
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        sheet.append_row([data, categoria.capitalize(), valor])
        bot.reply_to(message, f"✅ Gasto registrado: {categoria.capitalize()} - R$ {valor:.2f}")
    except:
        bot.reply_to(message, "❌ Formato inválido. Use: <categoria> <valor>\nEx: padaria 15.90")

# INICIA O BOT
bot.polling()