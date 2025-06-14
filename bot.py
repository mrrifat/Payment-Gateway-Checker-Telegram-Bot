import logging
import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# --- Load .env ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Payment Gateways ---
GATEWAYS = {
    "PayPal": "paypal.com",
    "Stripe": "stripe.com",
    "Authorize.Net": "authorize.net",
    "Square": "squareup.com",
    "Braintree": "braintreepayments.com",
    "2Checkout": "2checkout.com",
    "WorldPay": "worldpay.com",
    "Skrill": "skrill.com",
    "Razorpay": "razorpay.com",
    "Payoneer": "payoneer.com",
    "Coinbase Commerce": "commerce.coinbase.com",
    "Alipay": "alipay.com",
    "WePay": "wepay.com",
    "Amazon Pay": "pay.amazon.com",
    "Google Pay": "pay.google.com",
    "Apple Pay": "apple.com/apple-pay",
    "Klarna": "klarna.com",
    "Afterpay": "afterpay.com",
    "PayU": "payu.com",
    "BlueSnap": "bluesnap.com",
    "Mollie": "mollie.com",
    "Adyen": "adyen.com",
    "Revolut": "revolut.com/business",
    "Paystack": "paystack.com",
    "Flutterwave": "flutterwave.com",
    "Instamojo": "instamojo.com",
    "CCAvenue": "ccavenue.com",
    "CyberSource": "cybersource.com",
    "Paysafe": "paysafe.com",
    "Dwolla": "dwolla.com",
    "Zettle": "zettle.com",
    "Venmo": "venmo.com",
    "FastSpring": "fastspring.com",
    "Checkout.com": "checkout.com",
    "GoCardless": "gocardless.com",
    "BitPay": "bitpay.com",
    "Payone": "payone.com",
    "Sage Pay": "sagepay.co.uk",
    "Verifone": "verifone.com",
    "Wirecard": "wirecard.com",  
}

# --- Utils ---
def detect_gateway(html_content):
    return [name for name, domain in GATEWAYS.items() if domain in html_content]

def check_captcha(html_content):
    keywords = ['g-recaptcha', 'hcaptcha', 'data-sitekey', 'cf-captcha']
    return [kw for kw in keywords if kw in html_content]

def check_cloudflare(headers):
    return 'cf-ray' in headers

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me a URL & I'll check for:\n"
        "- Payment Gateways\n"
        "- CAPTCHA (ReCAPTCHA, hCaptcha)\n"
        "- Cloudflare Protection\n\n"
        "Example: https://example.com"
    )

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        url = "http://" + url

    await update.message.reply_text(f"🔍 Checking: {url}")

    try:
        response = requests.get(url, timeout=15)
        html = response.text
        headers = response.headers

        gateways = detect_gateway(html)
        captchas = check_captcha(html)
        cloudflare = check_cloudflare(headers)
        status_code = response.status_code
        ssl = url.startswith("https://")

        report = f"""
🔗 **URL:** `{url}`
📡 **Status Code:** {status_code}
🔒 **SSL:** {'Yes' if ssl else 'No'}

💳 **Payment Gateways:** {', '.join(gateways) if gateways else 'None found'}
🤖 **CAPTCHA Detected:** {', '.join(captchas) if captchas else 'None'}
🛡️ **Cloudflare:** {'Yes' if cloudflare else 'No'}
        """

        await update.message.reply_markdown(report)

    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")

# --- Main ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
