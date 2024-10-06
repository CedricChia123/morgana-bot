import json
import os
import random
import requests
from telegram import InputFile, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from telegram.error import TimedOut

class StickerManager:
    def __init__(self, sticker_file):
        self.link = None
        with open(sticker_file, 'r') as file:
            data = json.load(file)
            self.stickers = data['stickers']

    def set_link(self, link):
        self.link = link

    def get_random_sticker(self):
        random_sticker = random.choice(self.stickers)
        return random_sticker
    
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN_MORGANA')

app = ApplicationBuilder().token(BOT_TOKEN).build()
stickerManager = StickerManager(os.path.join(os.path.dirname(__file__), 'stickers.json'))
    
def generate_secret_code():
    return "🔑 Congratz, you found the hidden message! Thank you for using this bot! 🔑"

async def check_for_secret_code(update: Update):
    if random.random() < 0.01:  # 1% chance
        await update.message.reply_text(generate_secret_code())
        return True
    return False

def process_image(image_url: str):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    scale = 512 / max(image.size)
    image = image.resize((int(image.width * scale), int(image.height * scale)))
    image = image.convert("RGBA")
    out = BytesIO()
    image.save(out, format="WEBP")
    out.seek(0)

    return out

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

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def generate_cat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    await generate_animal(update, context, 'https://api.thecatapi.com/v1/images/search')

async def generate_dog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    await generate_animal(update, context, 'https://dog.ceo/api/breeds/image/random')

async def generate_duck(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    random_sticker = stickerManager.get_random_sticker()
    try:
        await update.message.reply_sticker(sticker=random_sticker)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def generate_yes_or_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    response = random.choice(["Yes", "No"])
    await update.message.reply_text(response)

async def generate_joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    await generate_joke_text(update, context, 'https://official-joke-api.appspot.com/random_joke')

async def get_sticker_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    if sticker:
        file_id = sticker.file_id
        await update.message.reply_text(f"Sticker File ID: {file_id}")
    else:
        await update.message.reply_text("Please send a sticker!")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}!\n'
        "This bot generates random animals.\n\n"
        "Available commands:\n"
        "/cat - Generates a random cat\n"
        "/dog - Generates a random dog\n"
        "/duck - Generates a duck sticker\n"
        "/flip - Generates yes or no\n"
        "/joke - Generates a random joke\n"
    )

app.add_handler(CommandHandler("cat", generate_cat))
app.add_handler(CommandHandler("dog", generate_dog))
app.add_handler(CommandHandler("duck", generate_duck))
app.add_handler(CommandHandler("flip", generate_yes_or_no))
app.add_handler(CommandHandler("joke", generate_joke))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("start", help))

app.run_polling()
