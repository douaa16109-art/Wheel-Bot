import telebot
import random
import time
from flask import Flask
from threading import Thread

# سيرفر بسيط لإبقاء البوت مستيقظاً على Render
app = Flask('')
@app.route('/')
def home(): return "البوت يعمل بنجاح!"
def run(): app.run(host='0.0.0.0', port=8080)

# التوكن الخاص ببوت العجلة
API_TOKEN = '8666840880:AAGNqOZEpz_mlgC_ME9H_GsbJEywoi6pnyU'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "مرحباً بكم في عجلة الاختيارات 🎡✨\n\nاكتبوا الأسماء متبوعة بكلمة 'قرعة' لنبدأ الاختيار.")

@bot.message_handler(func=lambda message: "قرعة" in message.text)
def start_spin(message):
    raw_text = message.text.replace("قرعة", "").strip()
    names = [n.strip() for n in raw_text.replace("،", ",").split(",") if n.strip()]
    
    if len(names) < 2:
        bot.reply_to(message, "يجب إدخال اسمين على الأقل لبدء الاختيار! 🎡")
        return

    msg = bot.send_message(message.chat.id, "جاري تدوير عجلة الاختيارات... 🎡🌀")
    frames = ["⏳ لحظات من الانتظار...", "🌀 العجلة تدور الآن...", "✨ ترقبوا الاسم المختار..."]
    
    for frame in frames:
        time.sleep(1.2)
        try: bot.edit_message_text(frame, message.chat.id, msg.message_id)
        except: pass

    winner = random.choice(names)
    result_text = f"🎊 تم الاختيار بنجاح 🎉\n\nالاسم المختار هو: \n✨💎 **{winner}** 💎✨"
    
    time.sleep(1)
    bot.edit_message_text(result_text, message.chat.id, msg.message_id, parse_mode="Markdown")

def start_bot():
    Thread(target=run).start()
    bot.polling(non_stop=True)

if __name__ == "__main__":
    start_bot()
