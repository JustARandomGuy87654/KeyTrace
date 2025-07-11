# SilentKey v2.0 — Educational Keylogger (C# Rewrite)

![Warning](https://img.shields.io/badge/Warning-Educational%20Use%20Only-red)

---

## ⚠️ Disclaimer

**SilentKey** is an **educational keylogger** rewritten in C# for native Windows execution.  
It is created **only for learning and research purposes** in cybersecurity.  
It captures keystrokes and periodic screenshots, sending them securely to a Telegram bot.

**Important:**
- Use this tool **only** on machines you own or have explicit permission to test.
- Unauthorized use is illegal and unethical.
- This project is designed to help you learn about:
  - Keylogging techniques.
  - Encrypted & secure data transmission.
  - Stealth and persistence.

---

## ✨ Features

✅ Native C# implementation — no Python required.  
✅ Records keystrokes in a clean, readable format.  
✅ Takes periodic screenshots (interval adjustable remotely).  
✅ Sends data securely to a Telegram bot (encrypted).  
✅ Fully silent — no visible console or window.  
✅ Sends initial status message with external IP.  
✅ Remote control: adjust screenshot interval at runtime via bot commands.

---

## 🛠️ Setup & Usage

### 1️⃣ Create your Telegram Bot
- Talk to [@BotFather](https://t.me/BotFather) and create a new bot.
- Save the Bot Token.

### 2️⃣ Get your Telegram Chat ID
- Use @userinfobot or other methods to find your chat ID.

### 3️⃣ Configure the Code
- Open `Program.cs` and fill in:
  ```csharp
  private static string telegramToken = "YOUR_TELEGRAM_BOT_TOKEN";
  private static string chatId = "YOUR_CHAT_ID";
