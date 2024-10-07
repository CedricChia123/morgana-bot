from telegram import Update
from telegram.ext import ContextTypes
from utils.logs import log_info
import os

async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = update.get_bot()
    user = update.effective_user

    if context.args:
        user_code = " ".join(context.args)
        if user_code == os.getenv("SECRET_CODE"):
            await log_info(f"{user.name} entered the correct code: {user_code}", bot)
            await update.message.reply_text(f"Congratz! You entered the correct code.")
        else:
            await update.message.reply_text("Womp womp, the code you entered is incorrect.")
    else:
        await update.message.reply_text("Please enter a code after the /code command, e.g., `/code 1234ABC`.")