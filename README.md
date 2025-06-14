# 🚀 Payment Gateway & Stripe Checker Bot

A powerful **Telegram bot** built with Python that:

✅ Checks any website for:
- **Payment gateways** (big + regional: PayPal, Stripe, Klarna, Razorpay, etc.)
- **CAPTCHA** (ReCAPTCHA, hCaptcha)
- **Cloudflare protection**
- Basic **HTTP status, SSL info, IP & ISP**

✅ Inspects **Stripe links & merchant sites** to detect:
- Link type (`Checkout`, `Billing Portal`, `Invoice`)
- Likely **3D Secure** vs **2D Secure**
- Smart Stripe usage detection on merchant sites

📥 **Get results instantly in your Telegram chat!**

---

## 📌 **Commands**

### `/url <website>`
Full scan for any website.
- Example:
```
/url https://example.com
```

### `/stripe <link or site>`
Smart Stripe-specific check:
- If you pass a **Stripe link** → Detects type & security level.
- If you pass a **merchant site** → Checks for Stripe usage & 3D Secure clues.
- Examples:
```
/stripe https://checkout.stripe.com/...
/stripe https://billing.stripe.com/...
/stripe https://merchantwebsite.com
```

---

## 📂 **Project Structure**

```
Payment-Gateway-Checker-Telegram-Bot/
├── bot.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ **How to Use**

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Payment-Gateway-Checker-Telegram-Bot.git
cd Payment-Gateway-Checker-Telegram-Bot
```

### 2️⃣ Install dependencies (recommended: use a virtual env)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Configure your bot token

Copy the example .env and edit:

```bash
cp .env.example .env
```

Edit `.env`:

```env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

### 4️⃣ Run the bot

```bash
python bot.py
```

✅ In Telegram:
- `/start` to confirm it works
- `/url https://example.com`
- `/stripe https://checkout.stripe.com/...`

---

## ☁️ Deploying on a VPS

Recommended: run on a Linux server for 24/7 uptime.

1. Connect to your server:
```bash
ssh user@your-vps
```

2. Clone the repo & install requirements as above.

3. Use a systemd service to auto-start at boot (optional but recommended).

---

## 🔒 .env & Secrets

✅ Never commit your `.env`!  
✅ Uses `python-dotenv` to load secrets securely.

---

## ✅ Tested with

- `python-telegram-bot` v20+
- Python 3.10+
- Linux VPS (Ubuntu 20.04+)

---

## ❤️ Contributing

Pull requests are welcome!  
Feel free to suggest more payment gateways or features — just open an issue or PR.

---

## 📜 License

**MIT** — free to use, modify, and distribute.

---

## ⚠️ Disclaimer

This bot provides best-effort checks based on visible website code & known patterns.  
It cannot guarantee real merchant settings for 3D/2D Secure.  
Use responsibly & ethically!

---

## 🚀 Star the repo if you like it — and enjoy!
