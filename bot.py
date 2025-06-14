import os
import re
import cloudscraper
import socket
import ssl
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from python_dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

import json

# Load .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Known payment gateways
GATEWAYS = ["PayPal", "Stripe", "Klarna", "Adyen", "Shopify", "Square", "Braintree", "Authorize.Net", "Worldpay"]

# Known CAPTCHA keywords
CAPTCHAS = ["recaptcha", "hcaptcha", "cloudflare challenge"]

# Known platforms for quick tech detection
PLATFORMS = ["Shopify", "Angular", "React", "Vue", "Next.js", "Lit", "Gin", "Laravel", "WordPress"]

# Helper to get IP and ISP
def get_ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = response.get("country", "Unknown")
        isp = response.get("isp", "Unknown")
        return ip, country, isp
    except:
        return "N/A", "N/A", "N/A"

# Check SSL by connecting directly
def has_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(3)
            s.connect((domain, 443))
        return True
    except:
        return False

# Main URL checker
async def check_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    parts = msg.split()
    if len(parts) < 2:
        await update.message.reply_text("Please provide a URL like:\n`/url https://example.com`", parse_mode="Markdown")
        return

    url = parts[1].strip()

    # Force HTTPS
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)

    parsed = urlparse(url)
    domain = parsed.netloc

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

    # Payment gateways
    found_gateways = []
    for gateway in GATEWAYS:
        if re.search(gateway, html, re.IGNORECASE):
            found_gateways.append(gateway)
    gateway_result = ", ".join(found_gateways) if found_gateways else "None found"

    # CAPTCHA
    found_captcha = any(c in html.lower() for c in CAPTCHAS)
    captcha_result = "Detected ❌" if found_captcha else "No Captcha Detected ✅"

    # Cloudflare
    uses_cf = "cloudflare" in html.lower()
    cf_result = "Yes ❌" if uses_cf else "No ✅"

    # GraphQL
    graphql = "Yes" if "graphql" in html.lower() else "No"

    # Platform tech
    detected_platforms = []
    for tech in PLATFORMS:
        if tech.lower() in html.lower():
            detected_platforms.append(tech)
    platform_result = ", ".join(detected_platforms) if detected_platforms else "Unknown"

    # IP, Country, ISP
    ip, country, isp = get_ip_info(domain)

    # Reply
    reply = f"""
🌐 *Website Information* 🌐

🔗 *Site URL:* [{url}]({url})
🔍 *HTTP Status:* `{status_code}`
💳 *Payment Gateway:* `{gateway_result}`
🛡️ *Captcha:* {captcha_result}
☁️ *Cloudflare:* {cf_result}
🔍 *GraphQL:* `{graphql}`
🛠️ *Platform:* `{platform_result}`
🌍 *Country:* `{country}`
🌐 *IP Address:* `{ip}`
📡 *ISP:* `{isp}`

👤 *Checked By:* {update.effective_user.first_name}
    """

    await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=True)

# Start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send `/url https://example.com` to check a site.")

# Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("url", check_url))
    app.run_polling()
