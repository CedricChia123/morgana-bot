import random
from telegram import Update
from telegram.ext import ContextTypes
from utils.generate_code import check_for_secret_code, generate_secret_code
from utils.logs import log_info

cuisines = [
    "Italian", "Chinese", "Mexican", "Japanese", "Thai", "Indian", "French", "Korean"
]

async def generate_food_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        await update.message.reply_text(generate_secret_code())
    await log_info("{}: generate food".format(update.effective_user.name), update.get_bot())
    random_cuisine = random.choice(cuisines)

    await update.message.reply_text(f"Morgana suggests some {random_cuisine} cuisine today")
