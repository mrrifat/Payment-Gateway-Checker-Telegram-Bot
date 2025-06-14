import os
import re
import cloudscraper
import socket
import ssl
import requests
from urllib.parse import urlparse

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 🌐 Expanded payment gateways list
GATEWAYS = [
    "PayPal", "Stripe", "Square", "Braintree", "Authorize.Net", "Worldpay",
    "Adyen", "Klarna", "Afterpay", "Affirm", "Sezzle", "Zip", "Checkout.com",
    "Mollie", "Skrill", "Paysafe", "PayU", "Payoneer", "Alipay", "WeChat Pay",
    "Razorpay", "Paytm", "CC Avenue", "Ingenico", "CyberSource", "BlueSnap",
    "FastSpring", "2Checkout", "PaySimple", "GoCardless", "Apple Pay",
    "Google Pay", "Amazon Pay", "Samsung Pay"
]

# CAPTCHA indicators
CAPTCHAS = ["recaptcha", "hcaptcha", "cloudflare challenge"]

# Popular platforms (optional tech detection)
PLATFORMS = ["Shopify", "Angular", "React", "Vue", "Next.js", "Lit", "Gin", "Laravel", "WordPress"]

# IP info helper
def get_ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = response.get("country", "Unknown")
        isp = response.get("isp", "Unknown")
        return ip, country, isp
    except:
        return "N/A", "N/A", "N/A"

# SSL check helper
def has_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(3)
            s.connect((domain, 443))
        return True
    except:
        return False

# Main handler
async def check_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    parts = msg.split()
    if len(parts) < 2:
        await update.message.reply_text(
            "Please provide a URL like:\n`/url https://example.com`",
            parse_mode="Markdown"
        )
        return

    url = parts[1].strip()

    # Enforce HTTPS
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    scraper = cloudscraper.create_scraper()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = scraper.get(url, headers=headers, timeout=10)
        status_code = response.status_code
        html = response.text
    except Exception as e:
        await update.message.reply_text(f"Error fetching URL: {e}")
        return

    # SSL check
    ssl_enabled = "Yes ✅" if has_ssl(domain) else "No ❌"

    # Payment gateways — with special Stripe Checkout detection
    found_gateways = []
    html_lower = html.lower()

    if "checkout.stripe.com" in domain:
        found_gateways.append("Stripe Checkout (Likely 3D Secure)")
    else:
        for gateway in GATEWAYS:
            if gateway.lower() in html_lower:
                if gateway.lower() == "stripe":
                    if ("3dsecure" in html_lower or 
                        "strong customer authentication" in html_lower or
                        "sca" in html_lower):
                        found_gateways.append("Stripe (3D Secure)")
                    else:
                        found_gateways.append("Stripe (2D Secure)")
                else:
                    found_gateways.append(gateway)

    gateway_result = ", ".join(sorted(set(found_gateways))) if found_gateways else "None found"

    # CAPTCHA
    found_captcha = any(c in html_lower for c in CAPTCHAS)
    captcha_result = "Detected ❌" if found_captcha else "No Captcha Detected ✅"

    # Cloudflare
    uses_cf = "cloudflare" in html_lower
    cf_result = "Yes ❌" if uses_cf else "No ✅"

    # GraphQL
    graphql = "Yes" if "graphql" in html_lower else "No"

    # Platform detection
    detected_platforms = [p for p in PLATFORMS if p.lower() in html_lower]
    platform_result = ", ".join(sorted(set(detected_platforms))) if detected_platforms else "Unknown"

    # IP info
    ip, country, isp = get_ip_info(domain)

    # Reply message
    reply = f"""
🌐 *Website Information* 🌐

🔗 *URL:* [{url}]({url})
📶 *HTTP Status:* `{status_code}`
🔒 *SSL:* `{ssl_enabled}`
💳 *Payment Gateways:* `{gateway_result}`
🛡️ *CAPTCHA:* {captcha_result}
☁️ *Cloudflare:* {cf_result}
🗂️ *GraphQL:* `{graphql}`
🛠️ *Platform:* `{platform_result}`
🌍 *Country:* `{country}`
🌐 *IP:* `{ip}`
📡 *ISP:* `{isp}`

👤 Checked by: {update.effective_user.first_name}
    """

    await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=True)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send `/url https://example.com` to check a site.")

# Run bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("url", check_url))
    app.run_polling()
