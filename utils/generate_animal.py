import requests
from telegram import InputFile, Update
from telegram.ext import ContextTypes
from telegram.error import TimedOut
from utils.process_image import process_image

async def generate_animal(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    response = requests.get(url)
    if response.status_code == 200:
        image_url = response.json()[0]['url'] if 'cat' in url else response.json()['message']
        try:
            processed_image = process_image(image_url)
            sticker_file = InputFile(processed_image, filename="sticker.webp")
            await update.message.reply_sticker(sticker=sticker_file, read_timeout=60)
        except TimedOut:
            await update.message.reply_text("The request timed out. Please try again.")
    else:
        await update.message.reply_text(f'Could not fetch an image at this time. Please try again later.')