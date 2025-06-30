import os
import telebot
import gspread
from datetime import datetime, timedelta
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import base64
import json

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# CONFIGURAÇÃO DO GOOGLE SHEETS
cred_base64 = os.getenv("GOOGLE_CREDENTIALS_JSON_BASE64")
cred_dict = json.loads(base64.b64decode(cred_base64).decode("utf-8"))

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)
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
        data = (datetime.now() + timedelta(hours=-5)).strftime("%d/%m/%Y %H:%M")
        sheet.append_row([data, categoria.capitalize(), valor])
        bot.reply_to(message, f"✅ Gasto registrado: {categoria.capitalize()} - R$ {valor:.2f}")
        print(f"Mensagem recebida: {texto}")  # <- debug útil
    except Exception as e:
        print(f"Erro ao registrar gasto: {e}")  # <- mais útil ainda
        bot.reply_to(message, "❌ Formato inválido. Use: <categoria> <valor>\nEx: padaria 15.90")

# INICIA O BOT
bot.polling()
