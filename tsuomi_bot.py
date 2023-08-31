import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import random
JOKES = [
    "الولد لأبنه: نسكّر التلفزيون ؟ … الإبن : لا لا .. خليه مردود",
    "مرة فيه شاب مرخي يسوق في سيارة وطلع في الأحمر .. لحق عليه الشرطي بالموتو وقال له بعصبية : ليش طلعت في الأحمر؟ رد الشاب بخوف : والله انا لماطلعت ما كانش أحمر هلبة .. يعني تقدر تقول نص نص.",
    "واحد أحول بيزوق حوشهم زوق حوش جارهم .. وجارهم حتى هوا أحول خطم عليه قال له “ربي يعاون والعقبة لينا”.",
    "واحد بطنه توجع فيه مشي لدكتور باكستاني سأله الدكتور : لاباس عليك ..ردعليه : والله يا دكتور واكل هندي(يعنى تين شوكى) .. الدكتور سيبه وهرب.",
    "واحد مشي يزور في خالته خضرا لقاها يابسة.",
    "المحبوس الأول: علاش حبسوك؟ .. المحبوس الثاني: تصور على خاطر خنبت حبل طوله ما يجيش ميترو .. لاكن في نهايته بقرة.",
    "القاضي للمتهم: خلي إجابتك كلها شفوي .. أمتى آخر مرة شفت المجني عليه ,المتهم : شفوي !!.",
    "سكران طاح من فوق عمارة قالوله لاباس شنو صار قاللهم و الله ماني عارف حتى اني كيف واصل"
]

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def repeat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_repeat = update.message.text.split('/repeat ', 1)[1]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_repeat)


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_joke = random.choice(JOKES)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=random_joke)

if __name__ == '__main__':
    bot_token = os.getenv("BOT_TOKEN")
    if bot_token is None:
        raise ValueError("Bot token not found in environment variables.")

    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    repeat_handler = CommandHandler('repeat', repeat)
    joke_handler = CommandHandler('joke', joke)

    application.add_handler(joke_handler)
    application.add_handler(start_handler)
    application.add_handler(repeat_handler)

    application.run_polling()
