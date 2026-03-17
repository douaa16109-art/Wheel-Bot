import telebot
import random
import time
from flask import Flask
from threading import Thread

# سيرفر لإبقاء البوت متصلاً
app = Flask('')
@app.route('/')
def home(): return "البوت في الخدمة"
def run(): app.run(host='0.0.0.0', port=8080)

API_TOKEN = '8666840880:AAGNqOZEpz_mlgC_ME9H_GsbJEywoi6pnyU'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🎡 أهلاً بك! أنا جاهز لإجراء القرعة في هذه المجموعة.\nأرسل الأسماء وبينهما فاصلة، ثم أتبعوها بكلمة 'قرعة'.\nمثال: أحمد، سارة، ليلى قرعة")

@bot.message_handler(func=lambda message: "قرعة" in message.text)
def spin_wheel(message):
    chat_id = message.chat.id
    
    # تنظيف النص ومعالجة الفراغات والفاصلة العربية والإنجليزية
    raw_text = message.text.replace("قرعة", "").strip()
    names = [n.strip() for n in raw_text.replace("،", ",").split(",") if n.strip()]
    
    if len(names) < 2:
        bot.reply_to(message, "🎡 أوه! أحتاج لاسمين على الأقل لتدور العجلة!")
        return

    try:
        # إرسال إيموجي العجلة (🎰) الخاص بتليجرام
        msg = bot.send_dice(chat_id, emoji='🎰')
    except:
        msg = bot.send_message(chat_id, "جاري سحب الاسم... 🌀")

    # انتظار حركة العجلة
    time.sleep(4)
    
    winner = random.choice(names)
    
    # رسالة الفائز مع إيموجي الاحتفال (🎉) في البداية
    # تليجرام سيعرض القصاصات الورقية (Confetti) عند عرض الإيموجي في بداية الرسالة
    final_msg = (
        f"🎉 **مبرووووووك الفوز!** 🎉\n\n"
        f"🎡 وقع الاختيار على:\n"
        f"👑💎 【 **{winner}** 】 💎👑\n\n"
        f"حظاً موفقاً للبقية. 🎈🧸"
    )
    
    # الرد على رسالة العجلة النتيجة
    # تليجرام سيعرض القصاصات الورقية (Confetti) تلقائياً عند عرض الرسالة
    bot.reply_to(msg, final_msg, parse_mode="Markdown")

def start_bot():
    Thread(target=run).start()
    bot.polling(non_stop=True)

if __name__ == "__main__":
    start_bot()
