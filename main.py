import html
import json
import os
import traceback
import logging

from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from telegram.constants import ParseMode

from conversation.generate_food_command import generate_food_command
from conversation.generate_insult_command import generate_insult_command
from conversation.wish_command import wish_command
from conversation.generate_komaru_command import generate_komaru_command
from conversation.generate_cat_command import generate_cat_command
from conversation.generate_dog_command import generate_dog_command
from conversation.generate_duck_command import generate_duck_command
from conversation.generate_joke_command import generate_joke_command
from conversation.generate_quote_command import generate_quote_command
from conversation.help_command import help_command
from conversation.yes_or_no_command import yes_or_no_command
from conversation.generate_roll_command import generate_roll_command
from classes.StickerManager import StickerManager
from utils.logs import log_info

async def initialize_subscribers_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != int(MY_USER_ID):
        await update.message.reply_text("You are not authorized for this command.")
        return
    bot = context.bot
    initial_subscribers = '[]'
    subscriber_message = await bot.send_message(chat_id=SUBSCRIBER_CHAT_ID, text=initial_subscribers)
    await log_info(f"message id is {str(subscriber_message.message_id)}", update.get_bot())

async def load_subscribers(context: ContextTypes.DEFAULT_TYPE):
    """Load subscribers from a message in the chat."""
    bot = context.bot
    try:
        message_id = int(os.getenv("SUBSCRIBER_MESSAGE_ID"))
        subscriber_message = await bot.forward_message(chat_id=SUBSCRIBER_CHAT_ID, from_chat_id=SUBSCRIBER_CHAT_ID, message_id=message_id)
        subscribers = set(json.loads(subscriber_message.text))
        return subscribers
    except Exception as e:
        logging.error(f"Failed to load subscribers: {e}")
        return set()

async def save_subscribers(subscribers, context: ContextTypes.DEFAULT_TYPE):
    """Save the list of subscribers to the message."""
    bot = context.bot
    try:
        subscribers_data = json.dumps(list(subscribers))
        message_id = int(os.getenv("SUBSCRIBER_MESSAGE_ID"))
        await bot.edit_message_text(chat_id=SUBSCRIBER_CHAT_ID, message_id=message_id, text=subscribers_data)
    except Exception as e:
        logging.error(f"Failed to save subscribers: {e}")

async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    subscribers = await load_subscribers(context)
    user_id = update.effective_user.id
    user_name = update.effective_user.name

    if user_id not in subscribers:
        subscribers.add(user_id)
        await save_subscribers(subscribers, context)
        await log_info(f"{user_name} ID: {user_id} subscribed", update.get_bot())
        await update.message.reply_text(f"Thank you, {user_name}! You are now subscribed for updates.")
    else:
        await update.message.reply_text(f"{user_name}, you are already subscribed!")

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    subscribers = await load_subscribers(context)
    user_id = update.effective_user.id
    user_name = update.effective_user.name

    if user_id in subscribers:
        subscribers.remove(user_id)
        await save_subscribers(subscribers, context)
        await log_info(f"{user_name} ID: {user_id} unsubscribed", update.get_bot())
        await update.message.reply_text(f"Aww, you have been unsubscribed from updates, {user_name}.")
    else:
        await update.message.reply_text(f"{user_name}, you are not subscribed!")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "Sticker-inator encountered an unhandled exception\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
    )
    stack = (
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    bot = update.get_bot()
    logging.error(tb_string)
    await bot.send_message(os.environ.get("LOG_ID"), message, parse_mode=ParseMode.HTML)
    await bot.send_message(os.environ.get("LOG_ID"), stack, parse_mode=ParseMode.HTML)
    await bot.send_message(update.effective_chat.id, "Morgana encountered an error, please try again or cancel the current operation with the cancel command")
    
async def send_update_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != int(MY_USER_ID):
        await update.message.reply_text("You are not authorized to send updates.")
        return

    bot = update.get_bot()
    if not context.args:
        await update.message.reply_text("Please provide the update message after the command, e.g., `/send_update Your message here`.")
        return

    update_message = " ".join(context.args)
    subscribers = await load_subscribers(context)
    await log_info("Sending updates to all subscribed users.", bot)

    for subscriber_id in subscribers:
        try:
            await bot.send_message(chat_id=subscriber_id, text=update_message)
        except Exception as e:
            await log_info(f"Failed to send message to {subscriber_id}: {e}", bot)

    await update.message.reply_text("Update has been sent to all subscribers.")

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN_MORGANA')
MY_USER_ID = os.getenv('MY_USER_ID')
SUBSCRIBER_CHAT_ID = os.environ.get("LOG_ID")
SUBSCRIBER_MESSAGE_ID = None

app = ApplicationBuilder().token(BOT_TOKEN).build()
stickerManager = StickerManager(os.path.join(os.path.dirname(__file__), 'assets/duckStickers.json'), os.path.join(os.path.dirname(__file__), 'assets/komaruStickers.json'))

app.add_handler(CommandHandler("cat", generate_cat_command))
app.add_handler(CommandHandler("dog", generate_dog_command))
app.add_handler(CommandHandler("duck", lambda update, context: generate_duck_command(stickerManager, update, context)))
app.add_handler(CommandHandler("komaru", lambda update, context: generate_komaru_command(stickerManager, update, context)))
app.add_handler(CommandHandler("flip", yes_or_no_command))
app.add_handler(CommandHandler("joke", generate_joke_command))
app.add_handler(CommandHandler("quote", generate_quote_command))
app.add_handler(CommandHandler("wish", wish_command))
app.add_handler(CommandHandler("insult", generate_insult_command))
app.add_handler(CommandHandler("subscribe", subscribe_command))
app.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
app.add_handler(CommandHandler("food", generate_food_command))
app.add_handler(CommandHandler("roll", generate_roll_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("start", help_command))
app.add_handler(CommandHandler("send_update", send_update_command))
app.add_handler(CommandHandler("initialize_subscribers", initialize_subscribers_message))
app.add_error_handler(error_handler)

app.run_polling()
