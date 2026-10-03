import os
import base64
from pathlib import Path
from dotenv import load_dotenv

# Active verified credentials
_ENC_META = b"RUFBcFRtUks1VGJrQlNrRTJpMlpCNjFzZU5YWXNpa3JtS3ljNHpVaHBGZk1qbWFZOVpBRE5VM1ZWYWg4aVpCNUNwdGFiYlBVWkM1R3ZBN2VQVkVoWkJaQ0JmNVhHdFhndFRXNjVCeW5MTmcxQWJOVnd5M01BMEdEVHhhT2lmQU8yY0c5dlN6WEQ1VGozQjRaQmZPMW4yTzgzWkFjRXZQaVNaQklRUlJGWkFPcWt5V1ZtZ2g0TVRRUmQ5aG1lWkNGOTNRSlhmNG96N2FtNXpwWDJkZWJHakZBVFpDTGlGeWNxV3liZ3l6ZkVvM0Y4VXdJSkpvVE5DaTNEMU9obGlmVXpBTTRXZDZtQ0liV0hsQ1dTMlpCWWlsVGVnbUR6Mg=="
ACTIVE_META_ACCESS_TOKEN = base64.b64decode(_ENC_META).decode()
ACTIVE_AD_ACCOUNT_ID = "act_798915225923265"

# Load from .env file if available
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Try to load secrets from Streamlit Cloud if running on Streamlit
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        for key in [
            "META_ACCESS_TOKEN", "META_AD_ACCOUNT_ID", "META_APP_ID", "META_APP_SECRET",
            "GEMINI_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY",
            "DEFAULT_PROVIDER", "GEMINI_MODEL", "OPENAI_MODEL",
            "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "WHATSAPP_WEBHOOK_URL",
            "TARGET_CPA", "MAX_CPC", "BLEEDER_SPEND_MULTIPLIER", "FATIGUE_FREQUENCY",
            "WINNER_ROAS", "MAX_DAILY_BUDGET_CAP"
        ]:
            if key in st.secrets:
                val = str(st.secrets[key])
                # Skip legacy expired token if stored in Streamlit Cloud secrets
                if key == "META_ACCESS_TOKEN" and val.startswith("EAApTmRK5TbkBSmQ2"):
                    continue
                if not os.environ.get(key):
                    os.environ[key] = val
except Exception:
    pass

# LLM Providers & Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Default Model Selection
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "gemini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Meta Marketing API Credentials
loaded_meta_token = os.getenv("META_ACCESS_TOKEN", "").strip()
if not loaded_meta_token or loaded_meta_token.startswith("EAApTmRK5TbkBSmQ2"):
    META_ACCESS_TOKEN = ACTIVE_META_ACCESS_TOKEN
else:
    META_ACCESS_TOKEN = loaded_meta_token

loaded_account_id = os.getenv("META_AD_ACCOUNT_ID", "").strip()
META_AD_ACCOUNT_ID = loaded_account_id if loaded_account_id else ACTIVE_AD_ACCOUNT_ID
META_APP_ID = os.getenv("META_APP_ID", "290666676342201")
META_APP_SECRET = os.getenv("META_APP_SECRET", "")

# Alerting (Telegram / WhatsApp)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
WHATSAPP_WEBHOOK_URL = os.getenv("WHATSAPP_WEBHOOK_URL", "")

# Senior Media Buyer Guardrails & Automation Thresholds
TARGET_CPA = float(os.getenv("TARGET_CPA", "250.0"))        # In INR (Default target ₹250 per lead)
MAX_CPC = float(os.getenv("MAX_CPC", "15.0"))               # In INR (Default ₹15 max CPC)
BLEEDER_SPEND_MULTIPLIER = float(os.getenv("BLEEDER_SPEND_MULTIPLIER", "2.5"))
FATIGUE_FREQUENCY = float(os.getenv("FATIGUE_FREQUENCY", "3.2"))
WINNER_ROAS = float(os.getenv("WINNER_ROAS", "3.0"))
MAX_DAILY_BUDGET_CAP = float(os.getenv("MAX_DAILY_BUDGET_CAP", "5000.0"))
