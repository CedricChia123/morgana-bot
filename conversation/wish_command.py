from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.logs import log_info

async def wish_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = update.get_bot()
    user = update.effective_user

    if context.args:
        wish_text = " ".join(context.args)
        await log_info(f"{update.effective_user.name}: wish - {wish_text}", update.get_bot())
        await update.message.reply_text(f"Thank you for your feedback! You wished for: {wish_text}")
    else:
        await update.message.reply_text("Please provide your feature wish after the /wish command, e.g., `/wish I want more cats`.")