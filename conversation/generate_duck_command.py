from telegram import Update
from telegram.ext import ContextTypes
from utils.generate_code import check_for_secret_code
from classes.StickerManager import StickerManager
from utils.logs import log_info

async def generate_duck_command(stickerManager: StickerManager, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_for_secret_code(update):
        return
    random_sticker = stickerManager.get_random_sticker()
    try:
        await log_info("{}: generate duck".format(update.effective_user.name), update.get_bot())
        await update.message.reply_sticker(sticker=random_sticker)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")