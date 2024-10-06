import requests
from telegram import Update
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TimedOut

async def generate_joke_text(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    response = requests.get(url)
    if response.status_code == 200:
        text = response.json()
        try:
            await update.message.reply_text(f'{text["setup"]}\n{text["punchline"]}')
        except TimedOut:
            await update.message.reply_text("The request timed out. Please try again.")
    else:
        await update.message.reply_text(f'Could not fetch at this time. Please try again later.')