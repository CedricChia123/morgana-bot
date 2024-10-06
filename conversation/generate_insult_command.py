from telegram import Update
from telegram.ext import ContextTypes
from utils.generate_code import check_for_secret_code, generate_secret_code
from utils.generate_insult import generate_insult
from utils.logs import log_info

async def generate_insult_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        await update.message.reply_text(generate_secret_code())
    await log_info("{}: generate insult".format(update.effective_user.name), update.get_bot())
    await generate_insult(update, context, 'https://insult.mattbas.org/api/insult')
