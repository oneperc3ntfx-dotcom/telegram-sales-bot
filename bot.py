import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime
from dotenv import load_dotenv

# ================= TOKEN =================
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# ================= GOOGLE SHEETS =================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("SalesBot").sheet1

# ================= PARSE MESSAGE =================
def parse_message(text):
    """
    Format:
    nama | produk | modal | harga
    """

    try:
        parts = [x.strip() for x in text.split("|")]

        if len(parts) != 4:
            return None

        nama = parts[0]
        produk = parts[1]
        modal = int(parts[2])
        harga = int(parts[3])

        return nama, produk, modal, harga

    except:
        return None


# ================= HANDLER =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    data = parse_message(text)

    if not data:
        await update.message.reply_text(
            "❌ Format salah!\nContoh:\nBudi | Nasi Goreng | 15000 | 25000"
        )
        return

    nama, produk, modal, harga = data

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keuntungan = harga - modal

    # ================= SAVE TO SHEET =================
    sheet.append_row([
        waktu,
        nama,
        produk,
        modal,
        harga,
        keuntungan
    ])

    await update.message.reply_text(
        f"✅ Tersimpan!\nUntung: {keuntungan}"
    )


# ================= RUN BOT =================
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running...")
app.run_polling()
