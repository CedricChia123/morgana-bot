import requests
from telegram import Update
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TimedOut

async def generate_insult(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    response = requests.get(url)
    if response:
        text = response.text
        try:
            await update.message.reply_text(text)
        except TimedOut:
            await update.message.reply_text("The request timed out. Please try again.")
    else:
        await update.message.reply_text(f'Could not fetch at this time. Please try again later.')