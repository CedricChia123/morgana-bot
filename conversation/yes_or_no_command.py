import random
from telegram import Update
from telegram.ext import ContextTypes
from utils.logs import log_info

from utils.generate_code import check_for_secret_code, generate_secret_code

async def yes_or_no_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    response = random.choice(["Yes", "No"])
    await log_info("{}: generate yes or no".format(update.effective_user.name), update.get_bot())
    await update.message.reply_text(response)