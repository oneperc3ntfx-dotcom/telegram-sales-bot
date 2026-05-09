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


# ================= HANDLE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        text = update.message.text.strip()
        chat_id = update.message.chat_id

        print("PESAN SALES:", text)

        # ================= /OMSET =================
        if text.lower() == "/omset":

            requests.post(
                APPS_SCRIPT_URL,
                json={
                    "text": "/omset",
                    "chat_id": chat_id
                },
                timeout=10
            )

            return

        # ================= FORMAT CEK =================
        parts = text.split(" ")

        if len(parts) < 4:

            await update.message.reply_text(
                "❌ FORMAT SALAH!\n\n"
                "Contoh:\n"
                "budi tas 20.000 100.000"
            )

            return

        # ================= KIRIM KE APPS SCRIPT =================
        requests.post(
            APPS_SCRIPT_URL,
            json={
                "text": text,
                "chat_id": chat_id
            },
            timeout=10
        )

        await update.message.reply_text(
            "📨 DATA BERHASIL DIKIRIM"
        )

    except Exception as e:

        print("ERROR:", e)

        await update.message.reply_text(
            "⚠️ Server sedang sibuk, coba lagi."
        )


# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, handle)
)

print("SALES BOT AKTIF 🚀")

app.run_polling()
