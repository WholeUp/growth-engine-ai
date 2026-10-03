"""
Notification Hub: Multi-Channel Alert Dispatcher
Sends real-time alerts for Bleeder Ads killed, Winners scaled, and Daily Summaries.
Supports Telegram, WhatsApp Webhook, Rich Console, and Local Log File.
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
import requests

from config import settings

logger = logging.getLogger("NotificationHub")

custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "danger": "bold red",
    "success": "bold green",
    "highlight": "bold magenta"
})
console = Console(theme=custom_theme)

LOGS_DIR = Path(__file__).resolve().parent.parent / "outputs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
ALERT_LOG_FILE = LOGS_DIR / "ad_alerts.log"

class NotificationHub:
    def __init__(self):
        self.telegram_token = settings.TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = settings.TELEGRAM_CHAT_ID
        self.whatsapp_webhook = settings.WHATSAPP_WEBHOOK_URL

    def send_alert(self, title: str, message: str, level: str = "info", details: Dict[str, Any] = None) -> bool:
        """
        Dispatches alert across all active channels.
        Level: 'info', 'warning', 'danger', 'success'
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_text = f"[{timestamp}] [{level.upper()}] {title}\n{message}"
        if details:
            for k, v in details.items():
                formatted_text += f"\n• {k}: {v}"

        # 1. Rich Console Display
        color_map = {
            "info": "cyan",
            "warning": "yellow",
            "danger": "red",
            "success": "green"
        }
        panel_color = color_map.get(level.lower(), "white")
        console.print(Panel(formatted_text, title=f"🚨 AI MEDIA BUYER ALERT: {title}", border_style=panel_color))

        # 2. Append to Local Log File
        try:
            with open(ALERT_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(formatted_text + "\n" + "-"*50 + "\n")
        except Exception as e:
            logger.error(f"Failed to write to alert log: {e}")

        # 3. Telegram Bot Dispatch (if configured)
        if self.telegram_token and self.telegram_chat_id and not self.telegram_token.startswith("your_"):
            try:
                tg_url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
                tg_payload = {
                    "chat_id": self.telegram_chat_id,
                    "text": f"🤖 *AI Media Buyer Alert*\n*{title}*\n{message}",
                    "parse_mode": "Markdown"
                }
                requests.post(tg_url, json=tg_payload, timeout=5)
            except Exception as e:
                logger.error(f"Telegram notification error: {e}")

        # 4. WhatsApp Webhook Dispatch (if configured)
        if self.whatsapp_webhook and not self.whatsapp_webhook.startswith("your_"):
            try:
                wa_payload = {
                    "event": "ai_ad_alert",
                    "title": title,
                    "message": message,
                    "level": level,
                    "timestamp": timestamp,
                    "details": details or {}
                }
                requests.post(self.whatsapp_webhook, json=wa_payload, timeout=5)
            except Exception as e:
                logger.error(f"WhatsApp webhook notification error: {e}")

        return True
