from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}!\n'
        "This bot is a stress reliever.\n\n"
        "Available commands:\n"
        "/cat - Generates a random cat\n"
        "/dog - Generates a random dog\n"
        "/duck - Generates a duck sticker\n"
        "/flip - Generates yes or no\n"
        "/joke - Generates a random joke\n"
    )