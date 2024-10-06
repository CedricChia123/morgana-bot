import json
import random

class StickerManager:
    def __init__(self, duck_sticker_file, komaru_sticker_file):
        with open(duck_sticker_file, 'r') as file:
            data = json.load(file)
            self.duck_stickers = data['stickers']
        with open(komaru_sticker_file, 'r') as file:
            data = json.load(file)
            self.komaru_stickers = data['stickers']

    def get_random_duck_sticker(self):
        random_sticker = random.choice(self.duck_stickers)
        return random_sticker
    
    def get_random_komaru_sticker(self):
        random_sticker = random.choice(self.komaru_stickers)
        return random_sticker