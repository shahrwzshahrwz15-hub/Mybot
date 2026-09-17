import os
import telebot
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from deep_translator import GoogleTranslator
pyTelegramBotAPI
google-generativeai
yt-dlp
moviepy

BOT_TOKEN = "8640548442:AAG59mCYsBdVaCcDbLsAmiuL-3CNbIJtZno"
bot = telebot.TeleBot(BOT_TOKEN)
import google.generativeai as genai
genai.configure(api_key="AQ.Ab8RN6KNkjWdRjcHWA5ZA1cftFLeQQJMmhQkz7FJB_1ZNOkc-g")

signature = (
    "\n\n───────────────────\n"
    "👨‍💻 پەرەپێدراوە لەلایەن: **shahrwz kh** (وەرگێڕ)\n"
    "👑 سەرۆک | 👤 یۆزەرنەیم: @di1cc"
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 بەخێر هاتیت بۆ بۆتی وەرگێڕانی زیرەک!\n\n"
        "💬 **دەتوانیت:**\n"
        "1️⃣ دەق بنێریت بۆ وەرگێڕان.\n"
        "2️⃣ **ڤیدیۆ** بنێریت بۆ ئەوەی قسەکانی ناوەوه‌ی بکەمە دەق و وەریانگێڕم بۆ **سۆرانی و بادینی**!"
        f"{signature}"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# مامەڵەکردن لەگەڵ ناردنی ڤیدیۆ
@bot.message_handler(content_types=['video'])
def handle_video(message):
    processing_msg = bot.reply_to(message, "⏳ ڤیدیۆکە وەرگیرا، خەریکی دەرهێنانی دەنگ و گۆڕینی بۆ دەقم...")

    video_path = f"video_{message.chat.id}.mp4"
    audio_path = f"audio_{message.chat.id}.wav"

    try:
        # داگرتنی ڤیدیۆ لە تێلیگرام
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(video_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # جیاکردنەوەی دەنگ لە ڤیدیۆ
        video_clip = VideoFileClip(video_path)
        if video_clip.audio is not None:
            video_clip.audio.write_audiofile(audio_path, codec='pcm_s16le', logger=None)
        video_clip.close()

        # گۆڕینی دەنگ بۆ دەق (Speech to Text)
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
            extracted_text = r.recognize_google(audio_data)

        bot.edit_message_text("🔄 دەقەکە دۆزرایەوە، خەریکی وەرگێڕانیم بۆ سۆرانی و بادینی...", message.chat.id, processing_msg.message_id)

        # وەرگێڕان بۆ سۆرانی و بادینی
        sorani = GoogleTranslator(source='auto', target='ku').translate(extracted_text)
        badini = GoogleTranslator(source='auto', target='kmr').translate(extracted_text)

        response_text = (
            f"🎬 **ئەنجامی پڕۆسێسی ڤیدیۆ:**\n\n"
            f"📝 **دەقی دۆزراوە لە ڤیدیۆکە:**\n{extracted_text}\n\n"
            f"💬 **کوردی (سۆرانی):**\n{sorani}\n\n"
            f"💬 **کوردی (بادینی):**\n{badini}"
            f"{signature}"
        )
        bot.edit_message_text(response_text, message.chat.id, processing_msg.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.edit_message_text(f"❌ هەڵە ڕووی دا یان دەنگ لە ڤیدیۆکەدا نەبوو: {str(e)}{signature}", message.chat.id, processing_msg.message_id, parse_mode="Markdown")

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

# وەرگێڕانی ئاسایی دەق
@bot.message_handler(func=lambda message: True)
def translate_text(message):
    text_to_translate = message.text
    if not text_to_translate or text_to_translate.startswith('/'):
        return

    processing_msg = bot.reply_to(message, "⚡ خەریکی وەرگێڕانم...")

    try:
        sorani = GoogleTranslator(source='auto', target='ku').translate(text_to_translate)
        badini = GoogleTranslator(source='auto', target='kmr').translate(text_to_translate)

        response_text = (
            f"🌐 **ئەنجامی وەرگێڕان:**\n\n"
            f"📄 **دەقی ڕەسەن:**\n{text_to_translate}\n\n"
            f"💬 **کوردی (سۆرانی):**\n{sorani}\n\n"
            f"💬 **کوردی (بادینی):**\n{badini}"
            f"{signature}"
        )
        bot.edit_message_text(response_text, message.chat.id, processing_msg.message_id, parse_mode="Markdown")
    except Exception as e:
        bot.edit_message_text(f"❌ هەڵە ڕووی دا: {str(e)}{signature}", message.chat.id, processing_msg.message_id, parse_mode="Markdown")

print("Bot with Video & Text translation is running 24/7...")
bot.infinity_polling()
