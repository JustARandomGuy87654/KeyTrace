import requests
import base64
from config import TOKEN, CHAT_ID

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=data)
    except:
        pass

def send_photo_base64(base64_img, caption=""):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    data = {
        "chat_id": CHAT_ID,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    files = {
        "photo": base64.b64decode(base64_img)
    }
    try:
        requests.post(url, data=data, files=files)
    except:
        pass