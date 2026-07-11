import os
import requests

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL")


# ==========================================
# HANDLE MESSAGE
# ==========================================

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        if update.message is None:
            return

        text = update.message.text.strip()
        chat_id = update.message.chat_id

        print(f"[PESAN] {text}")

        parts = text.split()

        # ==========================
        # PERINTAH
        # ==========================

        if text.lower() in [
            "/hari",
            "/bulan",
            "/omset",
            "/help"
        ]:

            requests.post(
                APPS_SCRIPT_URL,
                json={
                    "text": text,
                    "chat_id": chat_id
                },
                timeout=20
            )

            return

        # ==========================
        # BELANJA
        # ==========================

        if len(parts) > 0 and parts[0].lower() == "belanja":

            if len(parts) != 3:

                await update.message.reply_text(

"""❌ FORMAT SALAH

Contoh

Belanja 15tas 2000000"""
                )

                return

        # ==========================
        # PENJUALAN
        # ==========================

        else:

            if len(parts) != 3:

                await update.message.reply_text(

"""❌ FORMAT SALAH

Contoh

budi tasLV 250000"""
                )

                return

        # ==========================
        # KIRIM KE APPS SCRIPT
        # ==========================

        response = requests.post(

            APPS_SCRIPT_URL,

            json={
                "text": text,
                "chat_id": chat_id
            },

            timeout=20

        )

        if response.status_code != 200:

            await update.message.reply_text(
                "⚠️ Gagal menghubungi server."
            )

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "⚠️ Server sedang sibuk."
        )


# ==========================================
# MAIN
# ==========================================

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(

        MessageHandler(

            filters.TEXT & ~filters.COMMAND,

            handle

        )

    )

    app.add_handler(

        MessageHandler(

            filters.Regex(r"^/(hari|bulan|omset|help)$"),

            handle

        )

    )

    print("===================================")
    print(" SALES BOT BERJALAN 🚀")
    print("===================================")

    app.run_polling()


if __name__ == "__main__":
    main()
