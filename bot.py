import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL")

def parse(text):
    try:
        parts = [x.strip() for x in text.split(",")]

        if len(parts) != 4:
            return None

        return {
            "text": text,
            "chat_id": None
        }
    except:
        return None


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id

    parts = [x.strip() for x in text.split(",")]

    if len(parts) != 4:
        await update.message.reply_text(
            "❌ Format salah!\nContoh:\nbudi , tas , 10.000 , 25.000"
        )
        return

    payload = {
        "text": text,
        "chat_id": chat_id
    }

    requests.post(APPS_SCRIPT_URL, json=payload)

    await update.message.reply_text("📨 Tersimpan ke Google Sheets!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot running...")
app.run_polling()
