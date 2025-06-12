# SilentKey - Educational Keylogger for Cybersecurity Learning

![Warning](https://img.shields.io/badge/Warning-Educational%20Use%20Only-red)

---

## ⚠️ Disclaimer

**SilentKey** is a simple keylogger created solely for educational and research purposes in cybersecurity. It captures keystrokes and periodic screenshots, sending them securely to a Telegram bot.

**Important:**

- Use this tool **only** on machines you own or have explicit permission to test.
- Unauthorized use is illegal and unethical.
- This project is designed to help you learn about keylogging techniques, encryption, and secure data transmission.

---

## Features

- Records keystrokes in a readable format.
- Takes screenshots every 30 seconds.
- Sends data to a Telegram bot via encrypted messages.
- Runs silently in the background.
- Sends an initial status message with the victim’s IP when started.
- Simple base64 encoding for easy readability (you must decode the keylogs)

---

## Setup & Usage

1. Create a Telegram bot and get the Bot Token.
2. Find your Telegram chat ID (where you want to receive logs).
3. Configure the `token`, `chat_id`, and `encryption_key` variables in the script.
4. Run the script on the target machine **with permission**.

---
