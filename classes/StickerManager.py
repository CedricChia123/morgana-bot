import json
import random

class StickerManager:
    def __init__(self, sticker_file):
        with open(sticker_file, 'r') as file:
            data = json.load(file)
            self.stickers = data['stickers']

    def get_random_sticker(self):
        random_sticker = random.choice(self.stickers)
        return random_sticker