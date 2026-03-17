import telebot
import random
import time
from flask import Flask
from threading import Thread

# سيرفر بسيط لإرضاء Render
app = Flask('')
@app.route('/')
def home(): return "البوت نشط!"
def run(): app.run(host='0.0.0.0', port=8080)

API_TOKEN = '8666840880:AAGNqOZEpz_mlgC_ME9H_GsbJEywoi6pnyU'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🎡 أهلاً بكم في عجلة الحظ السعيدة! ✨\n\nأرسلوا الأسماء وبينهما فاصلة، ثم أتبعوها بكلمة 'قرعة'.\nمثال: أحمد، سارة، ليلى قرعة")

@bot.message_handler(func=lambda message: "قرعة" in message.text)
def spin_wheel(message):
    raw_text = message.text.replace("قرعة", "").strip()
    names = [n.strip() for n in raw_text.replace("،", ",").split(",") if n.strip()]
    
    if len(names) < 2:
        bot.reply_to(message, "🎡 أوه! أحتاج لاسمين على الأقل لتدور العجلة!")
        return

    # إرسال صورة متحركة لعجلة تدور (رابط مباشر)
    wheel_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJic2R6ZzRyc2R6ZzRyc2R6ZzRyc2R6ZzRyc2R6ZzRyc2R6ZzR5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l3vR6pE7p7p7p7p7p7/giphy.gif"
    msg = bot.send_animation(message.chat.id, wheel_gif, caption="🌀 العجلة تدور الآن... ترقبوا الحظ!")

    time.sleep(4) # وقت دوران العجلة
    
    winner = random.choice(names)
    
    # مسح رسالة العجلة وإرسال الفائز
    bot.delete_message(message.chat.id, msg.message_id)
    
    final_msg = (
        f"🎊🎉 **مباااااارك الفوز!** 🎉🎊\n\n"
        f"🎡 العجلة اختارت الصديق(ة):\n"
        f"✨💎 **【 {winner} 】** 💎✨\n\n"
        f"🎈🧸 حظاً أوفر للبقية في المرة القادمة!"
    )
    bot.send_message(message.chat.id, final_msg, parse_mode="Markdown")

def start_bot():
    Thread(target=run).start()
    bot.polling(non_stop=True)

if __name__ == "__main__":
    start_bot()
