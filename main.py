import telebot
import random
import time
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "البوت نشط"
def run(): app.run(host='0.0.0.0', port=8080)

API_TOKEN = '8666840880:AAGNqOZEpz_mlgC_ME9H_GsbJEywoi6pnyU'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🎡 أهلاً بكم في عجلة القرعة! أرسلوا الأسماء وبينهما فاصلة ثم كلمة 'قرعة'. 🧸🎨")

@bot.message_handler(func=lambda message: "قرعة" in message.text)
def spin_wheel(message):
    chat_id = message.chat.id
    
    raw_text = message.text.replace("قرعة", "").strip()
    names = [n.strip() for n in raw_text.replace("،", ",").split(",") if n.strip()]
    
    if len(names) < 2:
        bot.reply_to(message, "أحتاج لاسمين على الأقل للبدء! ⚽")
        return

    try:
        # 1. إرسال عجلة الحظ المتحركة
        msg = bot.send_dice(chat_id, emoji='🎰')
    except:
        msg = bot.send_message(chat_id, "جاري تدوير العجلة... 🌀")

    time.sleep(4) # انتظار توقف العجلة
    
    winner = random.choice(names)
    
    # 2. إرسال إيموجي منفرد لتفعيل "صوت الاحتفال وقصاصات الشاشة"
    # ملاحظة: يجب أن يكون الإيموجي وحيداً لتفعيل التأثير
    bot.send_message(chat_id, "🎉") 
    
    # 3. إرسال اسم الفائز بتنسيق مبهج للأطفال
    final_msg = (
        f"🎊 **الفائز الرائع هو** 🎊\n\n"
        f"👑✨  【 **{winner}** 】  ✨👑\n\n"
        f"مبارك لك الفوز! 🎈🧸🎨"
    )
    bot.send_message(chat_id, final_msg, parse_mode="Markdown")

def start_bot():
    Thread(target=run).start()
    bot.polling(non_stop=True)

if __name__ == "__main__":
    start_bot()
