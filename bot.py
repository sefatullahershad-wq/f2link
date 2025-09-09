import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # آدرس Railway بدون / آخر

# فقط این دو کاربر اجازه دسترسی دارند
ALLOWED_USERS = [6174716282, 97608294]

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def is_allowed(user_id):
    return user_id in ALLOWED_USERS

@bot.message_handler(commands=['start', 'help'])
def start(message):
    if not is_allowed(message.from_user.id):
        bot.reply_to(
            message,
            f"⛔ شما اجازه استفاده از این ربات را ندارید.\n🆔 User ID: {message.from_user.id}"
        )
        return
    bot.reply_to(message, "سلام 👋\nفایل بفرست تا لینک مستقیم از سرور تلگرام بگیری.")

def send_file_link(message, file_id, file_name=None):
    if not is_allowed(message.from_user.id):
        bot.reply_to(
            message,
            f"⛔ شما اجازه استفاده از این ربات را ندارید.\n🆔 User ID: {message.from_user.id}"
        )
        return
    try:
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        text = f"📥 لینک دانلود مستقیم:\n{file_url}"
        if file_name:
            text = f"📄 {file_name}\n{text}"
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {e}")

# هندلر فایل‌ها
@bot.message_handler(content_types=['document'])
def document_handler(message):
    send_file_link(message, message.document.file_id, message.document.file_name)

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    largest = message.photo[-1]
    send_file_link(message, largest.file_id, "Photo")

@bot.message_handler(content_types=['video'])
def video_handler(message):
    send_file_link(message, message.video.file_id, message.video.file_name)

@bot.message_handler(content_types=['audio'])
def audio_handler(message):
    send_file_link(message, message.audio.file_id, message.audio.file_name)

@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    send_file_link(message, message.voice.file_id, "Voice")

# --- webhook ---
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8
