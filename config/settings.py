import os
from pathlib import Path
from dotenv import load_dotenv

# Load from .env file if available
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# LLM Providers & Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Default Model Selection
# Recommended: gemini-2.0-flash or gemini-1.5-flash for speed & high context
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "gemini")  # 'gemini' or 'openai'
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Meta Marketing API Credentials
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")
META_APP_ID = os.getenv("META_APP_ID", "")
META_APP_SECRET = os.getenv("META_APP_SECRET", "")

# Alerting (Telegram / WhatsApp)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
WHATSAPP_WEBHOOK_URL = os.getenv("WHATSAPP_WEBHOOK_URL", "")

# Senior Media Buyer Guardrails & Automation Thresholds
TARGET_CPA = float(os.getenv("TARGET_CPA", "250.0"))        # In INR (Default target ₹250 per lead)
MAX_CPC = float(os.getenv("MAX_CPC", "15.0"))               # In INR (Default ₹15 max CPC)
BLEEDER_SPEND_MULTIPLIER = float(os.getenv("BLEEDER_SPEND_MULTIPLIER", "2.5"))  # Stop if spent > 2.5x CPA & 0 leads
FATIGUE_FREQUENCY = float(os.getenv("FATIGUE_FREQUENCY", "3.2"))                # Flag if frequency > 3.2
WINNER_ROAS = float(os.getenv("WINNER_ROAS", "3.0"))                           # Scale if ROAS > 3.0
MAX_DAILY_BUDGET_CAP = float(os.getenv("MAX_DAILY_BUDGET_CAP", "5000.0"))       # Safety Hard limit ₹5000/day
