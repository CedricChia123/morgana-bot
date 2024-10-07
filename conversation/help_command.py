from telegram import Update
from telegram.ext import ContextTypes
from utils.logs import log_info

from utils.generate_code import check_for_secret_code

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_for_secret_code(update):
        return
    await log_info("{}: help".format(update.effective_user.name), update.get_bot())
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}!\n'
        "This bot is a stress reliever. Consider using /wish command to suggest a new feature!\n\n"
        "Available commands:\n"
        "/wish <YOUR WISH> - Suggest a new feature\n"
        "/cat - Generates a random cat\n"
        "/dog - Generates a random dog\n"
        "/duck - Generates a duck sticker\n"
        "/flip - Generates yes or no\n"
        "/joke - Generates a random joke\n"
        "/komaru - Generates a random komaru cat\n"
        "/quote - Generates a motivational quote\n"
        "/insult - Generates a random insult\n"
        "/food - Generates a random cuisine\n"
        "/roll - Rolls a dice\n"
        "/subscribe - Subscribe for bot updates\n"
        "/unsubscribe - Unsubscribe from bot updates\n"
        "/code - Submit a code"
    )