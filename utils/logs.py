import logging
import os
from telegram import Update
from telegram.constants import ParseMode


async def send_message(update: Update, message):
    # sends message with markdown parse mode
    bot = update.get_bot()
    await bot.send_message(
        update.effective_chat.id, message, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True
    )


async def log_info(info, bot):
    logging.info(info)
    try:
        await bot.send_message(os.environ.get("LOG_ID"), "*\[Morgana\]* " + info, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        logging.error(e)