import logging
import requests
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
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


async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Question Game! Type /next to get a new question.")


async def repeat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_repeat = update.message.text.split('/repeat ', 1)[1]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_repeat)


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_joke = random.choice(JOKES)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=random_joke)


async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question, options, correct_answer = get_random_question()
    if question:
        context.user_data['correct_answer'] = correct_answer
        context.user_data['question'] = question
        context.user_data['options'] = options

        answer_options = [[f"/answer {option}"] for option in options]

        random.shuffle(answer_options)

        question_text = f"Question: {question}\nOptions:\n"

        reply_markup = ReplyKeyboardMarkup(
            answer_options, one_time_keyboard=True)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=question_text,
            reply_markup=reply_markup  # Set the custom keyboard
        )
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, something went wrong. Please try again later.")


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text.split('/answer ', 1)[1]
    correct_answer = context.user_data.get('correct_answer')

    if user_answer == correct_answer:
        response_text = "Correct! Well done."
    else:
        response_text = f"Sorry, the correct answer is: {correct_answer}"

    # Clear the custom keyboard
    reply_markup = ReplyKeyboardRemove()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text,
        reply_markup=reply_markup  # Remove the custom keyboard
    )


def get_random_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        question_data = data['results'][0]
        question = question_data['question']
        options = question_data['incorrect_answers'] + \
            [question_data['correct_answer']]
        correct_answer = question_data['correct_answer']
        return question, options, correct_answer
    return None, [], None


if __name__ == '__main__':
    bot_token = os.getenv("BOT_TOKEN")
    if bot_token is None:
        raise ValueError("Bot token not found in environment variables.")

    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    repeat_handler = CommandHandler('repeat', repeat)
    joke_handler = CommandHandler('joke', joke)
    start_game_handler = CommandHandler('startgame', start_game)
    next_question_handler = CommandHandler('next', next_question)
    answer_handler = CommandHandler('answer', check_answer)
    application.add_handler(answer_handler)
    application.add_handler(next_question_handler)
    application.add_handler(start_game_handler)
    application.add_handler(joke_handler)
    application.add_handler(start_handler)
    application.add_handler(repeat_handler)

    application.run_polling()
