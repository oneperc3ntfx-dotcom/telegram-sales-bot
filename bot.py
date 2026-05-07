import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= ENV =================
TOKEN = os.getenv("BOT_TOKEN")
APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL")


# ================= HANDLE MESSAGE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()
    chat_id = update.message.chat_id

    # ================= COMMAND /OMSET =================
    if text.lower() == "/omset":

        payload = {
            "text": "/omset",
            "chat_id": chat_id
        }

        requests.post(APPS_SCRIPT_URL, json=payload)

        return

    # ================= FORMAT INPUT =================
    parts = text.split(" ")

    if len(parts) < 4:

        await update.message.reply_text(
            "❌ Format salah!\n\n"
            "Contoh:\n"
            "budi tas 20.000 100.000"
        )

        return

    # ================= KIRIM KE APPS SCRIPT =================
    payload = {
        "text": text,
        "chat_id": chat_id
    }

    requests.post(APPS_SCRIPT_URL, json=payload)

    # ================= BALASAN =================
    await update.message.reply_text(
        "✅ Data berhasil dikirim!"
    )


# ================= RUN BOT =================
app = ApplicationBuilder().token(TOKEN).build()

# PENTING:
# jangan pakai ~filters.COMMAND
app.add_handler(
    MessageHandler(filters.TEXT, handle)
)

print("Bot running...")

app.run_polling()
