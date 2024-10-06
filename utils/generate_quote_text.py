import requests
from telegram import Update
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TimedOut

async def generate_quote_text(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            text = response.json()

            if text[0]["q"] == "Too many requests. Obtain an auth key for unlimited access.":
                await update.message.reply_text('Too many requests. Please try again after some time.')
                return
            
            try:
                await update.message.reply_text(f'{text[0]["q"]}\n- {text[0]["a"]}')
            except TimedOut:
                await update.message.reply_text("The request timed out. Please try again.")
        else:
            await update.message.reply_text('Could not fetch at this time. Please try again later.')

    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f'Network error: {e}. Please try again later.')