import html
import json
import os
import sqlite3
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
from classes.StickerManager import StickerManager
from utils.logs import log_info

def init_db():
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            user_id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()
    await log_info(f"{user_name} ID: {user_id} subscribed", update.get_bot())
    await update.message.reply_text(f"Thank you, {user_name}! You are now subscribed for updates.")

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_name = update.effective_user.name

    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subscribers WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    await log_info(f"{user_name} ID: {user_id} unsubscribed", update.get_bot())

    await update.message.reply_text(f"Aww, you have been unsubscribed from updates, {user_name}.")

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
    await log_info("Sending updates to all subscribed users.", bot)
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM subscribers")
    subscribed_users = cursor.fetchall()
    conn.close()

    for user_id_tuple in subscribed_users:
        subscriber_id = user_id_tuple[0]
        try:
            await bot.send_message(chat_id=subscriber_id, text=update_message)
        except Exception as e:
            await log_info(f"Failed to send message to {subscriber_id}: {e}", bot)
    await update.message.reply_text("Update has been sent to all subscribers.")

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
    
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN_MORGANA')
MY_USER_ID = os.getenv('MY_USER_ID')

app = ApplicationBuilder().token(BOT_TOKEN).build()
stickerManager = StickerManager(os.path.join(os.path.dirname(__file__), 'assets/duckStickers.json'), os.path.join(os.path.dirname(__file__), 'assets/komaruStickers.json'))

init_db()
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
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("start", help_command))
app.add_handler(CommandHandler("send_update", send_update_command))
app.add_error_handler(error_handler)

app.run_polling()
