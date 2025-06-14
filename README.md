# 🚀 Telegram Payment Gateway Checker Bot

This is a simple but powerful **Telegram bot** built with Python that:

✅ Checks any website for:  
- Known **payment gateways** (PayPal, Stripe, Klarna, etc.)  
- **CAPTCHA** (ReCAPTCHA, hCaptcha, Cloudflare challenges)  
- **Cloudflare protection**  
- Basic HTTP status and SSL info

✅ Reports results directly in your Telegram chat.

---

## 📌 Features

- **Easy to use:** Just send a URL in Telegram.
- **Secure:** Uses `.env` for secrets — never commit your bot token.
- **Flexible:** Add or remove gateways easily.
- **Ready for VPS or cloud hosting.**

---

## 📂 Project Structure

```
telegram-gateway-checker/
├── bot.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ How to Use

### 1️⃣ Clone the repository

```bash
git clone https://github.com/mrrifat/Payment-Gateway-Checker-Telegram-Bot.git
cd Payment-Gateway-Checker-Telegram-Bot
```

### 2️⃣ Install dependencies

It's recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure your bot token

Copy the example `.env` file:

```bash
cp .env.example .env
```

Edit it with your bot token from [@BotFather](https://t.me/BotFather):

```env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
```

### 4️⃣ Run the bot

```bash
python bot.py
```

### 5️⃣ Use it

* Open Telegram.
* Find your bot (the one you created via BotFather).
* Click **Start**.
* Send any website URL like `https://example.com`.
* Get instant results about payment gateways, CAPTCHA, Cloudflare, and more!

---

## ☁️ Deploying on a VPS

Run this bot on any Linux VPS 24/7:

```bash
# Connect to your server
ssh user@your-vps

# Pull your repo
git clone https://github.com/YOUR_USERNAME/telegram-gateway-checker.git
cd telegram-gateway-checker

# Install dependencies
pip install -r requirements.txt

# Create .env and add your bot token
nano .env

# Run the bot
python bot.py
```

👉 **Pro tip:**
Use `screen` or `tmux` to keep it running in the background:

```bash
screen -S bot
python bot.py
# To detach: Ctrl + A, then D
```

---

## 🔒 .env & Secrets

✅ Never commit your `.env` file!
✅ This project uses `python-dotenv` to load secrets securely.

---

## ✅ Tested with

* `python-telegram-bot` 20+
* Python 3.10+
* Linux VPS (Ubuntu 20.04+)

---

## ❤️ Contributing

Pull requests are welcome!
Feel free to suggest new payment gateways — just edit the `GATEWAYS` dictionary in `bot.py`.

---

## 📜 License

**MIT** — free to use, modify, and distribute.

---

## ⚠️ Disclaimer

I am not responsible for any misuse or bad works done with this project.
This bot is made for learning purposes only. Use responsibly and ethically.

---

## 🚀 Star the repo if you like it!

Happy hacking and have fun!
