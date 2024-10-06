from telegram import Update
from telegram.ext import ContextTypes
from utils.generate_code import check_for_secret_code
from utils.generate_animal import generate_animal
from utils.logs import log_info

async def generate_dog_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    await log_info("{}: generate dog".format(update.effective_user.name), update.get_bot())
    await generate_animal(update, context, 'https://dog.ceo/api/breeds/image/random')