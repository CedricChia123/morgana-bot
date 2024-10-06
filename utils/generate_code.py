import random
from telegram import Update

def generate_secret_code():
    return "🔑 Congratz, you found the hidden message! Thank you for using this bot! 🔑"

async def check_for_secret_code(update: Update):
    if random.random() < 0.01:  # 1% chance
        await update.message.reply_text(generate_secret_code())
        return True
    return False