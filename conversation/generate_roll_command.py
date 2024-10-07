import random
from telegram import Update
from telegram.ext import ContextTypes
from utils.logs import log_info

from utils.generate_code import check_for_secret_code, generate_secret_code

async def generate_roll_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    response = random.choice([1,2,3,4,5,6])
    await log_info("{}: roll".format(update.effective_user.name), update.get_bot())
    if response == 1:
        await update.message.reply_text(f'Womp womp! You got a 1.')
    elif response == 6:
        await update.message.reply_text(f'Great, a 6!')
    else:
        await update.message.reply_text(response)