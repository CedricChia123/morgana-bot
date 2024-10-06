import html
import json
import os
import traceback
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv
from telegram.constants import ParseMode

from conversation.generate_cat_command import generate_cat_command
from conversation.generate_dog_command import generate_dog_command
from conversation.generate_duck_command import generate_duck_command
from conversation.generate_joke_command import generate_joke_command
from conversation.help_command import help_command
from conversation.yes_or_no_command import yes_or_no_command
from classes.StickerManager import StickerManager

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

app = ApplicationBuilder().token(BOT_TOKEN).build()
stickerManager = StickerManager(os.path.join(os.path.dirname(__file__), 'assets/duckStickers.json'))

app.add_handler(CommandHandler("cat", generate_cat_command))
app.add_handler(CommandHandler("dog", generate_dog_command))
app.add_handler(CommandHandler("duck", lambda update, context: generate_duck_command(stickerManager, update, context)))
app.add_handler(CommandHandler("flip", yes_or_no_command))
app.add_handler(CommandHandler("joke", generate_joke_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("start", help_command))
app.add_error_handler(error_handler)

app.run_polling()
