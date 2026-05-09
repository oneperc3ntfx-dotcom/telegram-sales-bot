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

SALES_SCRIPT_URL = os.getenv("SALES_SCRIPT_URL")
EXPENSE_SCRIPT_URL = os.getenv("EXPENSE_SCRIPT_URL")


# ================= HANDLE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        text = update.message.text.strip()
        chat_id = update.message.chat_id

        print("PESAN:", text)

        lower = text.lower()

        # ================= PENGELUARAN =================
        if (
            lower.startswith("keluar ")
            or lower == "/pengeluaran"
            or lower == "/total"
        ):

            print("KE EXPENSE SHEET")

            requests.post(
                EXPENSE_SCRIPT_URL,
                json={
                    "text": text,
                    "chat_id": chat_id
                },
                timeout=10
            )

            return

        # ================= SALES =================
        print("KE SALES SHEET")

        requests.post(
            SALES_SCRIPT_URL,
            json={
                "text": text,
                "chat_id": chat_id
            },
            timeout=10
        )

    except Exception as e:

        print("ERROR:", e)

        await update.message.reply_text(
            "⚠️ Server sibuk."
        )


# ================= RUN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, handle)
)

print("BOT 2 SHEET AKTIF 🚀")

app.run_polling()
