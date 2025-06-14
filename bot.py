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

# Load env vars
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ✅ Full robust gateways list
GATEWAYS = [
    "PayPal", "Stripe", "Square", "Braintree", "Authorize.Net", "Worldpay",
    "Adyen", "Klarna", "Afterpay", "Affirm", "Sezzle", "Zip", "Splitit",
    "Checkout.com", "Mollie", "Skrill", "Paysafe", "PayU", "Payoneer",
    "Alipay", "WeChat Pay", "Razorpay", "Paytm", "CC Avenue", "Ingenico",
    "CyberSource", "BlueSnap", "FastSpring", "2Checkout", "PaySimple",
    "GoCardless", "Apple Pay", "Google Pay", "Amazon Pay", "Samsung Pay",
    "Flutterwave", "iDEAL", "Bancontact", "Giropay", "Sofort", "GCash",
    "TrueMoney", "M-Pesa"
]

CAPTCHAS = ["recaptcha", "hcaptcha", "cloudflare challenge"]

PLATFORMS = ["Shopify", "WooCommerce", "Magento", "BigCommerce", "Angular", "React", "Vue", "Next.js", "Laravel", "WordPress"]

def get_ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return ip, res.get("country", "Unknown"), res.get("isp", "Unknown")
    except:
        return "N/A", "N/A", "N/A"

def has_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(3)
            s.connect((domain, 443))
        return True
    except:
        return False

async def check_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip().split()
    if len(msg) < 2:
        await update.message.reply_text("Use: `/url https://example.com`", parse_mode="Markdown")
        return

    url = msg[1].strip()
    if url.startswith("http://"):
        url = url.replace("http://", "https://", 1)

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    scraper = cloudscraper.create_scraper()
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = scraper.get(url, headers=headers, timeout=10)
        status_code = res.status_code
        html = res.text.lower()
    except Exception as e:
        await update.message.reply_text(f"Error fetching URL: {e}")
        return

    ssl_status = "Yes ✅" if has_ssl(domain) else "No ❌"
    found_gateways = sorted({g for g in GATEWAYS if g.lower() in html})
    captcha = "Detected ❌" if any(c in html for c in CAPTCHAS) else "No ✅"
    cf = "Yes ❌" if "cloudflare" in html else "No ✅"
    graphql = "Yes" if "graphql" in html else "No"
    platforms = sorted({p for p in PLATFORMS if p.lower() in html}) or ["Unknown"]
    ip, country, isp = get_ip_info(domain)

    reply = f"""
🌐 *Site Info*

🔗 [{url}]({url})
📶 Status: `{status_code}`
🔒 SSL: `{ssl_status}`
💳 Gateways: `{', '.join(found_gateways) or 'None'}`
🛡️ CAPTCHA: {captcha}
☁️ Cloudflare: {cf}
📂 GraphQL: `{graphql}`
🛠️ Platforms: `{', '.join(platforms)}`
🌍 Country: `{country}`
🌐 IP: `{ip}`
📡 ISP: `{isp}`
"""
    await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=True)

async def check_stripe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip().split()
    if len(msg) < 2:
        await update.message.reply_text("Use: `/stripe <Stripe link or merchant site>`", parse_mode="Markdown")
        return

    input_url = msg[1].strip()
    if input_url.startswith("http://"):
        input_url = input_url.replace("http://", "https://", 1)

    parsed = urlparse(input_url)
    domain = parsed.netloc.lower()

    # If direct stripe.com link:
    if "stripe.com" in domain:
        if "checkout" in domain or "/checkout" in input_url:
            kind = "Stripe Checkout"
            security = "Likely 3D Secure"
        elif "billing" in domain or "/billing" in input_url:
            kind = "Stripe Billing Portal"
            security = "Usually 2D Secure"
        elif "invoice" in domain or "/invoice" in input_url:
            kind = "Stripe Hosted Invoice"
            security = "Usually 2D Secure"
        else:
            kind = "Unknown Stripe Link"
            security = "Could not determine"
        reply = f"""
🔍 *Stripe Link Inspector*

🔗 `{kind}`
🔐 *Security*: `{security}`

⚠️ *Note:* Exact authentication depends on merchant config and card rules.
"""
    else:
        # Merchant site: same as /url but show only Stripe info
        scraper = cloudscraper.create_scraper()
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            res = scraper.get(input_url, headers=headers, timeout=10)
            html = res.text.lower()
        except Exception as e:
            await update.message.reply_text(f"Error fetching site: {e}")
            return

        stripe_found = "Yes ✅" if "stripe" in html else "No ❌"
        is_3d = "Yes" if any(k in html for k in ["3dsecure", "sca", "strong customer authentication"]) else "Unknown"
        reply = f"""
🔍 *Stripe Merchant Scan*

🔗 URL: [{input_url}]({input_url})
💳 *Uses Stripe:* `{stripe_found}`
🔐 *3D Secure Clues:* `{is_3d}`

⚠️ *Note:* Only inferred from visible site code.
"""
    await update.message.reply_text(reply, parse_mode="Markdown", disable_web_page_preview=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Use `/url <site>` to scan any site or `/stripe <stripe link or merchant site>` to inspect Stripe only.",
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("url", check_url))
    app.add_handler(CommandHandler("stripe", check_stripe))
    app.run_polling()
