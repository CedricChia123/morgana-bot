import random
from telegram import Update
from telegram.ext import ContextTypes

from utils.generate_code import check_for_secret_code

async def yes_or_no_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    response = random.choice(["Yes", "No"])
    await update.message.reply_text(response)