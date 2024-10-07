import random
from telegram import Update
import os

def generate_secret_code():
    return f'Congratz! The code is {os.getenv("SECRET_CODE")}'

async def check_for_secret_code(update: Update):
    if random.random() < 0.001:
        return True
    return False