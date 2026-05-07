import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")
APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()
    chat_id = update.message.chat_id

    # DEBUG
    print("PESAN MASUK:", text)

    # ================= /OMSET =================
    if text.lower() == "/omset":

        print("COMMAND OMSET TERDETEKSI")

        payload = {
            "text": "/omset",
            "chat_id": chat_id
        }

        requests.post(APPS_SCRIPT_URL, json=payload)

        return

    # ================= FORMAT =================
    parts = text.split(" ")

    if len(parts) < 4:

        await update.message.reply_text(
            "❌ FORMAT BARU:\n"
            "budi tas 20.000 100.000"
        )

        return

    payload = {
        "text": text,
        "chat_id": chat_id
    }

    requests.post(APPS_SCRIPT_URL, json=payload)

    await update.message.reply_text(
        "✅ DATA BARU MASUK"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, handle)
)

print("BOT VERSI BARU OMSET AKTIF")

app.run_polling()
