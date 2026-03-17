import telebot
import random
import time
from flask import Flask
from threading import Thread

# سيرفر لإبقاء البوت نشطاً
app = Flask('')
@app.route('/')
def home(): return "البوت في الخدمة"
def run(): app.run(host='0.0.0.0', port=8080)

API_TOKEN = '8666840880:AAGNqOZEpz_mlgC_ME9H_GsbJEywoi6pnyU'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🎡 أهلاً بك. أنا جاهز لإجراء القرعة.\nأرسل الأسماء مفصولة بفاصلة ثم كلمة 'قرعة'.")

@bot.message_handler(func=lambda message: "قرعة" in message.text)
def spin_wheel(message):
    # تنظيف النص ومعالجة الفراغات والفاصلة العربية والإنجليزية
    raw_text = message.text.replace("قرعة", "").strip()
    # تقسيم الأسماء وتنظيف الفراغات حول كل اسم
    names = [n.strip() for n in raw_text.replace("،", ",").split(",") if n.strip()]
    
    if len(names) < 2:
        bot.reply_to(message, "يرجى إدخال اسمين على الأقل لإجراء القرعة.")
        return

    # إرسال الإيموجي المتحرك للعجلة (🎰 أو 🎲 أو 🎯)
    # تليجرام يستخدم send_dice لإرسال الإيموجيات المتحركة التفاعلية
    try:
        # الإيموجي 🎰 يظهر عجلة حظ تدور في تليجرام
        # يمكنك تجربة 🎲 (نرد) أو 🎯 (هدف) بدلاً منها
        msg = bot.send_dice(message.chat.id, emoji='🎰')
    except:
        # إذا لم يدعم تليجرام الإيموجي، نستخدم الرمز العادي
        msg = bot.send_message(message.chat.id, "جاري سحب الاسم... 🌀")

    # ننتظر قليلاً حتى تكتمل حركة الإيموجي (3-4 ثوانٍ)
    time.sleep(4)
    
    winner = random.choice(names)
    
    final_msg = (
        f"✨ **تمت القرعة بنجاح** ✨\n\n"
        f"وقع الاختيار على:\n"
        f"👑 【 **{winner}** 】\n\n"
        f"حظاً موفقاً للجميع في المرات القادمة. 🎈"
    )
    
    # نرد على رسالة الإيموجي بالنتيجة
    bot.reply_to(msg, final_msg, parse_mode="Markdown")

def start_bot():
    Thread(target=run).start()
    bot.polling(non_stop=True)

if __name__ == "__main__":
    start_bot()
