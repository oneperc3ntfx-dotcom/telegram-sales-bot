import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime
from dotenv import load_dotenv

# ================= LOAD TOKEN =================
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

# ================= PARSER =================
def parse_message(text):
    parts = text.split()

    if len(parts) < 3:
        return None

    jenis = parts[0].lower()
    nominal = parts[1]

    if not nominal.isdigit():
        return None

    produk = " ".join(parts[2:])

    return jenis, nominal, produk

# ================= HANDLE MESSAGE =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    data = parse_message(text)

    if not data:
        await update.message.reply_text(
            "❌ Format salah\nContoh: jual 100000 nasi goreng"
        )
        return

    jenis, nominal, produk = data
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([waktu, jenis, nominal, produk])

    await update.message.reply_text("✅ Tersimpan ke Google Sheets")

# ================= RUN BOT =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running...")
app.run_polling()
