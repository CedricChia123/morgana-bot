import random
from telegram import Update

def generate_secret_code():
    return "Thank you for using this bot! Please use /wish command to suggest new features~"

async def check_for_secret_code(update: Update):
    if random.random() < 0.05:  # 5% chance
        return True
    return False