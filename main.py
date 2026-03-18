import telebot
import random
import time
from flask import Flask
from threading import Thread

# سيرفر لإبقاء البوت نشطاً
app = Flask('')
@app.route('/')
def home(): return "البوت نشط"
def run(): app.run(host='0.0.0.0', port=8080)

API_TOKEN = '8666840880:AAGNqOZEpz_mlgC_ME9H_GsbJEywoi6pnyU'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🎡 أهلاً بكم! أنا جاهز لإجراء القرعة.\nأرسلوا الأسماء وبينهما فاصلة، ثم كلمة 'قرعة'. 🧸⚽")

@bot.message_handler(func=lambda message: "قرعة" in message.text)
def spin_wheel(message):
    chat_id = message.chat.id
    
    raw_text = message.text.replace("قرعة", "").strip()
    names = [n.strip() for n in raw_text.replace("،", ",").split(",") if n.strip()]
    
    if len(names) < 2:
        bot.reply_to(message, "أحتاج لاسمين على الأقل للبدء! 🎨")
        return

    try:
        # 1. إرسال عجلة الحظ
        msg = bot.send_dice(chat_id, emoji='🎰')
    except:
        msg = bot.send_message(chat_id, "جاري تدوير العجلة... 🌀")

    time.sleep(4) # انتظار توقف العجلة
    
    winner = random.choice(names)
    
    # 2. حذف رسالة العجلة لإفساح المجال للنتيجة
    try: bot.delete_message(chat_id, msg.message_id)
    except: pass
    
    # 3. إرسال اسم الفائز
    final_msg = (
        f"🎊 **الفائز الرائع هو** 🎊\n\n"
        f"👑✨  【 **{winner}** 】  ✨👑\n\n"
        f"مبارك لك الفوز! 🎈🧸🎨"
    )
    sent_msg = bot.send_message(chat_id, final_msg, parse_mode="Markdown")
    
    # 4. إضافة "Reaction" (تفاعل) القصاصات على الرسالة فوراً
    # هذا ما يجعل القصاصات "تندفع" من الرسالة للخارج كما وصفتِ تماماً
    try:
        bot.set_message_reaction(chat_id, sent_msg.message_id, [telebot.types.ReactionTypeEmoji("🎉")], is_big=True)
    except:
        # في حال كانت النسخة قديمة، يرسل إيموجي منفرد كبديل
        bot.send_message(chat_id, "🎉")

def start_bot():
    Thread(target=run).start()
    bot.polling(non_stop=True)

if __name__ == "__main__":
    start_bot()
