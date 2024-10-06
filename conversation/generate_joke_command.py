from telegram import Update
from telegram.ext import ContextTypes
from utils.generate_code import check_for_secret_code
from utils.generate_joke_text import generate_joke_text
from utils.logs import log_info

async def generate_joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    await log_info("{}: generate joke".format(update.effective_user.name), update.get_bot())
    await generate_joke_text(update, context, 'https://official-joke-api.appspot.com/random_joke')
