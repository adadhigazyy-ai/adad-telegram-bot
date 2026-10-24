import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# إعداد السجل لرصد الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ضبط مفتاح الذكاء الاصطناعي (استبدل النص التالي بمفتاح الـ API الخاص بك)
genai.configure(api_key="AQ.Ab8RN6I4bOHf2JhfV5FGayHc25Ix83Xcmm93tqetemmVH2E3Rw")
model = genai.GenerativeModel('gemini-1.5-flash')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('أهلاً بك. أنا مساعدك العلمي للصف العاشر. اطرح سؤالك أو الفقرة التي لم تفهمها.')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # توليد الرد من نموذج الذكاء الاصطناعي
    response = model.generate_content(user_message)
    ai_reply = response.text

    # العبارات الثابتة في البداية والنهاية
    prefix = "أهلاً وسهلاً في بوت الأستاذ أداد حجازي \nللصف العاشر لشرح مادة الفيزياء والعلوم\n\n"
    suffix = "\n\n📚 مصدر المعلومات: نوطة الأستاذ أداد حجازي\n\nهل فهمت المعلومة أم أصيغها بطريقة أخرى؟\nيسعدني أنني مساعدك الذكي، لقد طورني الأستاذ أداد لمساعدتك متى وكيفما تشاء."

    # دمج الرد مع البداية والنهاية
    final_message = prefix + ai_reply + suffix

    await update.message.reply_text(final_message)


if __name__ == '__main__':
    application = ApplicationBuilder().token("8970639449:AAF_HP6FY3-ZqCA8DDUd17gX2LZ9E_m1ygQ").build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("البوت قيد التشغيل...")
    application.run_polling()