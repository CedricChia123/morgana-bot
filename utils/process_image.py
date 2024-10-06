from io import BytesIO
import requests
from PIL import Image

def process_image(image_url: str):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    scale = 512 / max(image.size)
    image = image.resize((int(image.width * scale), int(image.height * scale)))
    image = image.convert("RGBA")
    out = BytesIO()
    image.save(out, format="WEBP")
    out.seek(0)

    return out